from chat import chatbot_query_engine, question_answer

def chat_with_bot(query_engine):
    print("Hey! How can I help you?")
    
    conversation_history = []
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'exit':
            print("Bot: Bye, Remember me)")
            break
        
        response = question_answer(query_engine, user_input, conversation_history)
        print(f"Bot: {response}\n")

def main():
    
    # Setup engine
    query_engine = chatbot_query_engine()
    
    # Start chat interface
    chat_with_bot(query_engine)

if __name__ == "__main__":
    main()