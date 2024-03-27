from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from claude_to_chatgpt.adapter import ClaudeAdapter
import json
import os
from claude_to_chatgpt.logger import logger

# 环境变量和日志配置保持不变

adapter = ClaudeAdapter(CLADE_BASE_URL)

app = FastAPI()

# CORS中间件配置保持不变

@app.api_route("/v1/chat/completions", methods=["POST"])
async def chat(request: Request):
    response = await adapter.chat(request)
    return JSONResponse(content=response)

# 其他路由和模型列表接口保持不变

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=PORT, log_level=LOG_LEVEL)
