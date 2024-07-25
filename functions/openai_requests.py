import openai

openai.organization = "your_openai_organization_id"
openai.api_key = "your_openai_api_key"

try:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты помогаешь детям с ограниченными возможностями психологически и тебя зовут Алма. Твои ответы должны быть меньше чем 200 слов. Если ребенок просит рассказать сказку, она должна быть во всех красках. Также помогай с домашними заданиями и рассказывай исторические факты."},
            {"role": "user", "content": "Привет, Алма!"},
        ]
    )
    print(response['choices'][0]['message']['content'])
except openai.error.OpenAIError as e:
    print(f"OpenAI API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
