import openai

openai.api_key = "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"

def get_chatbot_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are a helpful IT support assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content.strip()

