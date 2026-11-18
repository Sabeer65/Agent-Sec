# Phase 1 Audit: Agent-Sec baseline

Date: 2026-11-14. Branch: upgrade/production-ready (from main @ f4ae9d4).
Method: read the code, ran the existing tests, ran the pipeline and
individual components locally. Nothing in the code was changed.

Approach: findings are fixed in the system wherever feasible, and docs are
updated afterwards to describe what the system really does. Status is updated
(with commit hashes) as each fix lands.

## Resolved doubts

| Doubt | Finding | Fix |
|---|---|---|
| Attacker model `qwen/qwen3.8-27b` | Valid; it appears in my own Groq key's model list | None needed |
| Evaluator is "dual-pass" | One LLM call per verdict; the only second step is Pydantic format validation | Reword docs now; decide on a real second pass only after Phase 6 measures judge inconsistency |
| Tests cover attacker output shape and state defaults | Two tests. test_attacker makes a real Groq call and asserts a non-empty string; test_graph only checks four GraphState defaults | Phase 4 builds a real mocked suite |

## Measured baseline (small sample, not rates)

- 4 full runs and 5 probes with the hand-written attacks (attacks.py): all
  judged not vulnerable. The patcher never ran in a real run.
- Per-run time after warm-up: 11.1 s, 14.4 s, 11.3 s. The first run took
  120.6 s (cause not confirmed; cold model load is my guess).
- The local target is about 82-86% of each run; each Groq call takes ~1-2 s.
- qwen3:4b via Ollama: 3.2 GB, 100% GPU, context 4096 (from `ollama ps`).
- LangGraph recursion limit measured at 10,007 steps, so the only effective
  loop cap is max_iterations in route_after_evaluation.
- No leaked secrets found: .env never committed; no commit adds or removes
  "gsk_". (The scan covers only that key format.)

## Findings

| # | Finding | Fix in | Status |
|---|---|---|---|
| 1 | Groq clients are created at import time; a missing key crashes any import, including the whole dashboard | 2 | Open |
| 2 | No timeouts, retries or error handling on any LLM call | 2 | Open |
| 3 | Invalid judge JSON raises an unhandled ValidationError | 2 | Open |
| 4 | Untrusted text (attack, target reply) is not delimited for the judge or patcher | 2 | Open |
| 5 | Verdict schema is loose (confidence unbounded; contradictions allowed) | 2 | Open |
| 6 | Patcher output is not validated; an empty reply would become the system prompt | 2 | Open |
| 7 | Patched prompts mention <user_input> tags, but target.py never wraps input in them | 2 (wrap), 6 (measure effect) | Open |
| 8 | A failed attack ends the run, so the attacker never sees BLOCKED entries | 6 (measure, then decide) | Open |
| 9 | "iteration" counts patches, so report and dashboard show "0 / 5" after an attack was sent | 2 | Open |
| 10 | Report omits target reply, judge reasoning, original prompt, run id, backend and model | 2 | Open |
| 11 | Report filenames are timestamp-only (collision risk with parallel jobs) | 5 | Open |
| 12 | attacks.py is not used by the graph; attacks have no expected outcomes | 4 | Open |
| 13 | Unused import in graph.py; scratch file testapi.py in the repo root | 4 | Open |
| 14 | CI makes real Groq calls via a repo secret; triggers on main only; no ruff | 4 | Open |
| 15 | .gitignore gaps (.venv/, .env.*, *.db, caches); no .env.example | 2 | Open |
| 16 | requirements.txt is a full freeze (direct and transitive mixed); pytest in runtime deps | 2 | Open |
| 17 | The judge has only seen negative examples; its ability to catch real leaks is unmeasured | 6 | Open |
| 18 | Judge criterion ("break its rules") is vague; one roleplay reply was ambiguous | 6 | Open |
| 19 | Iteration cap: by code reading, up to 5 patches / 6 attacks, while docs say "5 iterations" (not yet observed in a run) | 2 (decide meaning), 4 (test) | Open |
| 20 | Dashboard live runs execute inside the Streamlit process: no auth, no per-visitor or global limit, no concurrency limit, no max prompt length | 5, 7 | Open |
| 21 | Hosted live test cannot work (needs local Ollama) | 3 (TARGET_BACKEND), then 5/7/8 (limits first) | Open |
| 22 | Raw exception text is shown to visitors | 7 | Open |
| 23 | Once live runs work, visitor runs would be written to the shared reports folder shown to all visitors. The hosting platform’s disk persistence is unverified | 5, 7 | Open |
| 24 | Dashboard reads reports without encoding="utf-8" and indexes fields directly (KeyError on old formats) | 7 | Open |
| 25 | Minor: sys.path hack and relative "reports/" path in the dashboard | 7 | Open |
| 26 | The attacker can refuse and return refusal text instead of an attack (seen once in ~7 calls). By code reading, that text is sent to the target as the "attack", so a refusal can be reported as a blocked attack | 2 | Open |

## Not yet audited

Dockerfile, docker-compose.yml, .devcontainer, full README text, and the
hosted demo's settings (platform and how secrets are configured there).
The hosted demo at agent-sec-project.streamlit.app (settings and secrets configuration)

## What may be claimed today

Only: the pipeline runs end to end locally; 4 full runs and 5 probes were all
judged not vulnerable; target memory use was 3.2 GB on GPU. Not claimed: any
attack-success or patch-effectiveness rate, "XML input isolation" as a working
defence, "dual-pass" evaluation, or live tests working on the hosted demo.