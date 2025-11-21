from fastapi import FastAPI
from pydantic import BaseModel

from .logic.fetcher import load_quiz_page
from .logic.parser import parse_quiz_page
from .logic.solver import solve_task

app = FastAPI()

MY_SECRET = "abc123"

class QuizRequest(BaseModel):
    email: str
    secret: str
    url: str

@app.post("/")
async def solve(body: QuizRequest):
    if body.secret != MY_SECRET:
        return {"error": "Forbidden: Invalid secret"}

    next_url = body.url
    final_answers = []

    for step in range(10):  # max 10 steps
        html = await load_quiz_page(next_url)
        parsed = parse_quiz_page(html)
        answer = solve_task(parsed)

        final_answers.append({
            "url": next_url,
            "answer": answer
        })

        submit_url = parsed.get("submit_url")
        if not submit_url:
            break  # quiz ends

        # Submit answer
        from server.utils.submit_utils import submit_answer
        response = submit_answer(
            submit_url,
            body.email,
            body.secret,
            next_url,
            answer
        )

        if not response.get("correct", True):
            # still within 3-minute window — stop chaining
            break

        next_url = response.get("url")
        if not next_url:
            break

    return {
        "message": "Quiz chain completed",
        "steps": final_answers
    }
