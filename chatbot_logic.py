import ollama

def get_chatbot_response(user_input):
    try:
        response = ollama.chat(
            model="gemma:2b",
            messages=[
                {"role": "system", "content": "You are an IT support assistant. Keep responses short and helpful."},
                {"role": "user", "content": user_input}
            ],
            stream=False
        )
        return response["message"]["content"]
    except Exception as e:
        return f"Error: {e}"
