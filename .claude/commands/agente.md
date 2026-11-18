---
description: Consulta directa a un agente del estudio (uso: /agente <nombre> <pregunta>). Nombres: ceo, investigador, guionista, productor, editor, auditor, analista, cfo
---
El Director quiere consultar directamente a un agente: $ARGUMENTS

1. La primera palabra es el nombre del agente (ceo, investigador, guionista, productor, editor, auditor, analista, cfo). Si no coincide con ninguno, muestra la lista y pregunta.
2. Si el agente es `investigador` o `auditor`, delega la consulta en ese subagente (`.claude/agents/<nombre>.md`); para los demás, carga su skill (`.claude/skills/<nombre>/SKILL.md`) y responde tú con ese rol, sin lanzar subagente. En ambos casos usa el resto del texto **literalmente** como pregunta del Director, junto con el contexto necesario (ID de producción si se menciona; estado actual con `python3 -m estudio estado <ID>`).
3. Es una **consulta**: el agente responde, explica o propone, pero no cambia el estado de ninguna producción ni genera gastos, salvo que el Director lo pida expresamente en el mensaje.
4. Devuelve la respuesta del agente encabezada con su nombre (p. ej., «**Investigador:**»). Si la pregunta contiene una idea, objeción o perspectiva editorial, ofrece registrarla en el Cuaderno con `/nota`.
