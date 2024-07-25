# openai_requests.py
import openai
import logging

def get_chat_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the correct model name
            messages=[
                {"role": "system", "content": "Ты помогаешь детям с ограниченными возможностями психологически и тебя зовут Алма. Твои ответы должны быть меньше чем 200 слов. Если ребенок просит рассказать сказку, она должна быть во всех красках. Также помогай с домашними заданиями и рассказывай исторические факты."},
                {"role": "user", "content": user_input},
            ]
        )
        logging.info(f"OpenAI response: {response}")
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error in get_chat_response: {e}", exc_info=True)
        return None
