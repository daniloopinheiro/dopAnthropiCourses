# Avaliações — `dotnet-expert`

## Ficheiros

| Ficheiro | Uso |
|----------|-----|
| [prompts.md](prompts.md) | Prompts e critérios de sucesso (p1–p6) |
| [runs/](runs/) | Uma JSON por execução de teste |
| [runs/baseline-0001.json](runs/baseline-0001.json) | Template inicial — preencher após testes |

## Fluxo

1. Executar cada prompt em **p1–p5** numa conversa Cursor (skill activa no projeto).
2. Copiar `runs/baseline-0001.json` → `runs/YYYYMMDD-HHMM.json` ou editar o baseline.
3. Preencher `actual_summary`, `scores`, `passed`, `notes` por prompt.
4. Gerar relatório HTML:

```powershell
Set-Location D:\source\repos\dopme-io\dopmeConsultoria
python .cursor/skills/skill-creator/scripts/eval-viewer/generate_review.py `
  --input .cursor/skills/dotnet-expert/evals/runs/baseline-0001.json `
  --output .cursor/skills/dotnet-expert/evals/runs/baseline-0001-review.html
```

5. Comparar duas runs:

```powershell
python .cursor/skills/skill-creator/scripts/eval-viewer/generate_review.py `
  --input .cursor/skills/dotnet-expert/evals/runs/baseline-0001.json `
  --compare .cursor/skills/dotnet-expert/evals/runs/20260522-1400.json `
  --output .cursor/skills/dotnet-expert/evals/runs/compare-review.html
```

6. Ajustar `../SKILL.md` conforme feedback; registar em `changes_made`; repetir **p6** se necessário.

## Meta de aprovação

- `aggregate.pass_rate` ≥ **0,8** (mínimo 4/5 prompts em p1–p5).
- Nenhum `trigger_correct` &lt; **0,5** em p1 ou p2.
