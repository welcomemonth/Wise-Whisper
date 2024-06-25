from openai import OpenAI
import requests

llm = OpenAI(
    # base_url = 'http://localhost:11434/v1',
    # base_url='https://llm.meetmonth.top/v1',
    # base_url='https://api.openai.com/v1',
    base_url='https://macaw-pleasing-jawfish.ngrok-free.app/v1',
    api_key='ollama'  # required, but unused
)


# 通过GET /api/tags获取本地模型接口列表
def get_model_list():
    base_url = 'https://macaw-pleasing-jawfish.ngrok-free.app/api/tags'
    # 发送 GET 请求以获取模型列表
    response = requests.get(base_url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 解析响应的 JSON 数据
        models = response.json()['models']
        models_list = [model['name'] for model in models]
        return models_list
    else:
        print(f"无法获取模型列表，HTTP 状态码：{response.status_code}")
        return []


# 对大语言模型回复接口进行再次封装，只需要用户传递聊天内容
def ask(messages, model='llama2:13b', **kwargs):
    # print(kwargs)
    return llm.chat.completions.create(
        model=model,
        messages=messages,
        **kwargs
    )


# 测试大语言模型是否可用，不可用返回False
def test_llm_availability():
    try:
        # response = llm.models.list()
        return True
    except Exception as e:
        print(f"无法连接到大语言模型，错误信息：{e}")
        return False


if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The LA Dodgers won in 2020."},
        {"role": "user", "content": "给我讲一个冷笑话"}
    ]
    res = ask(messages, stream=False)

    # for index, chunk in enumerate(res):
    #     if index == 0:
    #         print(chunk)
    # ChatCompletionChunk(id='chatcmpl-263', choices=[Choice(delta=ChoiceDelta(content='OK', function_call=None, role='assistant', tool_calls=None), finish_reason=None, index=0, logprobs=None)], created=1719298104, model='llama2:13b', object='chat.completion.chunk', service_tier=None, system_fingerprint='fp_ollama', usage=None)
    #     print(chunk.choices[0].delta.content, end="")
    # )
    print(res)
    # ChatCompletion(id='chatcmpl-376', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content="Okay! Here's a cold one for you:\n\nWhy did the tomato turn down the date with the avocado?\n\nBecause it was a fruit-less relationship! 😜", role='assistant', function_call=None, tool_calls=None))], created=1719298206, model='llama2:13b', object='chat.completion', service_tier=None, system_fingerprint='fp_ollama', usage=CompletionUsage(completion_tokens=47, prompt_tokens=0, total_tokens=47))
    # print(response.choices[0].message.content)













