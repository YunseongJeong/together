from enum import Enum
from typing import List
from string_function import check_keywords_in_string
import requests
from bs4 import BeautifulSoup
import os
from page_url_manager import AnnouncementPage

class Announcement:
    def __init__(self, title: str, content_html: str, content_text: str, notice_board_name: str, url: str, files: list):
        self.title = title
        self.url = url
        self.content_html = content_html
        self.content_text = content_text
        self.notice_board_name = notice_board_name
        self.files = files

def get_anns_url(announcementPage : AnnouncementPage) -> List[Announcement]:
    try:
        response = requests.get(announcementPage.page_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(e.strerror)
        
    soup = BeautifulSoup(response.text, 'html.parser')
    table_element = soup.find("tbody")
    span_tags = table_element.find_all("td", "_artclTdTitle")

    table = [tag for tag in span_tags]
    urls = []
    
    for line in table:
        # if check_keywords_in_string(line.getText(), ["대회", "공모전"]):
        element =line.find('a', class_='artclLinkView')
        if element:
            url = element['href']
        urls.append(announcementPage.default_url + url)
        
    return urls
    

def crawl_ann(url: str) -> Announcement:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(e)
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    base_url = response.url.split('/bbs/')[0]

    title_element = soup.find("h2", class_="artclViewTitle")
    title = title_element.get_text(strip=True) if title_element else "Title not found"

    # 텍스트 콘텐츠 추출
    content_text_element = soup.find('div', class_="artclView")
    content_text = content_text_element.get_text(strip=True) if content_text_element else "Content not found"

    # HTML 콘텐츠 추출
    content_html = str(content_text_element) if content_text_element else "Content not found"

    # 파일 다운로드
    inserts = soup.find_all('dd', class_="artclInsert")
    os.makedirs('downloads', exist_ok=True)
    files = []
    for insert in inserts:
        li_tags = insert.find_all("li")
        for li in li_tags:
            link_tag = li.find("a")
            if link_tag and 'download.do' in link_tag["href"]:
                file_url = link_tag["href"]
                if not file_url.startswith('http'):
                    file_url = base_url + file_url
                file_name = link_tag.get_text(strip=True)
                file_path = os.path.join('downloads', file_name)
                file_data = requests.get(file_url).content
                with open(file_path, 'wb') as f:
                    f.write(file_data)
                files.append(file_path)
                print(f'파일 다운로드 완료: {file_path}')  # 파일 다운로드 완료 메시지 출력

    return Announcement(
        title=title,
        url=url,
        notice_board_name="",
        content_html=content_html,
        content_text=content_text,
        files=files
    )



        

def crawl_anns(announcementPage : AnnouncementPage) :
    urls = get_anns_url(announcementPage)
    results = []
    for url in urls:
        temp = crawl_ann(url)
        if (temp != None):
            results.append(temp)
    return results