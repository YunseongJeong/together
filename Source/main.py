from gpt_client import answer_gpt
from crawl_announcement import crawl_anns, Announcement
from selenium_test import WriteNoticeService
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    
    anns = crawl_anns("https://cse.pusan.ac.kr/cse/14651/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGY3NlJTJGMjYwNSUyRmFydGNsTGlzdC5kbyUzRmJic09wZW5XcmRTZXElM0QlMjZpc1ZpZXdNaW5lJTNEZmFsc2UlMjZzcmNoQ29sdW1uJTNEJTI2cGFnZSUzRDExJTI2c3JjaFdyZCUzRCUyNnJnc0JnbmRlU3RyJTNEJTI2YmJzQ2xTZXElM0QlMjZyZ3NFbmRkZVN0ciUzRCUyNg%3D%3D")
    
    announcements = []

    id = os.environ.get("PLATO_ID")
    pw = os.environ.get("PLATO_PW")
    course_name = "[테스트]"

    for ann in anns:
        print("\n\n\n\n")
        ann.content = answer_gpt(ann.get_content())
        announcements.append(ann)
        WriteNoticeService().write_notices(id, pw, course_name, announcements) 

if __name__ == "__main__":
    main()