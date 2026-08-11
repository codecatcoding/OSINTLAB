# OSINT LAB PRO Reports para WordPress

Plugin WooCommerce para vender informes PDF generados desde el widget OSINT LAB PRO.

## Que hace

- Crea el producto `Informe OSINT LAB PRO` por 10 EUR.
- Crea el cupon `code2026` con 100% de descuento para ese producto.
- Recibe los resultados acumulados por el widget.
- Redirige al checkout de WooCommerce/Stripe.
- Tras pago confirmado, muestra un boton para descargar el PDF.
- Solicita el PDF a la API OSINT LAB PRO.

## Instalacion

1. Comprime la carpeta `osintlab-reports`.
2. En WordPress ve a `Plugins > Anadir nuevo > Subir plugin`.
3. Sube el ZIP y activa el plugin.
4. Revisa `WooCommerce > OSINT LAB Reports`.
5. Confirma que la API apunta a tu tunnel activo o a `https://api.codecatcoding.com` cuando quede definitivo.

## Widget Elementor

El widget debe tener:

```html
data-report-endpoint="/wp-json/osintlab/v1/report/checkout"
data-report-price="10"
data-report-currency="EUR"
```

## Seguridad de produccion

Para produccion, configura el mismo secreto en:

API:

```bash
export OSINTLAB_REPORT_SECRET="cambia-este-secreto"
```

WordPress:

```text
WooCommerce > OSINT LAB Reports > Report secret
```

Sin secreto, el modo actual sirve para probar el flujo con el tunnel temporal.
