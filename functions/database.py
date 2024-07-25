import json
import random

def get_recent_messages():
    file_name = "stored_data.json"
    learn_instruction = {
        "role": "system",
        "content": "Ты помогаешь детям с ограниченными возможностями психологически и тебя зовут Алма. Твои ответы должны быть меньше чем 200 слов. Если ребенок просит рассказать сказку, она должна быть во всех красках. Также помогай с домашними заданиями и рассказывай исторические факты."
    }
    
    messages = []
    x = random.uniform(0, 1)
    if x < 0.2:
        learn_instruction["content"] += " Твои слова должны ободрять ребенка"
    elif x < 0.5:
        learn_instruction["content"] += " Твои ответы должны быть не высокоинтеллектуальные и легкими поучительными"
    else:
        learn_instruction["content"] += " Ты можешь предлагать ребенку игры чтобы он играл в них в жизни"
    
    messages.append(learn_instruction)

    try:
        with open(file_name) as user_file:
            data = json.load(user_file)
            if data:
                messages.extend(data[-5:])
    except Exception as e:
        print(f"Error reading stored messages: {e}")
    
    return messages

def store_messages(request_message, response_message):
    file_name = "stored_data.json"
    messages = get_recent_messages()[1:]
    
    user_message = {"role": "user", "content": request_message}
    assistant_message = {"role": "assistant", "content": response_message}
    messages.extend([user_message, assistant_message])
    
    try:
        with open(file_name, "w") as f:
            json.dump(messages, f)
    except Exception as e:
        print(f"Error storing messages: {e}")

def reset_messages():
    file_name = "stored_data.json"
    try:
        open(file_name, "w").close()
    except Exception as e:
        print(f"Error resetting messages: {e}")
