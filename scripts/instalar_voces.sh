#!/usr/bin/env bash
# Instala las voces gratuitas (locales, sin suscripción) en una sesión nueva. Idempotente.
# Piper (voces es_MX/es_ES) y Kokoro-82M (Apache-2.0) en un entorno aislado con Python 3.12.
set -e
command -v espeak-ng >/dev/null || apt-get install -y -qq espeak-ng >/dev/null
python3 -c "import piper" 2>/dev/null || python3 -m pip install -q piper-tts
mkdir -p "${VOCES_DIR:=$HOME/.voces}"
for v in es/es_MX/claude/high/es_MX-claude-high es/es_MX/ald/medium/es_MX-ald-medium es/es_ES/davefx/medium/es_ES-davefx-medium; do
  n=$(basename "$v"); for ext in onnx onnx.json; do
    [ -f "$VOCES_DIR/$n.$ext" ] || curl -sSL -o "$VOCES_DIR/$n.$ext" "https://huggingface.co/rhasspy/piper-voices/resolve/main/$v.$ext"; done
done
if [ ! -x /tmp/kenv/bin/python ]; then
  command -v uv >/dev/null || python3 -m pip install -q uv
  uv venv -q -p 3.12 /tmp/kenv
  VIRTUAL_ENV=/tmp/kenv uv pip install -q --index-strategy unsafe-best-match \
    --extra-index-url https://download.pytorch.org/whl/cpu torch kokoro soundfile
fi
echo "Voces listas: Piper en $VOCES_DIR · Kokoro en /tmp/kenv"
