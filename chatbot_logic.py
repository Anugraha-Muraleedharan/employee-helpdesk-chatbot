import openai

client = openai.OpenAI(api_key="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")

def get_chatbot_response(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if available
        messages=[
            {"role": "system", "content": "You are a helpful IT support assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content.strip()
