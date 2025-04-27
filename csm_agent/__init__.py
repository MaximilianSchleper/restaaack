from pydantic import BaseModel
from restack_ai.agent import agent, log
from typing import List, Dict

class Message(BaseModel):
    from_: str
    text: str

@agent.defn()
class EchoAgent:
    def __init__(self) -> None:
        self.end = False
        self.messages: List[Message] = []

    @agent.event
    async def messages(self, messages_event: Dict) -> List[Message]:
        new_messages = [Message(**m) for m in messages_event.get("messages", [])]
        log.info(f"Received messages: {new_messages}")
        self.messages.extend(new_messages)
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

