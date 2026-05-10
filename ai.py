import ollama
import pandas as pd 


history = []

while True:
    ask = input(">: ")
    response = ollama.chat(model="llama3.2:1b", messages=[{"role" : "user", "content": ask}])
    ai_response = response["message"]["content"]
    print(f"AI>{ai_response}")
    continue_1 = input("Do you want to continue(y/n): ")
    if continue_1 == "n":
        break
    else:
        ask = input(">: ")
        response = ollama.chat(model="llama3.2:1b", messages=[{"role" : "user", "content": ask}])
        ai_response = response["message"]["content"]
        print(f"AI>{ai_response}")

    memory = {
        "user" : "Umair",
        "question" : ask,
        "message" : ai_response,
    }

    history.append(memory)

df = pd.DataFrame(history)

df.to_csv("Ai history.csv")