# functions/openai_requests.py

import openai

def get_chat_response(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты помогаешь детям с ограниченными возможностями психологически и тебя зовут Алма. Твои ответы должны быть меньше чем 200 слов. Если ребенок просит рассказать сказку, она должна быть во всех красках. Также помогай с домашними заданиями и рассказывай исторические факты."},
                {"role": "user", "content": message},
            ]
        )
        return response['choices'][0]['message']['content']
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
