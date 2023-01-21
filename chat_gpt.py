from revChatGPT.ChatGPT import Chatbot


# You can specify custom conversation and parent ids. Otherwise it uses the saved conversation (yes. conversations
# are automatically saved)

# {
#   "message": message,
#   "conversation_id": self.conversation_id,
#   "parent_id": self.parent_id,
# }

class ChatGPT:

    def __init__(self, token):
        self.bot = Chatbot(
            {
                "session_token": token
            }, conversation_id=None, parent_id=None)  # You can start a custom conversation

    def get_response(self, prompt):
        answer = self.bot.ask(prompt, conversation_id=None, parent_id=None)
        print(answer)
        return answer['message']

