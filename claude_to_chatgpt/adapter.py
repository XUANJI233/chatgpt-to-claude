import httpx
import time
import json
import os
from fastapi import Request
from claude_to_chatgpt.util import num_tokens_from_string
from claude_to_chatgpt.logger import logger
from claude_to_chatgpt.models import model_map

class ClaudeAdapter:
    def __init__(self, claude_base_url="https://api.anthropic.com"):
        self.claude_api_key = os.getenv("CLAUDE_API_KEY", None)
        self.claude_base_url = claude_base_url

    def get_api_key(self, headers):
        auth_header = headers.get("authorization", None)
        if auth_header:
            return auth_header.split(" ")[1]
        else:
            return self.claude_api_key

    def convert_messages_to_prompt(self, messages):
        prompt = "\n\nHuman: "  # 开始时添加Human标签
        for message in messages:
            content = message["content"]
            prompt += f"{content}\n\n"  # 对于每个消息，加上内容后换两行
        prompt += "Assistant: "  # 结束时添加Assistant标签，等待回复
        return prompt

    def chatgpt_to_claude_params(self, chatgpt_params):
        model = model_map.get(chatgpt_params["model"], "claude-3-sonnet-20240229")  # 默认模型
        messages = chatgpt_params["messages"]
        prompt = self.convert_messages_to_prompt(messages)

        claude_params = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],  # 将整个对话作为单一消息发送
            "max_tokens": chatgpt_params.get("max_tokens", 1024),
        }

        return claude_params

    async def chat(self, request: Request):
        chatgpt_params = await request.json()
        claude_params = self.chatgpt_to_claude_params(chatgpt_params)
        api_key = self.get_api_key(request.headers)

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.claude_base_url}/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "accept": "application/json",
                    "content-type": "application/json",
                    "anthropic-version": "2023-06-01",
                },
                json=claude_params,
            )
            if response.is_error:
                raise Exception(f"Error: {response.status_code}")
            claude_response = response.json()
            return claude_response  # 直接返回Claude的响应，或者根据需要进行格式化
