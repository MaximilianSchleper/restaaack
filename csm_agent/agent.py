from datetime import timedelta
from pydantic import BaseModel
from restack_ai.agent import NonRetryableError, agent, log
from typing import List

class Message(BaseModel):
    from_: str
    text: str

class MessagesEvent(BaseModel):
    messages: List[Message]

class EndEvent(BaseModel):
    end: bool

@agent.defn()
class AgentChat:
    def __init__(self) -> None:
        self.end = False
        self.messages: List[Message] = []

    @agent.event
    async def messages(self, messages_event: MessagesEvent) -> List[Message]:
        log.info(f"Received messages: {messages_event.messages}")
        self.messages.extend(messages_event.messages)
        # Echo last message
        if messages_event.messages:
            echo = Message(from_="agent", text=messages_event.messages[-1].text)
            self.messages.append(echo)
        return self.messages

    @agent.event
    async def end(self, end: EndEvent) -> EndEvent:
        log.info("Received end")
        self.end = True
        return end

    @agent.run
    async def run(self, function_input: dict) -> None:
        log.info("AgentChat function_input", function_input=function_input)
        await agent.condition(lambda: self.end) 