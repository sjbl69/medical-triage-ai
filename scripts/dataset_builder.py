import json

def build_sft_dataset(symptoms, responses):
    data = []
    for s, r in zip(symptoms, responses):
        data.append({
            "text": f"Patient: {s}\nDoctor: {r}"
        })
    return data

def save_dataset(data, path):
    with open(path, "w") as f:
        json.dump(data, f)