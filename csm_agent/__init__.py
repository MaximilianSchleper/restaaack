from fastapi import FastAPI, Request, Form, Body
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from typing import Dict, List
from pydantic import BaseModel
from restack_ai.agent import NonRetryableError, agent, import_functions, log
from datetime import timedelta

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Placeholder Message and LlmChatInput
class Message(BaseModel):
    from_: str
    text: str

class LlmChatInput(BaseModel):
    messages: List[Message]

# Agent definition
@agent.defn()
class EchoAgent:
    def __init__(self) -> None:
        self.end = False
        self.messages: List[Message] = []

    @agent.event
    async def messages(self, messages_event: Dict) -> List[Message]:
        # Expecting {"messages": [Message]}
        new_messages = [Message(**m) for m in messages_event.get("messages", [])]
        log.info(f"Received messages: {new_messages}")
        self.messages.extend(new_messages)
        # Echo last message
        if new_messages:
            echo = Message(from_="agent", text=new_messages[-1].text)
            self.messages.append(echo)
        return self.messages

    @agent.event
    async def end(self, end: Dict) -> Dict:
        log.info("Received end")
        self.end = True
        return end

    @agent.run
    async def run(self, function_input: dict) -> None:
        log.info("EchoAgent function_input", function_input=function_input)
        await agent.condition(lambda: self.end)

echo_agent = EchoAgent()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "messages": [m.dict() for m in echo_agent.messages]})

@app.get("/messages", response_class=JSONResponse)
def get_messages():
    return [m.dict() for m in echo_agent.messages]

@app.post("/messages", response_class=JSONResponse)
async def post_message(payload: Dict = Body(...)):
    customer_message = payload.get("customer_message")
    if not customer_message:
        return JSONResponse({"error": "customer_message is required"}, status_code=400)
    # Send to agent
    await echo_agent.messages({"messages": [{"from_": "customer", "text": customer_message}]})
    return [m.dict() for m in echo_agent.messages]

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()

