#!/usr/bin/env python3
"""Gera relatório HTML a partir de evals/runs/*.json para revisão de skills."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any


def load_run(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def compute_aggregate(run: dict[str, Any]) -> dict[str, Any]:
    prompts = run.get("prompts", [])
    if not prompts:
        return {"pass_rate": 0.0, "avg_scores": {}}

    passed = sum(1 for p in prompts if p.get("passed") is True)
    pass_rate = passed / len(prompts) if prompts else 0.0

    score_keys: set[str] = set()
    for p in prompts:
        score_keys.update(p.get("scores", {}).keys())

    avg_scores: dict[str, float] = {}
    for key in sorted(score_keys):
        values = [p["scores"][key] for p in prompts if key in p.get("scores", {})]
        avg_scores[key] = sum(values) / len(values) if values else 0.0

    return {"pass_rate": pass_rate, "avg_scores": avg_scores}


def render_prompt_row(prompt: dict[str, Any]) -> str:
    scores = prompt.get("scores", {})
    scores_html = "".join(
        f"<li><strong>{escape(k)}</strong>: {v:.2f}</li>" for k, v in sorted(scores.items())
    )
    status = "pass" if prompt.get("passed") else "fail"
    return f"""
    <article class="prompt {status}">
      <header>
        <span class="badge">{escape(prompt.get('type', 'unknown'))}</span>
        <code>{escape(prompt.get('id', ''))}</code>
        <span class="status">{status.upper()}</span>
      </header>
      <p><strong>Prompt:</strong> {escape(prompt.get('prompt', ''))}</p>
      <p><strong>Esperado:</strong> {escape(prompt.get('expected', '—'))}</p>
      <p><strong>Resumo:</strong> {escape(prompt.get('actual_summary', '—'))}</p>
      <ul>{scores_html or '<li>Sem scores</li>'}</ul>
      <p><em>{escape(prompt.get('notes', ''))}</em></p>
    </article>
    """


def render_run_section(title: str, run: dict[str, Any]) -> str:
    agg = run.get("aggregate") or compute_aggregate(run)
    avg_items = "".join(
        f"<li>{escape(k)}: {v:.2f}</li>" for k, v in sorted(agg.get("avg_scores", {}).items())
    )
    prompts_html = "".join(render_prompt_row(p) for p in run.get("prompts", []))
    changes = run.get("changes_made") or []
    changes_html = (
        "<ul>" + "".join(f"<li>{escape(c)}</li>" for c in changes) + "</ul>"
        if changes
        else "<p>—</p>"
    )
    return f"""
    <section class="run">
      <h2>{escape(title)}</h2>
      <p><strong>Skill:</strong> {escape(run.get('skill_name', ''))}</p>
      <p><strong>Run ID:</strong> {escape(run.get('run_id', ''))}</p>
      <p><strong>Pass rate:</strong> {agg.get('pass_rate', 0):.0%}</p>
      <h3>Médias por métrica</h3>
      <ul>{avg_items or '<li>—</li>'}</ul>
      <h3>Alterações nesta iteração</h3>
      {changes_html}
      <h3>Prompts</h3>
      {prompts_html}
    </section>
    """


def build_html(runs: list[tuple[str, dict[str, Any]]], compare: bool) -> str:
    sections = "".join(render_run_section(title, run) for title, run in runs)
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    compare_note = (
        "<p class='compare'>Modo comparação: duas runs lado a lado.</p>" if compare else ""
    )
    return f"""<!DOCTYPE html>
<html lang="pt">
<head>
  <meta charset="utf-8"/>
  <title>Skill Eval Review</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 2rem; max-width: 960px; }}
    .prompt {{ border: 1px solid #ccc; border-radius: 8px; padding: 1rem; margin: 1rem 0; }}
    .prompt.pass {{ border-left: 4px solid #2e7d32; }}
    .prompt.fail {{ border-left: 4px solid #c62828; }}
    .badge {{ background: #eee; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.85rem; }}
    .status {{ float: right; font-weight: bold; }}
    .compare {{ background: #e3f2fd; padding: 0.5rem 1rem; border-radius: 4px; }}
    h1 {{ margin-bottom: 0.25rem; }}
    .meta {{ color: #666; font-size: 0.9rem; }}
  </style>
</head>
<body>
  <h1>Skill Eval Review</h1>
  <p class="meta">Gerado em {generated}</p>
  {compare_note}
  {sections}
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Gera relatório HTML de avaliação de skills.")
    parser.add_argument("--input", "-i", required=True, help="JSON da run (ou primeiro de --compare)")
    parser.add_argument("--output", "-o", help="Ficheiro HTML de saída (stdout se omitido)")
    parser.add_argument(
        "--compare",
        nargs="?",
        const=True,
        metavar="RUN_B",
        help="Segundo JSON para comparar (ou --compare RUN_B)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Erro: ficheiro não encontrado: {input_path}", file=sys.stderr)
        return 1

    runs: list[tuple[str, dict[str, Any]]] = [("Run A", load_run(input_path))]

    compare_mode = False
    if args.compare:
        compare_mode = True
        if args.compare is True:
            print("Erro: --compare requer o caminho do segundo JSON.", file=sys.stderr)
            return 1
        compare_path = Path(args.compare)
        if not compare_path.exists():
            print(f"Erro: ficheiro não encontrado: {compare_path}", file=sys.stderr)
            return 1
        runs.append(("Run B", load_run(compare_path)))

    html = build_html(runs, compare_mode)
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")
        print(f"Relatório escrito em: {out_path}")
    else:
        print(html)
    return 0


if __name__ == "__main__":
    sys.exit(main())
