from gpt_client import answer_gpt
from crawl_announcement import get_anns_url, crawl_ann_partial, crawl_ann
from selenium_service import WriteNoticeService
from dotenv import load_dotenv
import os
from duplicate_checker import is_recent_title_duplicate, save_title, truncate_text
from page_url_manager import PageUrlManager

def main():
    load_dotenv()
    page_url_manager = PageUrlManager()
    announcements = []

    id = os.environ.get("PLATO_ID")
    pw = os.environ.get("PLATO_PW")
    course_name = "[테스트]"

    for announcement_page in page_url_manager.announcement_pages:
        ann_urls = get_anns_url(announcement_page)  # 각 페이지에서 공지사항 URL 가져오기
        for url in ann_urls:
            # 제목만 부분적으로 크롤링
            partial_ann = crawl_ann_partial(url)
            if partial_ann:
                # 제목 중복 체크
                duplicate_check = is_recent_title_duplicate(partial_ann.title)
                print(f"중복 체크 결과: {duplicate_check} - {partial_ann.title}")
                if duplicate_check == "중복":
                    print("")
                    continue

                # 카테고리 분석을 위해 내용을 자름
                combined_text = f"{partial_ann.title}\n\n."
                truncated_content = truncate_text(combined_text, 15000)  # 토큰 수 제한
                category = answer_gpt(truncated_content)
                print(f"챗GPT 응답: {category} - {partial_ann.title}")

                if category in [
                    "[공모전] 공학/IT/SW",
                    "[공모전] 아이디어/기획",
                    "[공모전] 미술/디자인/건축",
                    "[공모전] 문학/수기/에세이",
                    "[공모전] 기타",
                    "교육/특강/프로그램",
                    "장학금",
                    "서포터즈",
                    "봉사활동",
                    "취업 정보" 
                ]:
                    # 전체 공지사항 크롤링
                    full_ann = crawl_ann(url)
                    full_ann.notice_board_name = category  # 게시판 이름 업데이트
                    announcements.append(full_ann)
                    save_title(partial_ann.title)  # 제목 저장
                    WriteNoticeService().write_notices(id, pw, course_name, [full_ann])  # 공지사항 작성
                    print(f"게시글 작성 완료\n")
                else:
                    print("")

if __name__ == "__main__":
    main()
