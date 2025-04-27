from fastapi import FastAPI, Request, Form, Body
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from typing import Dict
from csm_agent import EchoAgent, Message

app = FastAPI()
templates = Jinja2Templates(directory="templates")
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
    await echo_agent.messages({"messages": [{"from_": "customer", "text": customer_message}]})
    return [m.dict() for m in echo_agent.messages]

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main() 