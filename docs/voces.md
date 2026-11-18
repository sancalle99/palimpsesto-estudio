# Evaluación de voces gratuitas (18-nov-2026)

Estrellas y licencias leídas en GitHub el 18-nov-2026. Todas las pruebas se hicieron en CPU (4 núcleos), sin GPU.

| Modelo | Repositorio | ★ | Licencia | Español | Velocidad en CPU | Estado |
|---|---|---|---|---|---|---|
| **Kokoro-82M** (voz `em_alex`) | hexgrad/kokoro | — | Apache-2.0 | Sí (3 voces) | Muy rápida | **Elegida (DEC-0009)** |
| **Qwen3-TTS 0.6B CustomVoice** | [QwenLM/Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) | 14,5k | Apache-2.0 (código; confirmar los pesos en la ficha del modelo) | Sí (voces no nativas `ryan`, `aiden`) | ≈ 3,5 min de proceso por cada minuto de audio | En prueba: muestras enviadas al Director |
| Qwen3-TTS 1.7B VoiceDesign | ídem | ídem | ídem | Sí; la voz se describe con texto | Lenta en CPU (GPU recomendada) | Candidata futura |
| Chatterbox Multilingual V3 | [resemble-ai/chatterbox](https://github.com/resemble-ai/chatterbox) | 27,9k | MIT | Sí, con versiones afinadas para España y Latinoamérica | Media | **Archivado desde agosto de 2026** (sin mantenimiento); necesita un audio de referencia; incluye marca de agua |
| CosyVoice 3 | [FunAudioLLM/CosyVoice](https://github.com/FunAudioLLM/CosyVoice) | 24,4k | Apache-2.0 (código; pesos sin confirmar) | Sí | GPU | No probado |
| MeloTTS | [myshell-ai/MeloTTS](https://github.com/myshell-ai/MeloTTS) | 7,7k | MIT | Sí | Tiempo real | Calidad inferior a Kokoro |
| Piper | rhasspy/piper | — | Apache / CC0 / Unlicense según la voz | Sí | Muy rápida | Alternativa de respaldo |

**Descartados por licencia no comercial:** XTTS-v2 (CPML), F5-TTS (pesos CC-BY-NC) y Fish Speech / OpenAudio (pesos CC-BY-NC-SA).
