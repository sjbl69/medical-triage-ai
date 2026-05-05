#  Medical Triage AI — SFT + DPO (LoRA)

##  Project Overview

This project implements a **medical triage assistant** based on a language model fine-tuned using:

* **Supervised Fine-Tuning (SFT)** with LoRA
* **Preference Alignment (DPO)**
* Clinical evaluation and safety testing

The goal is to build a **safe and efficient triage system** capable of distinguishing between urgent and non-urgent medical situations.

---

##  Tech Stack

* Python
* PyTorch
* Hugging Face Transformers
* TRL (SFTTrainer, DPOTrainer)
* PEFT (LoRA)
* Datasets

---

##  Model

* Base model: `distilgpt2` *(lightweight for prototyping)*
* Training methods:

  * SFT (LoRA)
  * DPO (Direct Preference Optimization)

---

##  Project Structure

```
├── data/
│   ├── sft_dataset.json
│   ├── dpo_dataset.json
│
├── models/
│   ├── sft/
│   ├── dpo/
│
├── metadata/
│   ├── data_sources.md
│   ├── schema.json
│
├── scripts/
│   ├── data_cleaning.py
│   ├── anonymization.py
│   ├── dataset_builder.py
│
├── logs/
│   └── experiment.json
│
└── notebook.ipynb
```

---

##  Dataset

### SFT Dataset

* ~400 synthetic examples
* Format:

```
Patient: <symptom>
Doctor: <response>
```

### DPO Dataset

* Preference pairs:

  * `chosen` → correct response
  * `rejected` → incorrect / unsafe response

---

##  Training Pipeline

### 1. Supervised Fine-Tuning (SFT)

* LoRA applied on attention layers
* Reduces GPU memory usage
* Improves base model behavior

### 2. Preference Alignment (DPO)

* Trains model to prefer safe and correct outputs
* Uses human-like preference pairs

---

##  Evaluation

### Clinical Evaluation

| Test Case      | Expected    | Result |
| -------------- | ----------- | ------ |
| Chest pain     | URGENCE     | ✅      |
| Heavy bleeding | URGENCE     | ✅      |
| Headache       | NON URGENCE | ✅      |
| Diarrhea       | NON URGENCE | ✅      |

 Score automatically computed in pipeline

---

##  Experiment Tracking

Saved in:

```
logs/experiment.json
```

Includes:

* Model configuration
* Training parameters
* Dataset size
* Evaluation score

---

##  Reproducibility

* Deterministic dataset generation
* Logged hyperparameters
* Saved checkpoints:

  * `models/sft/`
  * `models/dpo/`


---


##  Author

Selma — AI Engineer
Project: Medical Triage AI

---

## ⚠️ Disclaimer

This project is for **educational purposes only**.
It must **not be used for real medical diagnosis or treatment**.
