import re

def anonymize(text):
    text = re.sub(r"\b\d{2,}\b", "[NUM]", text)
    text = re.sub(r"[A-Z][a-z]+", "[NAME]", text)
    return text

def anonymize_dataset(dataset):
    return [{"text": anonymize(x["text"])} for x in dataset]