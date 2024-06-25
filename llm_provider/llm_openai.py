from openai import OpenAI

llm = OpenAI(
    # base_url = 'http://localhost:11434/v1',
    # base_url='https://llm.meetmonth.top/v1',
    # base_url='https://api.openai.com/v1',
    base_url='https://macaw-pleasing-jawfish.ngrok-free.app/v1',
    api_key='ollama', # required, but unused
)


if __name__ == "__main__":
    response = llm.chat.completions.create(
      model="llama2:13b",
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The LA Dodgers won in 2020."},
        {"role": "user", "content": "给我讲一个冷笑话"}
      ]
    )
    print(response.choices[0].message.content)













