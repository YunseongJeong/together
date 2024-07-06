from openai import OpenAI


def answer_gpt(user_content):
    
    
    messages.append({"role" : "user", "content" : f"{user_content}"})

    response = chatgpt.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=False
    )
    
    messages.pop()
    
    assistant_content = response.choices[0].message.content

    return assistant_content


messages=[ #프로프팅 해야하는 코드
    {"role" : "system", "content" : "읽고 정리해서 출력해줘"} ] #role을 user에서 system 으로 바꿈

