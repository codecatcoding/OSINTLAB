const OSINTLAB_REPORT_PRODUCT_OPTION = 'osintlab_report_product_id';
const OSINTLAB_REPORT_API_OPTION = 'osintlab_report_api_base';
const OSINTLAB_REPORT_SECRET_OPTION = 'osintlab_report_secret';
const OSINTLAB_REPORT_COUPON_CODE = 'code2026';
const OSINTLAB_REPORT_API_DEFAULT = 'https://cakes-storm-migration-singles.trycloudflare.com';
const OSINTLAB_WIDGET_RAW_URL = 'https://raw.githubusercontent.com/codecatcoding/OSINTLAB/main/wordpress/elementor/osintlab-widget.html';

add_action('init', 'osintlab_snippet_bootstrap');
add_action('rest_api_init', 'osintlab_snippet_routes');
add_filter('the_content', 'osintlab_snippet_replace_page', 99);
add_filter('woocommerce_add_cart_item_data', 'osintlab_snippet_cart_item_data', 10, 3);
add_action('woocommerce_checkout_create_order', 'osintlab_snippet_attach_report_to_order', 10, 2);
add_action('woocommerce_thankyou', 'osintlab_snippet_download_button', 20);
add_action('woocommerce_order_details_after_order_table', 'osintlab_snippet_download_button_for_order', 20);

function osintlab_snippet_bootstrap() {
    if (get_option(OSINTLAB_REPORT_API_OPTION) !== OSINTLAB_REPORT_API_DEFAULT) {
        update_option(OSINTLAB_REPORT_API_OPTION, OSINTLAB_REPORT_API_DEFAULT);
    }

    $widget = get_transient('osintlab_widget_html');

    if ($widget && strpos($widget, OSINTLAB_REPORT_API_DEFAULT) === false) {
        delete_transient('osintlab_widget_html');
    }

    osintlab_snippet_product_and_coupon();
}

function osintlab_snippet_product_and_coupon() {
    if (!class_exists('WooCommerce') || !class_exists('WC_Product_Simple')) {
        return;
    }

    $product_id = absint(get_option(OSINTLAB_REPORT_PRODUCT_OPTION));
    $product = $product_id ? wc_get_product($product_id) : false;

    if (!$product) {
        $product = new WC_Product_Simple();
        $product->set_name('Informe OSINT LAB PRO');
        $product->set_slug('informe-osint-lab-pro');
        $product->set_description('Generacion de informe PDF OSINT LAB PRO a partir de resultados recopilados en la consola web.');
        $product->set_short_description('Informe PDF OSINT LAB PRO.');
        $product->set_regular_price('10');
        $product->set_price('10');
        $product->set_virtual(true);
        $product->set_sold_individually(true);
        $product->set_catalog_visibility('visible');
        $product->set_status('publish');
        $product_id = $product->save();
        update_option(OSINTLAB_REPORT_PRODUCT_OPTION, $product_id);
    }

    if (class_exists('WC_Coupon') && $product_id) {
        $coupon_id = wc_get_coupon_id_by_code(OSINTLAB_REPORT_COUPON_CODE);
        $coupon = $coupon_id ? new WC_Coupon($coupon_id) : new WC_Coupon();
        $coupon->set_code(OSINTLAB_REPORT_COUPON_CODE);
        $coupon->set_discount_type('percent');
        $coupon->set_amount(100);
        $coupon->set_product_ids(array($product_id));
        $coupon->set_individual_use(false);
        $coupon->set_status('publish');
        $coupon->save();
    }
}

function osintlab_snippet_replace_page($content) {
    if (is_admin() || !is_main_query() || !in_the_loop() || !is_page('osintlab')) {
        return $content;
    }

    $widget = get_transient('osintlab_widget_html');

    if (!$widget) {
        $response = wp_remote_get(OSINTLAB_WIDGET_RAW_URL, array('timeout' => 15));

        if (!is_wp_error($response) && wp_remote_retrieve_response_code($response) === 200) {
            $widget = wp_remote_retrieve_body($response);
            set_transient('osintlab_widget_html', $widget, HOUR_IN_SECONDS);
        }
    }

    return $widget ?: $content;
}

function osintlab_snippet_routes() {
    register_rest_route('osintlab/v1', '/report/checkout', array(
        'methods' => 'POST',
        'callback' => 'osintlab_snippet_create_checkout',
        'permission_callback' => '__return_true',
    ));

    register_rest_route('osintlab/v1', '/report/download/(?P<order_id>\d+)', array(
        'methods' => 'GET',
        'callback' => 'osintlab_snippet_download_pdf',
        'permission_callback' => '__return_true',
    ));
}

function osintlab_snippet_create_checkout(WP_REST_Request $request) {
    if (!class_exists('WooCommerce')) {
        return new WP_Error('woocommerce_missing', 'WooCommerce no esta activo.', array('status' => 500));
    }

    osintlab_snippet_product_and_coupon();
    $product_id = absint(get_option(OSINTLAB_REPORT_PRODUCT_OPTION));

    if (!$product_id || !wc_get_product($product_id)) {
        return new WP_Error('product_missing', 'No se pudo crear el producto de informe.', array('status' => 500));
    }

    $payload = $request->get_json_params();
    $items = isset($payload['items']) && is_array($payload['items']) ? $payload['items'] : array();

    if (empty($items)) {
        return new WP_Error('empty_report', 'No hay resultados para generar informe.', array('status' => 400));
    }

    $report_id = wp_generate_uuid4();
    $report_payload = array(
        'title' => 'Informe OSINT LAB PRO',
        'subject' => sanitize_text_field($payload['subject'] ?? ''),
        'items' => osintlab_snippet_sanitize_items($items),
    );

    set_transient('osintlab_report_' . $report_id, $report_payload, DAY_IN_SECONDS * 2);

    if (function_exists('WC') && WC()->session) {
        WC()->session->set('osintlab_report_id', $report_id);
    }

    $checkout_url = add_query_arg(
        array('add-to-cart' => $product_id, 'osint_report_id' => rawurlencode($report_id)),
        wc_get_checkout_url()
    );

    return rest_ensure_response(array(
        'ok' => true,
        'report_id' => $report_id,
        'product_id' => $product_id,
        'coupon' => OSINTLAB_REPORT_COUPON_CODE,
        'checkout_url' => $checkout_url,
    ));
}

