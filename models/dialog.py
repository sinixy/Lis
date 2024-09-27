from datetime import datetime, timedelta


class Message:

    def __init__(self, content: str, role: str, dt: datetime = datetime.now()):
        self.content = content
        self.role = role
        self.dt = dt

    def to_dict(self):
        return {
            'role': self.role,
            'content': self.content
        }
    
class Dialog:

    def __init__(self, messages: list[Message] = []):
        self.messages = messages

    def add(self, content: str, role: str):
        self.messages.append(Message(content, role))

    def pop(self) -> Message:
        return self.messages.pop()

    def prune(self, older_than: timedelta = timedelta(hours=24)):
        self.messages = [msg for msg in self.messages if msg.dt > datetime.now() - older_than]

    def to_list(self) -> list[dict]:
        return [msg.to_dict() for msg in self.messages]
    
    def to_text(self, user_name: str = 'user', assistant_name: str = 'assistant') -> str:
        text = ''
        role_to_name = {'user': user_name, 'assistant': assistant_name}
        for m in self.messages:
            text += f'[{m.dt.isoformat(timespec="seconds")}] {role_to_name[m.role]}: {m.content}\n'
        print('========\n', text, '========\n')
        return text