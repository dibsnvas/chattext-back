import openai
from functions.database import get_recent_messages

def get_chat_response(message_input):
    messages = get_recent_messages()
    user_message = {"role": "user", "content": message_input}
    messages.append(user_message)

    try:
        def chat_gpt(prompt):
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            return response

        response = chat_gpt(messages)
        message_text = response.choices[0].message.content
        return message_text
    except Exception as e:
        print(f"Error in get_chat_response: {e}")
        return None
