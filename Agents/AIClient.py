from google import genai

class AIClient:
    def __init__(self):
        print("Initializing AIClient")
        self.client = genai.Client(api_key="AIzaSyBIua6F8D_LmMWKmExIr1fEpvxkecAERL8")
        self.model = "gemini-3.5-flash-lite"
        self.chat = self.client.chats.create(model=self.model)
        print("Initialization complete")

    def send(self, message):
        interaction = self.chat.send_message(message)
        return interaction.text