from gpt_client import answer_gpt
from crawl_announcement import get_anns_url, crawl_ann_partial, crawl_ann
from selenium_service import WriteNoticeService
from dotenv import load_dotenv
import os
from duplicate_checker import is_recent_title_duplicate, save_title, truncate_text
from page_url_manager import PageUrlManager

# 사전 정의된 키워드와 카테고리 매핑
KEYWORD_CATEGORIES = {
    "장학금": "장학금",
    "장학생": "장학금",
    "지원금": "장학금",
    "인턴": "취업 정보",
    "일자리": "취업 정보",
    "공개모집": "취업 정보",
    "채용": "취업 정보",
    "공채": "취업 정보",
    "현장실습": "취업 정보"
}

# 제외할 키워드
EXCLUDE_KEYWORDS = ["대출", "재입학", "진학", "조교", "수강 신청", "수강신청", "수강 지도", "수강지도", "취소", "연기", "변경"]


def categorize_by_keywords(title, content_text):
    """
    제목과 내용에서 키워드를 검색하여 게시판을 직접 분류
    키워드가 매핑된 카테고리가 있는 경우 해당 카테고리로 분류하고, 그렇지 않으면 None 반환
    """
    for keyword in EXCLUDE_KEYWORDS:
        if keyword in title:
            return "해당없음"  # 제외할 키워드가 포함된 경우 '해당없음'으로 바로 반환

    for keyword, category in KEYWORD_CATEGORIES.items():
        if keyword in title:
            return category

    return None


def categorize_announcement(title, content_text):
    # 먼저 키워드를 기반으로 카테고리 분류 시도
    category = categorize_by_keywords(title, content_text)

    if category:
        return category
    else:
        # 사전 정의된 키워드로 분류되지 않으면 ChatGPT를 통해 카테고리 분류
        combined_text = f"{title}\n{content_text}"
        truncated_content = truncate_text(combined_text, 1000)  # 토큰 수 제한(1000토큰 = 약 500자)
        return answer_gpt(truncated_content)


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

                # 키워드 기반 카테고리 분류 시도
                category = categorize_announcement(partial_ann.title, partial_ann.content_text)
                print(f"카테고리 분류 결과: {category} - {partial_ann.title}")

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
