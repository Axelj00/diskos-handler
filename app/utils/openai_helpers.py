import openai

def get_answer_from_openai(question: str, context: str, openai_api_key: str) -> str:
    openai.api_key = openai_api_key
    # You can prompt the model with your context
    messages = [
        {"role": "system", "content": "You are a helpful assistant specialized in analyzing well data."},
        {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.1
    )
    
    return response.choices[0].message.content.strip()
