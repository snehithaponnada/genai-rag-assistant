import json


def save_chat(question, answer):

    data = {
        "question": question,
        "answer": answer
    }

    try:

        with open("backend/docs.json", "r") as f:
            chats = json.load(f)

    except:

        chats = []

    chats.append(data)

    with open("backend/docs.json", "w") as f:
        json.dump(chats, f, indent=4)