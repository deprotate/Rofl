from fastapi import FastAPI, HTTPException
import json
from model import generateTask

app = FastAPI()

@app.get("/generate/")
async def generate(theme: str):
    """
    Endpoint to generate a task based on the provided theme.

    Query Parameters:
    - theme: str - The theme for which to generate the task.

    Returns:
    - JSON response with an 'answer' field containing the generated text.
    """
    try:
        # Generate the task using the model
        result = generateTask(theme, "dataset.json")
        # Convert the result to a JSON-formatted string
        answer_text = json.dumps(result, indent=2, ensure_ascii=False)
        return {"answer": answer_text}
    except Exception as e:
        # Return HTTP 500 with error details on failure
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Run the app on 0.0.0.0:8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
  
