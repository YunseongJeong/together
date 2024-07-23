from gpt_client import answer_gpt
from crawl_announcement import crawl_anns, Announcement
from selenium_service import WriteNoticeService
from dotenv import load_dotenv
import os
import json
from page_url_manager import AnnouncementPage, PageUrlManager

def main():
    load_dotenv()
    page_url_manager = PageUrlManager()
    anns = []
    for announcemnt in page_url_manager.announcement_pages:
        anns += crawl_anns(announcemnt)
    
    announcements = []

    id = os.environ.get("PLATO_ID")
    pw = os.environ.get("PLATO_PW")
    course_name = "[테스트]"

    for ann in anns:
        print("\n\n\n\n")
        try:
            answer = answer_gpt(ann.get_content())
            data = json.loads(answer)
        except:
            continue
        print(answer)
        
        ann.notice_board_name = data["category"]
        ann.content = data["content"]
        announcements.append(ann)
    WriteNoticeService().write_notices(id, pw, course_name, announcements) 

if __name__ == "__main__":
    main()