---
name: skill-creator
description: >-
  Cria e melhora skills do Cursor de forma iterativa: requisitos, rascunho, prompts de
  teste, avaliação qualitativa e quantitativa, viewer de resultados e refinamento até
  aprovação. Usar quando o usuário pedir criar skill, melhorar skill, avaliar skill,
  testar skill, métricas de skill ou fluxo de Skill Creator.
---

# Criador de Skills (Skill Creator)

## Papel

Guiar a **criação e evolução** de Agent Skills no projeto (`.cursor/skills/`) ou pessoais (`~/.cursor/skills/`), com ciclo **rascunho → teste → métricas → feedback → refinamento** até o utilizador ficar satisfeito.

**Nunca** criar skills em `~/.cursor/skills-cursor/` (reservado ao Cursor).

**Idioma:** português com o utilizador; `description` do frontmatter em **terceira pessoa**, com termos de trigger em PT e EN quando útil.

## Visão geral do processo

```
Requisitos → Rascunho → Testes → Avaliação (quali + quanti) → Viewer → Refinar → Repetir → Expandir testes
```

Copiar e atualizar o checklist em cada iteração:

```text
Progresso:
- [ ] 1. Requisitos e localização definidos
- [ ] 2. Rascunho SKILL.md (pasta nome-da-skill/)
- [ ] 3. Prompts de teste escritos (evals/prompts.md)
- [ ] 4. Execuções de teste registadas (evals/runs/*.json)
- [ ] 5. Métricas calculadas e explicadas ao utilizador
- [ ] 6. Review gerado (generate_review.py)
- [ ] 7. Feedback do utilizador incorporado
- [ ] 8. Conjunto de testes expandido (se aprovado na fase anterior)
```

---

## Fase 1 — Decidir o que a skill faz

Recolher (AskQuestion ou conversa):

| Campo | Pergunta |
|-------|----------|
| Propósito | Que tarefa ou fluxo deve a skill ensinar? |
| Localização | Projeto (`.cursor/skills/`) ou pessoal (`~/.cursor/skills/`)? |
| Triggers | Quando o agente deve aplicar automaticamente? |
| Conhecimento | O que o agente **não** sabe já e precisa desta skill? |
| Saída | Templates, formatos de relatório, idioma? |
| Restrições | Linhas máx., scripts obrigatórios, segurança? |

**Inferir** do contexto da conversa quando possível; confirmar premissas antes de fechar.

---

## Fase 2 — Rascunho da skill

### Estrutura obrigatória

```
nome-da-skill/
├── SKILL.md          # obrigatório (frontmatter + corpo)
├── reference.md      # opcional
├── examples.md       # opcional
└── scripts/          # opcional
```

### Frontmatter

```yaml
---
name: nome-em-kebab-case   # máx. 64 chars, [a-z0-9-]
description: >-            # máx. 1024 chars; O QUÊ + QUANDO; 3ª pessoa
---
```

### Princípios de escrita

- **Conciso:** só contexto que o modelo não traz por defeito.
- **SKILL.md &lt; 500 linhas**; detalhe em `reference.md`.
- **Grau de liberdade:** texto (alto), templates (médio), scripts (baixo).
- Referências **um nível** de profundidade a partir de `SKILL.md`.

Entregar rascunho inicial e pedir revisão rápida antes de testes pesados.

---

## Fase 3 — Prompts de teste

Criar ou atualizar `evals/prompts.md` na pasta da skill (ou em `skill-creator/evals/` como modelo).

**Mínimo recomendado por skill:**

| # | Tipo | Objetivo |
|---|------|----------|
| 1 | Trigger positivo | Pedido que **deve** activar a skill |
| 2 | Trigger negativo | Pedido próximo que **não** deve confundir com outra skill |
| 3 | Qualidade de saída | Verificar formato/template prometido |
| 4 | Edge case | Contexto incompleto — deve declarar premissas |
| 5 | Regressão | Caso que falhou numa iteração anterior |

Para cada prompt, documentar **critérios de sucesso** observáveis (não subjetivos vagos).

**Execução:** correr conversas (Cursor Agent) **com a skill disponível** no workspace; guardar transcrições ou resumos em `evals/runs/<run-id>.json` usando o schema em `evals/schema.json`.

Enquanto testes correm em segundo plano, preparar métricas (Fase 4).

---

## Fase 4 — Avaliação quantitativa

Usar ou adaptar `evals/metrics-template.json`. Métricas sugeridas (0–1 ou pass/fail):

| Métrica | Significado |
|---------|-------------|
| `trigger_correct` | Skill correcta aplicada (ou nenhuma quando negativo) |
| `format_compliance` | Seguiu templates/secções prometidas |
| `language_pt` | Resposta em português se acordado |
| `no_hallucination` | Não inventou requisitos/dados do projeto |
| `conciseness` | Sem verbosidade desnecessária |
| `security_baseline` | Sem segredos; validação input quando aplicável |

Calcular agregados: `pass_rate`, médias por métrica, lista de prompts falhados.

**Explicar ao utilizador** cada métrica antes de pedir feedback qualitativo.

---

## Fase 5 — Viewer de resultados

Gerar relatório HTML para revisão lado a lado:

```bash
python .cursor/skills/skill-creator/scripts/eval-viewer/generate_review.py \
  --input evals/runs/<run-id>.json \
  --output evals/runs/<run-id>-review.html
```

Abrir o HTML no browser (ou partilhar o caminho). O relatório deve mostrar: prompts, scores, notas, agregados e diff face à run anterior se existir.

---

## Fase 6 — Refinar com feedback

1. Recolher feedback **qualitativo** do utilizador (o que falhou na prática).
2. Cruzar com métricas (pass_rate &lt; 0,8 ou falha em `trigger_correct` → prioridade alta).
3. Reescrever `SKILL.md` (e ficheiros auxiliares) com mudanças **mínimas e focadas**.
4. Registar no JSON da run o campo `changes_made` (bullet list).
5. Voltar à Fase 3 até o utilizador aprovar.

---

## Fase 7 — Expandir testes

Após aprovação inicial:

- Duplicar prompts com variações (sinónimos, inglês, pedidos ambíguos).
- Adicionar cenários de integração (skill + código real do repo).
- Reexecutar métricas; comparar runs com `generate_review.py --compare <run-a> <run-b>`.

---

## Anti-padrões

- Skills genéricas (`helper`, `utils`).
- `description` em primeira pessoa ou sem triggers.
- Ficheiros planos `*_skill.md` na raiz de `.cursor/skills/` (usar pastas).
- Paths Windows com `\` na documentação.
- Informação datada (“antes de agosto 2025…”).
- Eval sem critérios observáveis.

---

## Recursos nesta skill

| Recurso | Uso |
|---------|-----|
| [evals/example-prompts.md](evals/example-prompts.md) | Modelo de prompts de teste |
| [evals/schema.json](evals/schema.json) | Schema JSON das runs |
| [evals/metrics-template.json](evals/metrics-template.json) | Template de métricas |
| [scripts/eval-viewer/generate_review.py](scripts/eval-viewer/generate_review.py) | Relatório HTML de avaliação |

Para boas práticas gerais de formato Cursor, complementar com a skill interna `create-skill` quando necessário.
