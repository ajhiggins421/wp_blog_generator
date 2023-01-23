from revChatGPT.ChatGPT import Chatbot


class ChatGPT:

    def __init__(self, token):
        self.bot = Chatbot(
            {
                "session_token": token
            }, conversation_id=None, parent_id=None)  # You can start a custom conversation

    def get_response(self, prompt):
        answer = self.bot.ask(prompt, conversation_id=None, parent_id=None)
        return answer['message']

