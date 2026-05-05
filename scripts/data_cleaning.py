def clean_text(text):
    text = text.strip()
    text = text.replace("  ", " ")
    return text

def clean_dataset(dataset):
    return [{"text": clean_text(x["text"])} for x in dataset]