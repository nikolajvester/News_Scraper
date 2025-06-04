from transformers import pipeline

# Load the summarization model once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text):
    if len(text.split()) < 50:
        return text  # skip very short content

    summary = summarizer(
        text,
        max_length=100,
        min_length=30,
        do_sample=False
    )
    return summary[0]["summary_text"]
