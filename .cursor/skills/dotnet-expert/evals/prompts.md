# Prompts de teste — `dotnet-expert`

Usar em conversas Cursor com a skill disponível no workspace. Após cada execução, preencher `runs/<run-id>.json` e gerar o HTML com `skill-creator/scripts/eval-viewer/generate_review.py`.

**Passar:** todas as métricas relevantes ≥ **0,8** e `passed: true` no prompt.

---

## p1 — Trigger positivo (revisão de PR .NET)

**Prompt:**

> Revisa o código .NET do projeto `contratantes/EdgardMoraes/ModuloFinal/SistemaBibliotecario`, focando na camada API e em possíveis problemas de segurança e EF Core. Usa o formato de relatório da skill.

**Critérios de sucesso:**

| Métrica | Critério |
|---------|----------|
| `trigger_correct` | Resposta no âmbito .NET/ASP.NET Core/EF; não mistura Scrum ou outra linguagem |
| `format_compliance` | Secções: Resumo, Crítico, Avisos, Sugestões, Decisões/trade-offs, Pontos positivos |
| `language_pt` | Texto principal em português |
| `no_hallucination` | Cita ficheiros reais do repo ou declara que não encontrou código |
| `conciseness` | Sem tutorial genérico longo não pedido |
| `security_baseline` | Menciona validação input/auth se aplicável; não expõe segredos |

---

## p2 — Trigger negativo (Scrum, não .NET)

**Prompt:**

> Facilita a retrospectiva do sprint e propõe três ações de melhoria com dono e prazo.

**Critérios de sucesso:**

| Métrica | Critério |
|---------|----------|
| `trigger_correct` | **Não** deve responder como especialista .NET (formato de code review); deve usar processo ágil / scrum-agile-project-management |
| `format_compliance` | Formato de retro (o que correu bem / melhorar / ações), não relatório de código |
| `language_pt` | Português |

*Nota:* se o agente aplicar ambas as skills, documentar em `notes` e marcar `trigger_correct` ≤ 0,5.

---

## p3 — Qualidade de saída (decisão de desenho, formato breve)

**Prompt:**

> Para uma API interna em ASP.NET Core 8, compara **Minimal APIs** vs **Controllers** só para endpoints CRUD com validação e OpenAPI. Não proponhas refactor do projeto inteiro.

**Critérios de sucesso:**

| Métrica | Critério |
|---------|----------|
| `trigger_correct` | Foco .NET / ASP.NET Core |
| `format_compliance` | Formato breve: Contexto assumido, Opções (A/B…), Recomendação e riscos, Próximos passos |
| `language_pt` | Português |
| `conciseness` | Sem lista massiva de refactor obrigatório |

---

## p4 — Edge case (sem código no repo)

**Prompt:**

> Revisa a performance do microserviço de pagamentos em produção. SLA 50 ms p99, 2M req/dia, stack desconhecida.

**Critérios de sucesso:**

| Métrica | Critério |
|---------|----------|
| `trigger_correct` | Mantém lente .NET/soluções se assumir stack Microsoft; ou pede stack |
| `no_hallucination` | **Declara premissas** ou pede repo/métricas; não inventa ficheiros nem números de profiling |
| `language_pt` | Português |
| `security_baseline` | Não sugere expor connection strings ou tokens |

---

## p5 — Integração com código real (EF Core)

**Prompt:**

> Analisa `EmprestimoRepositorio.cs` e `EmprestimoConfiguracao.cs` no SistemaBibliotecario: risco de N+1, SQL parametrizado e transações.

**Critérios de sucesso:**

| Métrica | Critério |
|---------|----------|
| `trigger_correct` | Lê ou referencia paths sob `SistemaBibliotecario` |
| `format_compliance` | Relatório estruturado ou secções claras com achados por severidade |
| `no_hallucination` | Citações `startLine:endLine:path` quando possível |
| `security_baseline` | SQL parametrizado / sem concatenação de input utilizador |

---

## p6 — Regressão (placeholder)

**Prompt:** _(copiar da run anterior o prompt que falhou)_

**Critérios:** métrica que falhou na run `baseline-0001` (ou última) passa a ≥ 0,8.

---

## Métricas (referência)

| Chave | Escala | Significado |
|-------|--------|-------------|
| `trigger_correct` | 0–1 | Skill e âmbito corretos |
| `format_compliance` | 0–1 | Templates da skill respeitados |
| `language_pt` | 0–1 | Português conforme skill |
| `no_hallucination` | 0–1 | Sem inventar repo/dados |
| `conciseness` | 0–1 | Resposta proporcional ao pedido |
| `security_baseline` | 0–1 | OWASP/input/secrets quando aplicável |

**`passed`:** `true` se média das métricas aplicáveis ≥ 0,8 e nenhuma crítica &lt; 0,5.
