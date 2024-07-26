import openai
from functions.database import get_recent_messages

# Make sure to set up your OpenAI API key
openai.api_key = 'sk-proj-eecN1hd2PEneEI7OeNOIT3BlbkFJTVuG8hA9S0cP0IYcT7k1'

def get_chat_response(message_input):
    messages = get_recent_messages()
    user_message = {"role": "user", "content": message_input}
    messages.append(user_message)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        message_text = response.choices[0].message['content']
        return message_text
    except Exception as e:
        print(f"Error in get_chat_response: {e}")
        return None
