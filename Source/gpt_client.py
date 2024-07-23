from openai import OpenAI
import os




def answer_gpt(user_content):
    chatgpt = OpenAI(api_key=os.environ.get('GPT_API_KEY'))
    
    messages.append({"role" : "user", "content" : f"{user_content}"})

    response = chatgpt.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=False
    )
    
    messages.pop()
    
    assistant_content = response.choices[0].message.content

    return assistant_content


messages=[
    {"role" : "system", "content" : '''
     너는 내가 제공하는 공지사항을 정리해줘야한다

다음은 json 형식의 예시이다:
{{
  "content": "정리된 내용",
  "category": "Category 중 하나"
}}

enum Category:
    "[공모전] 공학/IT/SW"
    "[공모전] 아이디어/기획"
    "[공모전] 미술/디자인/건축"
    "[공모전] 사진/영상/UCC"
    "[공모전] 문학/수기/에세이"
    "[공모전] 기타"

결과는 json 형식이어야 한다.
     '''} ] #role을 user에서 system 으로 바꿈

