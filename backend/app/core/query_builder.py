ROLE_TOPICS = {
    "ai_ml": [
        "machine learning algorithms supervised unsupervised",
        "neural networks deep learning backpropagation",
        "model evaluation overfitting regularization",
        "natural language processing transformers",
        "feature engineering data preprocessing",
    ],
    "data_science": [
        "supervised learning classification regression",
        "data preprocessing feature engineering",
        "model evaluation cross validation metrics",
        "ensemble methods random forest boosting",
        "exploratory data analysis statistics",
    ],
}

ROLE_DISPLAY_NAMES = {
    "ai_ml": "AI/ML Engineer",
    "data_science": "Data Science / Applied ML",
}

def build_retrieval_query(role: str, skills: list[str]) -> str:
    role_key = "data_science" if "data" in role.lower() else "ai_ml"
    base_topics = ROLE_TOPICS.get(role_key, ROLE_TOPICS["ai_ml"])
    skill_context = " ".join(skills[:5]) if skills else ""
    query = f"{base_topics[0]} {skill_context}".strip()
    return query

def get_role_topics(role: str) -> list[str]:
    role_key = "data_science" if "data" in role.lower() else "ai_ml"
    return ROLE_TOPICS.get(role_key, ROLE_TOPICS["ai_ml"])