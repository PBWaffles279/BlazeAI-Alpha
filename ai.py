from ollama import chat


# Configuration


MODEL = "qwen3:1.7b"

THINKING = False
USE_PERSONALITY = False



# Load Personality


if USE_PERSONALITY:
    with open("personality.txt", "r", encoding="utf-8") as file:
        personality = file.read()
else:
    personality = ""



# Conversation


conversation = [
    {
        "role": "system",
        "content": personality
    }
]



# Chat Loop


while True:
    message = input("\nYou: ")

    if message.lower() == "quit":
        break

    conversation.append({
        "role": "user",
        "content": message
    })


    print("\n🧠 Blaze is thinking...\n")

    response = chat(
        model=MODEL,
        messages=conversation,
        think=THINKING,
        stream=True
    )

    thinking = ""
    answer = ""
    in_thinking = False

    for chunk in response:

        if chunk.message.thinking:
            if not in_thinking:
                in_thinking = True

            thinking += chunk.message.thinking

            if THINKING:
                print(chunk.message.thinking, end="", flush=True)

        elif chunk.message.content:
            if in_thinking and THINKING:
                print("\n\n💬 Blaze:\n", end="", flush=True)
                in_thinking = False

            answer += chunk.message.content
            print(chunk.message.content, end="", flush=True)

    print()

    conversation.append({
        "role": "assistant",
        "content": answer
    })
