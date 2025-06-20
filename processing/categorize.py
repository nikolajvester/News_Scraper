from transformers import pipeline

# Label set
CANDIDATE_LABELS = [
    # Tech & AI
    "Artificial Intelligence", "Machine Learning", "AI Ethics", "AI Policy",
    "Big Tech", "Startups", "Software Development", "Hardware",

    # Industry
    "Finance", "Healthcare", "Education", "Media", "Gaming", "Transportation",

    # Society
    "Politics", "Privacy", "Security", "Surveillance", "Law", "Ethics",
    "Labor", "Workforce", "Social Media", "Misinformation",

    # Consumer & Product
    "Product Launches", "Gadgets", "Smartphones", "Cloud Services",
    "User Experience", "Data & Analytics", "Enterprise Tech",

    # Environment & Innovation
    "Climate", "Sustainability", "Energy", "Infrastructure",
    "Science", "Research", "Innovation", "Regulation",

    # Meta/Editorial
    "Opinion", "Feature", "Analysis", "Trend",

    # Geo
    "China", "Europe", "US", "Global Tech", "DK"
]

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def categorize_text(text, labels=CANDIDATE_LABELS, threshold=0.3, top_n=3):
    """
    Classify text into primary and secondary categories using zero-shot learning.
    Returns:
        primary_category: str
        secondary_categories: list[str]
    """
    if not text or len(text.strip()) < 20:
        return "Uncategorized", []

    result = classifier(text, labels, multi_label=True)

    # Sort by score descending
    scored = sorted(zip(result['labels'], result['scores']), key=lambda x: x[1], reverse=True)

    primary = scored[0][0] if scored else "Uncategorized"
    secondary = [label for label, score in scored[1:top_n+1] if score >= threshold]

    return primary, secondary
