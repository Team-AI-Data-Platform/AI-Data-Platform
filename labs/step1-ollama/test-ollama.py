from ollama import chat

response = chat(
    model='gemma3:4b',
    messages=[
        {
            'role': 'user',
            'content': 'Local LLM이 무엇인지 설명해줘'
        }
    ]
)

print(response['message']['content'])