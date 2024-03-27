from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from claude_to_chatgpt.adapter import ClaudeAdapter
import os
from claude_to_chatgpt.logger import logger
from claude_to_chatgpt.models import models_list

CLAUDE_BASE_URL = os.getenv("CLAUDE_BASE_URL", "https://api.anthropic.com")
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
PORT = int(os.getenv("PORT", 8000))

logger.debug(f"claude_base_url: {CLAUDE_BASE_URL}")

adapter = ClaudeAdapter(CLADE_BASE_URL)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods, including OPTIONS
    allow_headers=["*"],
)

@app.api_route("/v1/chat/completions", methods=["POST"])
async def chat(request: Request):
    response = await adapter.chat(request)
    return JSONResponse(content=response)

@app.get("/v1/models")
async def models(request: Request):
    # Assuming models_list is a predefined list of available models.
    return JSONResponse(content={"object": "list", "data": models_list})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=PORT, log_level=LOG_LEVEL)
