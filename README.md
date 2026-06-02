# Local LLM FSM Benchmark (Ollama)

Experimento **100 % local** para evaluar modelos open-source con [Ollama](https://ollama.com) en la generación de **máquinas de estados finitas deterministas (FSM)** a partir de requisitos en lenguaje natural.

No se usan APIs de pago (OpenAI, Anthropic, Google, etc.).

## Objetivo

Comparar modelos locales en:

- validez JSON / cumplimiento de esquema
- determinismo
- cobertura de requisitos
- transiciones no soportadas o inferidas
- tamaño estructural de la FSM (estados, eventos, transiciones)

## Requisitos de hardware/software

| Componente | Recomendado |
|------------|-------------|
| GPU | NVIDIA RTX 4090 (24 GB VRAM) |
| Python | **3.11+** (usar `python3.12`; el `python3` del sistema puede ser 3.6) |
| Ollama | Instalado y en ejecución (`ollama serve`) |
| RAM | 32 GB+ recomendado para modelos 14B |

## Estructura del proyecto

```text
.
├── dataset/              # 20 sistemas × 12–13 requisitos numerados
├── prompts/              # Prompts y esquema FSM para Ollama
├── outputs/
│   ├── raw/              # Respuestas completas del modelo (JSON wrapper)
│   └── cleaned/          # FSM JSON parseado y validado
├── results/
│   ├── metrics.csv       # Resumen tabular (generado)
│   ├── summary_by_model.json
│   └── details/          # Métricas por modelo × sistema
├── scripts/
│   ├── check_models.py   # Verifica modelos instalados en Ollama
│   ├── run_experiment.py # Ejecuta generación FSM
│   ├── evaluate.py       # Agrega métricas → CSV
│   ├── plot_results.py   # Gráficos PNG + SVG
│   └── fsm_benchmark/    # Librería interna
├── figures/              # Gráficos exportados
├── paper/                # Borrador del artículo
├── requirements.txt
└── run_all.sh            # Pipeline reproducible completo
```

## Modelos evaluados

Obligatorios:

- `qwen2.5-coder:7b`
- `qwen2.5-coder:14b`
- `llama3.1:8b`
- `mistral-nemo:12b`
- `gemma2:9b`
- `phi3:14b`

Opcional (requiere más VRAM):

- `qwen2.5-coder:32b`

## Reproducibilidad — inicio rápido

### 1. Clonar / entrar al proyecto

```bash
cd /home/cesar/papers/ist2026
```

### 2. Instalar Ollama y descargar modelos

```bash
# Instalar Ollama: https://ollama.com/download
ollama serve   # en otra terminal si no está activo

# Verificar e instalar modelos
python3.12 scripts/check_models.py
# Copia y ejecuta cada comando `ollama pull ...` que imprima

# Con modelo opcional 32B
python3.12 scripts/check_models.py --include-optional
```

Comandos de instalación:

```bash
ollama pull qwen2.5-coder:7b
ollama pull qwen2.5-coder:14b
ollama pull llama3.1:8b
ollama pull mistral-nemo:12b
ollama pull gemma2:9b
ollama pull phi3:14b
# opcional:
ollama pull qwen2.5-coder:32b
```

### 3. Entorno Python

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Ejecutar todo el pipeline

```bash
chmod +x run_all.sh
./run_all.sh
```

Con modelo opcional 32B:

```bash
INCLUDE_OPTIONAL=1 ./run_all.sh
```

### 5. Ejecución paso a paso (manual)

```bash
source .venv/bin/activate

# 1) Comprobar modelos
python3.12 scripts/check_models.py

# 2) Generar FSMs (20 sistemas × N modelos)
python3.12 scripts/run_experiment.py

# Subconjunto para prueba rápida
python3.12 scripts/run_experiment.py \
  --models llama3.1:8b \
  --systems vending_machine atm

# 3) Calcular métricas
python3.12 scripts/evaluate.py

# 4) Generar figuras
python3.12 scripts/plot_results.py
```

## Salidas generadas

| Artefacto | Descripción |
|-----------|-------------|
| `outputs/raw/<modelo>/<sistema>.json` | Texto crudo + metadatos (tokens, duración) |
| `outputs/cleaned/<modelo>/<sistema>.json` | FSM JSON limpio |
| `results/metrics.csv` | Tabla principal para el paper |
| `results/summary_by_model.json` | Agregados por modelo |
| `results/details/<modelo>/<sistema>.json` | Métricas detalladas |
| `figures/*.png`, `figures/*.svg` | Gráficos |

## Métricas

| Métrica | Descripción |
|---------|-------------|
| `num_states` | Número de estados declarados |
| `num_events` | Número de eventos |
| `num_transitions` | Número de transiciones |
| `deterministic` | Sin pares `(source, event)` duplicados |
| `requirement_coverage` | Fracción de R1…Rn citados en transiciones |
| `unsupported_transitions` | Transiciones sin referencia válida a requisitos |
| `inferred_transitions` | Transiciones con requirement vacío o marcado implícito |
| `invalid_json` | No se pudo parsear/validar JSON |
| `schema_valid` | Cumple esquema Pydantic FSM |
| `unreachable_states` | Estados no alcanzables desde `initial_state` |

## Configuración del experimento

Parámetros en `scripts/fsm_benchmark/config.py`:

- `OLLAMA_TEMPERATURE = 0.0` — máxima reproducibilidad
- `OLLAMA_NUM_CTX = 8192` — contexto para requisitos largos
- Salida estructurada: esquema JSON vía API `format` de Ollama

Desactivar salida estructurada (ablation):

```bash
python3.12 scripts/run_experiment.py --no-structured-output
```

Continuar aunque falten modelos:

```bash
python3.12 scripts/run_experiment.py --skip-missing
```

## Dataset

20 sistemas en `dataset/systems/` (máquina expendedora, ATM, login, parking, ascensor, biblioteca, hotel, tickets, e-commerce, termostato, control de acceso, citas médicas, bici sharing, warehouse, examen online, alquiler coches, taquillas, restaurante, tren, gimnasio).

Ver `dataset/index.json` para el catálogo completo.

## Esquema FSM esperado

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

## Notas para RTX 4090

- Ejecutar modelos de a uno; Ollama gestiona VRAM automáticamente.
- El 32B puede requerir cuantización; usar solo si cabe en 24 GB.
- Para reducir tiempo de pilotaje: `--systems vending_machine login_system atm`.
- Tiempo estimado completo: ~2–6 h según modelos instalados y velocidad de inferencia.

## Citation

```bibtex
@misc{fsm_bench_20_ollama,
  title  = {FSM-Bench-20: Local Ollama Benchmark for LLM-Generated Deterministic FSMs},
  author = {...},
  year   = {2026},
  note   = {Dataset and scripts in repository}
}
```

## Licencia

Dataset y scripts: uso académico. Verificar licencias individuales de cada modelo en Ollama antes de publicar resultados.
