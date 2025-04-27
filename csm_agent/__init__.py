from fastapi import FastAPI, Request, Form, Body
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os
import uvicorn
from typing import Dict

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# In-memory storage for messages (MVP)
messages = []

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "messages": messages})

@app.post("/message")
def receive_message(request: Request, customer_message: str = Form(...)):
    # Placeholder: Here the agent/LLM logic will go
    response = f"(Agent placeholder) Received: {customer_message}"
    messages.append({"from": "customer", "text": customer_message})
    messages.append({"from": "agent", "text": response})
    return RedirectResponse("/", status_code=303)

@app.get("/messages", response_class=JSONResponse)
def get_messages():
    return messages

@app.post("/messages", response_class=JSONResponse)
def post_message(payload: Dict = Body(...)):
    customer_message = payload.get("customer_message")
    if not customer_message:
        return JSONResponse({"error": "customer_message is required"}, status_code=400)
    messages.append({"from": "customer", "text": customer_message})
    # Placeholder agent response
    response = f"(Agent placeholder) Received: {customer_message}"
    messages.append({"from": "agent", "text": response})
    return messages

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()

