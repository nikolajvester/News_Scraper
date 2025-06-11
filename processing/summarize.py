from transformers import pipeline

MODEL_NAME = "google/flan-t5-base"
DEVICE = -1
MAX_LENGTH = 350
MIN_LENGTH = 50

# Load the summarization model once
summarizer = pipeline("summarization", model=MODEL_NAME, tokenizer=MODEL_NAME, device=DEVICE)

def summarize_text(text):
    word_count = len(text.split())

    if word_count < 50:
        print(f"🟡 Skipping summary (too short: {word_count} words)")
        return text

    prompt = f"Summarize the following article critically and concisely. Avoid filler, focus only on key facts and implications:\n{text}"
    result = summarizer(prompt, max_new_tokens=150, do_sample=False)
    return result[0]["summary_text"]