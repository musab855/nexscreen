from google import genai
from app.config import get_settings
from app.utils.logger import logger
from google.genai.errors import ServerError, ClientError #type: ignore
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


settings = get_settings()
client = genai.Client(api_key=settings.gemini_api_key)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=5, max=30),
    retry=retry_if_exception_type((ServerError, ClientError))
)
def generate_report(role: str, skills: list[str], qa_pairs: list[dict]) -> dict:
    qa_text = ""
    # for i, pair in enumerate(qa_pairs):
    #     qa_text += f"Q{i+1}: {pair['question']}\nA{i+1}: {pair['answer']}\n\n"

    qa_text = ""
    for i, pair in enumerate(qa_pairs[:5]):
        q = pair['question'][:300]
        a = pair['answer'][:300]
        qa_text += f"Q{i+1}: {q}\nA{i+1}: {a}\n\n"

    prompt = f"""You evaluated a technical interview for a {role} position.

Candidate skills: {", ".join(skills)}

Interview transcript:
{qa_text}

Provide a structured evaluation in the following JSON format only, no markdown:
{{
    "overall_summary": "2-3 sentence summary of candidate performance",
    "strengths": ["strength1", "strength2"],
    "areas_for_improvement": ["area1", "area2"],
    "technical_score": <integer 1-10>,
    "recommendation": "hire" or "consider" or "reject"
}}"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    import json
    raw = response.text.strip().replace("```json", "").replace("```", "")
    insights = json.loads(raw)
    summary = insights.get("overall_summary", "")
    logger.info("report_generated", role=role)
    return {"summary_text": summary, "insights": insights}

