

def main():
    conversation = ConversationHistory()
    conversation.add_user_message("What methodology does the paper use?")
    conversation.add_assistant_message("The paper uses...")
    conversation.add_user_message("Why did the authors choose that?")
    conversation.add_assistant_message("The authors chose it because...")

    print(conversation.messages)    

class ConversationHistory:
    def __init__(self):
        self.messages = []

    def add_user_message(self,text):
        format_message = {
            "role": "user",
            "content": text
        }
        self.messages.append(format_message)
        return self.messages

    def add_assistant_message(self,text):
        format_message = {
            "role": "assistant",
            "content": text
        }
        self.messages.append(format_message)
        return self.messages

if __name__ == "__main__":
    main()