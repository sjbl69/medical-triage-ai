from transformers import pipeline

model_path = "./models/dpo-model"

pipe = pipeline(
    "text-generation",
    model=model_path,
    tokenizer=model_path
)

tests = [
    "Patient: J'ai une douleur à la poitrine\nDoctor:",
    "Patient: J'ai mal à la tête\nDoctor:",
    "Patient: Je saigne beaucoup\nDoctor:"
]

for t in tests:
    print("\nQUESTION:", t)

    result = pipe(
        t,
        max_new_tokens=40,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        repetition_penalty=1.2
    )[0]["generated_text"]

    print("RÉPONSE:", result.replace(t, ""))
    print("-" * 50)