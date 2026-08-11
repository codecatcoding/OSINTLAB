#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$PROJECT_ROOT/venv"
TOOLS_DIR="$PROJECT_ROOT/Herramientas"

mkdir -p \
  "$PROJECT_ROOT/Backups" \
  "$PROJECT_ROOT/Casos" \
  "$PROJECT_ROOT/Configuracion" \
  "$PROJECT_ROOT/Evidencias" \
  "$PROJECT_ROOT/Herramientas" \
  "$PROJECT_ROOT/Informes" \
  "$PROJECT_ROOT/Logs" \
  "$PROJECT_ROOT/Plantillas" \
  "$PROJECT_ROOT/Wordlists"

if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi

# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

python -m pip install --upgrade pip
python -m pip install -r "$PROJECT_ROOT/requirements.txt"

if ! command -v phoneinfoga >/dev/null 2>&1; then
  echo "PhoneInfoga no esta en PATH. Instalala manualmente o con tu gestor preferido."
fi

clone_or_update() {
  local repo_url="$1"
  local target_dir="$2"

  if [ -d "$target_dir/.git" ]; then
    git -C "$target_dir" pull --ff-only
  else
    git clone "$repo_url" "$target_dir"
  fi
}

clone_or_update "https://github.com/smicallef/spiderfoot.git" "$TOOLS_DIR/spiderfoot"
clone_or_update "https://github.com/lanmaster53/recon-ng.git" "$TOOLS_DIR/recon-ng"
clone_or_update "https://github.com/laramies/theHarvester.git" "$TOOLS_DIR/theHarvester"

python -m pip install \
  pyyaml dnspython mechanize flask-restful flasgger dicttoxml XlsxWriter \
  unicodecsv rq adblockparser ExifRead CherryPy cherrypy-cors Mako netaddr \
  ipwhois ipaddr phonenumbers pygexf python-whois secure python-docx \
  python-pptx publicsuffixlist cryptography pyOpenSSL

python -m pip install -e "$TOOLS_DIR/theHarvester"

cat > "$VENV_DIR/bin/spiderfoot" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT/Herramientas/spiderfoot"
exec "$PROJECT_ROOT/venv/bin/python" sf.py "$@"
EOF

cat > "$VENV_DIR/bin/recon-ng" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT/Herramientas/recon-ng"
exec "$PROJECT_ROOT/venv/bin/python" recon-ng "$@"
EOF

chmod +x "$VENV_DIR/bin/spiderfoot" "$VENV_DIR/bin/recon-ng"

python -m compileall -q "$PROJECT_ROOT/app" "$PROJECT_ROOT/run.py"

echo "OSINT LAB PRO instalado."
echo "Ejecuta: cd \"$PROJECT_ROOT\" && ./venv/bin/python run.py"
