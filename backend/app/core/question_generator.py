from google import genai
from app.config import get_settings
from app.utils.exceptions import QuestionGenerationError
from app.utils.logger import logger
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from google.genai.errors import ServerError, ClientError #type: ignore

settings = get_settings()
client = genai.Client(api_key=settings.gemini_api_key)
print(settings.gemini_api_key[:10])
# @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=60, max=120),
    retry=retry_if_exception_type((ServerError, ClientError))
)
def generate_question(
    role: str,
    skills: list[str],
    context_chunks: list[dict],
    previous_questions: list[str] = [],
) -> str:
    try:
        # context_text = "\n\n".join([c["text"] for c in context_chunks])
        context_text = "\n\n".join(
            c["text"][:500]
            for c in context_chunks[:3]
        )
        skills_text = ", ".join(skills) if skills else "general skills"
        previous_text = "\n".join(previous_questions) if previous_questions else "None"
        
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


        logger.info(
            f"Chunks: {len(context_chunks)}, "
            f"Context chars: {len(context_text)}, "
            f"Previous questions: {len(previous_questions)}, "
            f"Prompt chars: {len(prompt)}"
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        question = response.text.strip()
        logger.info("question_generated", role=role)
        return question
        
    except Exception as e:
        raise QuestionGenerationError(str(e))
