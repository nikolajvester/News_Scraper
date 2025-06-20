from transformers import pipeline
from transformers import AutoTokenizer
import warnings
from transformers.utils import logging as hf_logging

# Supressing max_length warnings as the token count is being set already
hf_logging.set_verbosity_error()
warnings.filterwarnings("ignore", message=".*max_length.*")

MODEL_NAME = "google/flan-t5-base"
DEVICE = -1
summarizer = pipeline("summarization", model=MODEL_NAME, tokenizer=MODEL_NAME, device=DEVICE, truncation=True)
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")

def summarize_text(text):
    word_count = len(text.split())
    if word_count < 50:
        print(f"🟡 Skipping summary (too short: {word_count} words)")
        return text
    
    tokenized = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    input_text = tokenizer.decode(tokenized["input_ids"][0], skip_special_tokens=True)

    max_tokens = min(200, int(word_count * 0.6))
    prompt = (
        "Summarize the following article critically and concisely. "
        "Avoid filler, focus only on key facts and implications:\n\n" + text
    )

    try:
        result = summarizer(prompt, max_new_tokens=max_tokens, do_sample=False)[0]
        summary = result.get("generated_text") or result.get("summary_text")
        return summary.strip() if summary else "[No summary returned]"
    except Exception as e:
        print(f"❌ Summarization failed: {e}")
        return "[Summarization error]"


MAX_INPUT_CHARS = 6000

def synthesize_summaries(summaries, model_name=None):
    """
    Generate a meta-summary from a list of summaries.
    Synthesizes insights, not just compression.
    """
    if not summaries:
        return None

    combined_text = "\n\n".join(summaries)
    truncated_text = combined_text[:MAX_INPUT_CHARS]

    prompt = (
        "You are an expert AI analyst. Analyze the following news summaries and identify:\n"
        "- Key themes or recurring trends\n"
        "- Product or technology developments\n"
        - "Social or political implications\n"
        "- Conflicts or market dynamics\n\n"
        "Do not list each summary. Write a coherent analysis that connects them:\n\n"
        + combined_text
    )

    result = summarizer(prompt, max_new_tokens=300, do_sample=False)
    return result[0]['generated_text']