import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import DPOTrainer, DPOConfig

MODEL_NAME = "./models/sft-model"
OUTPUT_DIR = "./models/dpo-model"

# tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# model
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="cpu"
)

# dataset
dataset = load_dataset("json", data_files="data/dpo_dataset.json")["train"]

# CONFIG (CPU SAFE)
training_args = DPOConfig(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=1,
    num_train_epochs=2,
    logging_steps=1,
    bf16=False,
    fp16=False
)


trainer = DPOTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset
)

trainer.train()

model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)