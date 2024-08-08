from openai import OpenAI
import os

def answer_gpt(user_content):
    chatgpt = OpenAI(api_key=os.environ.get('GPT_API_KEY'))
    
    messages = [
        {"role": "system", "content": (
                "Categorize the following text into the appropriate category and only state the category.\n"
                "If the text contains keywords like '대회' or '공모전' categorize it under one of the [Competition/Contest] categories\n"
                "If it matches any of the keywords from the above categories such as 장학, 서포터즈, 봉사, 취업, etc., categorize it accordingly.\n\n"
                "[Competition/Contest] Engineering/Information Technology/Software =([공모전] 공학/IT/SW)\n"
                "[Competition/Contest] Ideas/Planning =([공모전] 아이디어/기획)\n"
                "[Competition/Contest] Art/Design/Architecture =([공모전] 미술/디자인/건축)\n"
                "[Competition/Contest] Literature/Personal Narrative/Essay =([공모전] 문학/수기/에세이)\n"
                "[Competition/Contest] Miscellaneous (for contests not clearly falling into other categories or if uncertain) =([공모전] 기타)\n"
                "Education/Lecture/Program =(교육/특강/프로그램)\n"
                "Scholarship/Scholar (only those awarded, including work-study students) =(장학금)\n"
                "Supporters/Ambassadors =(서포터즈)\n"
                "Volunteer Work =(봉사활동)\n"
                "Employment Information (only company hiring, excluding graduate school, dormitories, etc.) =(취업 정보)\n"
                "If it does not fall under any category, respond with 'Not Applicable =(해당없음)'.\n\n"
                "The output must be one of the following: [공모전] 공학/IT/SW,\n"
                "[공모전] 아이디어/기획,\n"
                "[공모전] 미술/디자인/건축,\n"
                "[공모전] 문학/수기/에세이,\n"
                "[공모전] 기타,\n"
                "교육/특강/프로그램,\n"
                "장학금,\n"
                "서포터즈,\n"
                "봉사활동,\n"
                "취업 정보,\n"
                "or 해당없음. Never change or add to the result text. The output must be in Korean.\n"
                "Do not use quotation marks. Never say anything else."
            )
        },
        {"role": "user", "content": user_content}
    ]

    response = chatgpt.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    assistant_content = response.choices[0].message.content

    return assistant_content

def check_title_similarity(new_title, recent_titles):
    chatgpt = OpenAI(api_key=os.environ.get('GPT_API_KEY'))
    
    system_message = {
        "role": "system",
        "content": (
            "Judge whether the following new title is a duplicate of any of the recent titles. "
            "If the new title is the same or very similar to any of the recent titles, output '중복'. "
            "Consider minor differences in wording, punctuation, or formatting as duplicates if the main content is the same. "
            "If the new title conveys a different meaning or content compared to recent titles, output '중복 아님'. "
            "The output must be in Korean. Do not use quotation marks. Never say anything else."
        )
    }

    user_message = {
        "role": "user",
        "content": f"새로운 제목: {new_title}\n최근 제목들: " + "\n".join(recent_titles)
    }

    messages = [system_message, user_message]

    response = chatgpt.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    assistant_content = response.choices[0].message.content

    return assistant_content
