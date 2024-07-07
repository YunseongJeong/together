from gpt_client import answer_gpt
from crawl_announcement import crawl_anns, Announcement, AnnouncementPages
from selenium_test import WriteNoticeService
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    
    anns = crawl_anns(AnnouncementPages.naoe.value)
    
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