function osintlab_snippet_sanitize_items($items) {
    $clean = array();

    foreach (array_slice($items, 0, 25) as $item) {
        if (!is_array($item)) {
            continue;
        }

        $clean[] = array(
            'tool' => sanitize_text_field($item['tool'] ?? ''),
            'target' => sanitize_text_field($item['target'] ?? ''),
            'endpoint' => sanitize_text_field($item['endpoint'] ?? ''),
            'ok' => !empty($item['ok']),
            'returncode' => intval($item['returncode'] ?? 0),
            'stdout' => wp_strip_all_tags((string) ($item['stdout'] ?? '')),
            'stderr' => wp_strip_all_tags((string) ($item['stderr'] ?? '')),
            'results' => array_values(array_map('sanitize_text_field', array_slice((array) ($item['results'] ?? array()), 0, 200))),
            'captured_at' => sanitize_text_field($item['captured_at'] ?? ''),
        );
    }

    return $clean;
}

function osintlab_snippet_cart_item_data($cart_item_data, $product_id, $variation_id) {
    $report_product_id = absint(get_option(OSINTLAB_REPORT_PRODUCT_OPTION));

    if ($report_product_id && intval($product_id) === $report_product_id && !empty($_GET['osint_report_id'])) {
        $report_id = sanitize_text_field(wp_unslash($_GET['osint_report_id']));
        $cart_item_data['osintlab_report_id'] = $report_id;
        $cart_item_data['unique_key'] = md5($report_id . microtime());

        if (function_exists('WC') && WC()->session) {
            WC()->session->set('osintlab_report_id', $report_id);
        }
    }

    return $cart_item_data;
}

function osintlab_snippet_attach_report_to_order($order, $data) {
    $report_id = function_exists('WC') && WC()->session ? WC()->session->get('osintlab_report_id') : '';

    if (!$report_id && !empty($_REQUEST['osint_report_id'])) {
        $report_id = sanitize_text_field(wp_unslash($_REQUEST['osint_report_id']));
    }

    if (!$report_id) {
        return;
    }

    $payload = get_transient('osintlab_report_' . $report_id);

    if ($payload) {
        $order->update_meta_data('_osintlab_report_id', $report_id);
        $order->update_meta_data('_osintlab_report_payload', wp_json_encode($payload));
    }
}

function osintlab_snippet_download_button($order_id) {
    osintlab_snippet_download_button_for_order(wc_get_order($order_id));
}

function osintlab_snippet_download_button_for_order($order) {
    if (!$order instanceof WC_Order || !$order->is_paid() || !$order->get_meta('_osintlab_report_payload')) {
        return;
    }

    $url = add_query_arg(array('key' => $order->get_order_key()), rest_url('osintlab/v1/report/download/' . $order->get_id()));
    echo '<p><a class="button" href="' . esc_url($url) . '">Descargar informe OSINT PDF</a></p>';
}

function osintlab_snippet_download_pdf(WP_REST_Request $request) {
    $order_id = absint($request['order_id']);
    $key = sanitize_text_field($request->get_param('key'));
    $order = wc_get_order($order_id);

    if (!$order || !hash_equals($order->get_order_key(), $key) || !$order->is_paid()) {
        return new WP_Error('forbidden', 'Informe no disponible o pago no confirmado.', array('status' => 403));
    }

    $payload_json = $order->get_meta('_osintlab_report_payload');
    $payload = $payload_json ? json_decode($payload_json, true) : null;

    if (!$payload) {
        return new WP_Error('missing_report', 'No se encontro el contenido del informe.', array('status' => 404));
    }

    $api_base = untrailingslashit(get_option(OSINTLAB_REPORT_API_OPTION, OSINTLAB_REPORT_API_DEFAULT));
    $headers = array('Content-Type' => 'application/json');
    $secret = get_option(OSINTLAB_REPORT_SECRET_OPTION, '');

    if ($secret) {
        $headers['X-OSINTLAB-REPORT-SECRET'] = $secret;
    }

    $response = wp_remote_post($api_base . '/api/reports/pdf', array(
        'timeout' => 60,
        'headers' => $headers,
        'body' => wp_json_encode($payload),
    ));

    if (is_wp_error($response)) {
        return new WP_Error('api_error', $response->get_error_message(), array('status' => 502));
    }

    if (wp_remote_retrieve_response_code($response) < 200 || wp_remote_retrieve_response_code($response) >= 300) {
        return new WP_Error('api_error', 'La API no pudo generar el PDF.', array('status' => 502));
    }

    nocache_headers();
    header('Content-Type: application/pdf');
    header('Content-Disposition: attachment; filename="informe-osintlab-' . $order_id . '.pdf"');
    echo wp_remote_retrieve_body($response);
    exit;
}
