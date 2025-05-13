from ai.ai import OllamaAssistant

def main():
    assistant = OllamaAssistant()

    while True:
        query = input("Enter your question (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break

        print(assistant.handle_request(query)["ai_response"])


if __name__ == "__main__":
    main()


