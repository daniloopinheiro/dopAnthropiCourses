# Modelo de prompts de teste

Substituir `{{SKILL_NAME}}` e adaptar critérios por skill.

## 1. Trigger positivo

**Prompt:** «Preciso de uma revisão de código .NET neste PR.»

**Sucesso:** aplica `dotnet-expert`; lê código real; relatório com secções definidas na skill.

## 2. Trigger negativo

**Prompt:** «Prioriza o backlog do sprint.»

**Sucesso:** aplica `scrum-agile-project-management`, **não** skill técnica de linguagem.

## 3. Qualidade de saída

**Prompt:** «Analisa apenas a decisão entre Minimal API e Controllers.»

**Sucesso:** usa formato breve (Contexto / Opções / Recomendação / Próximos passos); sem refactor massivo não pedido.

## 4. Edge case

**Prompt:** «Revisa a arquitetura do sistema X» (sem repo nem requisitos).

**Sucesso:** declara premissas ou pede o mínimo; não inventa SLAs nem stack.

## 5. Regressão

**Prompt:** _(copiar prompt que falhou na run anterior)_

**Sucesso:** critério que falhou na métrica `{{METRIC}}` passa a ≥ 0,8.
