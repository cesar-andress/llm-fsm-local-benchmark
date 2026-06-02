# Local LLM FSM Benchmark (Ollama)

Fully **local** experiment for evaluating open-source models with [Ollama](https://ollama.com) on **deterministic finite state machine (FSM)** generation from natural-language requirements.

No paid APIs (OpenAI, Anthropic, Google, etc.) are used.

## Objective

Compare local models on:

- JSON validity and schema compliance
- Determinism
- Requirement coverage
- Unsupported or inferred transitions
- Structural FSM size (states, events, transitions)

## Hardware and software requirements

| Component | Recommended |
|-----------|-------------|
| GPU | NVIDIA RTX 4090 (24 GB VRAM) |
| Python | **3.11+** (use `python3.12`; system `python3` may be older) |
| Ollama | Installed and running (`ollama serve`) |
| RAM | 32 GB+ recommended for 14B models |

## Project structure

```text
.
├── dataset/              # 20 systems × 12–13 numbered requirements
├── benchmark/            # Catalog, gold FSM placeholders
├── prompts/              # FSM generation prompts and schema
├── outputs/
│   ├── raw/              # Full model responses (JSON wrapper)
│   └── cleaned/          # Parsed FSM JSON
├── results/
│   ├── metrics.csv       # Summary table (generated)
│   ├── summary_by_model.json
│   └── details/          # Per model × system metrics
├── scripts/
│   ├── check_models.py   # Verify Ollama models
│   ├── run_experiment.py # FSM generation
│   ├── evaluate.py       # Metrics → CSV
│   ├── plot_results.py   # PNG + SVG figures
│   └── fsm_benchmark/    # Internal library
├── figures/              # Exported plots
├── docs/                 # Evaluation protocol, gold strategy, language policy
├── requirements.txt
└── run_all.sh            # Reproducible pipeline
```

## Models evaluated

Required:

- `qwen2.5-coder:7b`
- `qwen2.5-coder:14b`
- `llama3.1:8b`
- `mistral-nemo:12b`
- `gemma2:9b`
- `phi3:14b`

Optional (higher VRAM):

- `qwen2.5-coder:32b`

## Quick start

### 1. Clone and enter the repository

```bash
git clone git@github.com:cesar-andress/llm-fsm-local-benchmark.git
cd llm-fsm-local-benchmark
```

### 2. Install Ollama and pull models

```bash
ollama serve   # separate terminal if not already running

python3.12 scripts/check_models.py
# Run each printed `ollama pull ...` command

python3.12 scripts/check_models.py --include-optional   # optional 32B
```

### 3. Python environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Run the full pipeline

```bash
chmod +x run_all.sh
./run_all.sh
```

With optional 32B model:

```bash
INCLUDE_OPTIONAL=1 ./run_all.sh
```

### 5. Step-by-step (manual)

```bash
source .venv/bin/activate
python3.12 scripts/check_models.py
python3.12 scripts/run_experiment.py
python3.12 scripts/evaluate.py
python3.12 scripts/plot_results.py
```

Pilot run:

```bash
python3.12 scripts/run_experiment.py \
  --models llama3.1:8b \
  --systems vending_machine atm
```

## Outputs

| Artifact | Description |
|----------|-------------|
| `outputs/raw/<model>/<system>.json` | Raw response + metadata (tokens, duration) |
| `outputs/cleaned/<model>/<system>.json` | Clean FSM JSON |
| `results/metrics.csv` | Main results table |
| `results/summary_by_model.json` | Per-model aggregates |
| `results/details/<model>/<system>.json` | Detailed metrics |
| `figures/*.png`, `figures/*.svg` | Plots |

## Metrics

| Metric | Description |
|--------|-------------|
| `num_states` | Number of declared states |
| `num_events` | Number of events |
| `num_transitions` | Number of transitions |
| `deterministic` | No duplicate `(source, event)` pairs |
| `requirement_coverage` | Fraction of R1…Rn cited in transitions |
| `unsupported_transitions` | Transitions without valid requirement references |
| `inferred_transitions` | Transitions with empty or implicit requirement fields |
| `invalid_json` | JSON parse failure |
| `schema_valid` | Passes Pydantic FSM schema |
| `unreachable_states` | States not reachable from `initial_state` |

## Configuration

Key parameters in `scripts/fsm_benchmark/config.py`:

- `OLLAMA_TEMPERATURE = 0.0` — reproducibility
- `OLLAMA_NUM_CTX = 8192` — context for long requirements
- Structured output via Ollama `format` JSON schema

Ablation (disable structured output):

```bash
python3.12 scripts/run_experiment.py --no-structured-output
```

## Dataset

20 systems in `dataset/systems/` covering vending machines, ATMs, login, parking gates, elevators, libraries, hotels, ticketing, e-commerce, thermostats, access control, medical booking, bike rental, warehouse inventory, online exams, car rental, package lockers, restaurants, trains, and gym membership.

See `dataset/index.json` for the full catalog and `docs/dataset.md` for schema details.

## Expected FSM schema

```json
{
  "states": ["Idle", "..."],
  "initial_state": "Idle",
  "events": ["insert_coin"],
  "transitions": [
    {
      "source": "Idle",
      "event": "insert_coin",
      "guard": "true",
      "action": "store_credit",
      "target": "CreditAvailable",
      "requirement": "R2"
    }
  ],
  "forbidden_behaviours": []
}
```

## RTX 4090 notes

- Run one model at a time; Ollama manages VRAM.
- 32B may require quantisation; use only if it fits in 24 GB.
- Reduce pilot time: `--systems vending_machine login_system atm`.
- Full run: approximately 2–6 hours depending on models and inference speed.

## Documentation

| Document | Description |
|----------|-------------|
| `REPRODUCIBILITY.md` | Full reproduction guide |
| `docs/evaluation_protocol.md` | Research questions and metrics |
| `docs/gold_standard_strategy.md` | Gold FSM methodology |
| `docs/PROJECT_RULES.md` | Language, repository separation, commits, releases |
| `docs/LANGUAGE_POLICY.md` | English-only policy (summary) |
| `docs/RESEARCH_REPOSITORY_POLICY.md` | Artifact placement (summary) |

## Citation

See `CITATION.cff`. Use the Zenodo DOI when available.

## License

MIT — see `LICENSE`. Verify individual model licenses on Ollama before publishing results.
