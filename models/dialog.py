from datetime import datetime, timedelta

from db import db
import asyncio


class Message:

    def __init__(self, id: int, content: str, role: str, dt: datetime = None):
        self.id = id
        self.content = content
        self.role = role
        self.dt = dt if dt else datetime.now()

    def to_dict(self, bson: bool = False):
        d = {
            'id': self.id,
            'dt': self.dt,
            'content': self.content,
            'role': self.role
        }
        if bson:
            d.pop('id')
            d['_id'] = self.id
        return d

    def to_llm_dict(self):
        return {
            'role': self.role,
            'content': self.content
        }
    
class Dialog:

    def __init__(self, messages: list[Message] = []):
        self.messages = messages

    def add(self, id: int, content: str, role: str, write: bool = True):
        msg = Message(id, content, role)
        self.messages.append(msg)
        if write:
            asyncio.ensure_future(db.dialog.insert_one(msg.to_dict(bson=True)))

    def pop(self) -> Message:
        return self.messages.pop()

    def prune(self, older_than: timedelta = timedelta(hours=24)):
        self.messages = [msg for msg in self.messages if msg.dt > datetime.now() - older_than]

    @classmethod
    async def load_dialog(cls, newer_than: timedelta = timedelta(hours=24)):
        dialog = cls()
        async for msg in db.dialog.find({'dt': {'$gt': datetime.now() - newer_than}}):
            dialog.messages.append(Message(msg['_id'], msg['content'], msg['role'], msg['dt']))
        return dialog

    def to_llm_list(self) -> list[dict]:
        return [msg.to_llm_dict() for msg in self.messages]
    
    def to_llm_text(self, user_name: str = 'user', assistant_name: str = 'assistant', system_name: str = 'system') -> str:
        text = ''
        role_to_name = {'user': user_name, 'assistant': assistant_name, 'system': system_name}
        for m in self.messages:
            text += f'[{m.dt.isoformat(timespec="seconds")}] {role_to_name[m.role]}: {m.content}\n'
        # print('========\n', text, '========\n')
        return text