from google import genai
from google.genai.errors import ServerError, ClientError
from app.config import get_settings
from app.utils.exceptions import QuestionGenerationError
from app.utils.logger import logger

settings = get_settings()
client = genai.Client(api_key=settings.gemini_api_key)

MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
]

def generate_question(
    role: str,
    skills: list[str],
    context_chunks: list[dict],
    previous_questions: list[str] = [],
) -> str:
    context_text = "\n\n".join(c["text"][:500] for c in context_chunks[:3])
    skills_text = ", ".join(skills) if skills else "general skills"
    previous_text = "\n".join(previous_questions) if previous_questions else "None"

    logger.info("Chunks: %d, Context chars: %d, Previous questions: %d, Prompt chars: %d" % (
        len(context_chunks[:3]),
        len(context_text),
        len(previous_questions),
        len(context_text) + len(skills_text) + len(previous_text)
    ))

    prompt = f"""You are conducting a technical interview for a {role} position.

Candidate skills: {skills_text}

Knowledge base context:
{context_text}

Previously asked questions:
{previous_text}

Generate exactly one specific, non-generic technical interview question that:
- Is grounded in the knowledge base context above
- Is relevant to the candidate's background
- Has not been asked before
- Tests conceptual or applied understanding
- Is concise and clear

Return only the question, nothing else."""

    last_error = None
    for model in MODELS:
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )
            logger.info(f"question_generated_{len(previous_questions)+1}", role=role, model=model)
            return response.text.strip()
        except (ServerError, ClientError) as e:
            logger.warning("model_failed", model=model, error=str(e))
            last_error = e
            continue

    raise QuestionGenerationError(str(last_error))