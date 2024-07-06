from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from typing import List
from crawl_announcement import Announcement

class WriteNoticeService:
    def __init__(self) :
        chrome_driver_path = './Source/chromedriver'


        options = webdriver.ChromeOptions()

        options.add_argument('headless')
        options.add_argument("no-sandbox")

        options.add_argument('window-size=1920x1080')

        options.add_argument("disable-gpu")  
        options.add_argument("lang=ko_KR") 
        options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')

        driver_service = Service(chrome_driver_path)
        self.driver = webdriver.Chrome(service=driver_service, options=options)
        self.driver.get('https://plato.pusan.ac.kr/')
    
    def write_notices(self, id:str, pw:str, course_name:str, announcements : List[Announcement]):
        
        self.login(id, pw)
        self.move_to_course(course_name)
        self.move_to_notice_board("공모전/ 공대")
        for announcement in announcements:
            self.write_notice_in_board(announcement.title, announcement.content)
        
    def login(self, id : str, pw : str):
        username_input = self.driver.find_element('id', 'input-username')
        username_input.send_keys(id)

        password_input = self.driver.find_element("id", "input-password")
        password_input.send_keys(pw)

        submit = self.driver.find_element("name", "loginbutton")
        submit.click()

    def move_to_course(self, course_name : str):
        course_link = self.driver.find_element(By.XPATH, '//h3[text()="'+ course_name +'"]/ancestor::a')
        course_link.click()

    def move_to_notice_board(self, notice_board_name:str):
        notice_board_link = self.driver.find_element(By.XPATH, '//a[contains(span[@class="instancename"], "' + notice_board_name + '")]')
        notice_board_link.click()

    def write_notice_in_board(self, subject:str, content:str):
        write_button = self.driver.find_element(By.XPATH, '//a[contains(text(), "쓰기")]')
        write_button.click()

        input_subject = self.driver.find_element("name", "subject")
        input_subject.send_keys(subject)

        input_content = self.driver.find_element("id", "id_contenteditable")
        input_content.send_keys(content)

        submit_button = self.driver.find_element("name", "submitbutton")
        submit_button.click()
