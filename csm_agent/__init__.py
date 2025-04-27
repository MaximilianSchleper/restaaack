from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os
import uvicorn

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

