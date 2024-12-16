from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import mysql.connector as mysql
import requests

class ModelMiner:
    def __init__(self) -> None:
        self.cnx = mysql.connect(
            host="localhost",
            database="cumyo",
            user="root",
            password=""
        )
        self.cursor = self.cnx.cursor(buffered=True)
        self.cursor.execute("SET GLOBAL max_allowed_packet=1073741824;")
        self.cursor.execute("SET GLOBAL net_buffer_length=1048576;")
        self.cursor.execute("SET GLOBAL connect_timeout=31536000;")
        self.cursor.execute("SET GLOBAL interactive_timeout=31536000;")
        self.cursor.execute("SET GLOBAL wait_timeout=31536000;")
        self.url = "https://fapello.com/page-$/"
        self.fast_mode = True
        self.scroll_pause_time = 2
        self.current_page = 0
        self.last_page = 86075
        self.item_count = 0
        self.browser = webdriver.Chrome()
        self.profile_browser = webdriver.Chrome()
        self.accountPage()

    def accountPage(self) -> None:
        self.current_page += 1
        print("|----------------------------------------------------------------------------------------------|\n")
        print("[Page: {}]".format(str(self.current_page)))
        print("[FastMode]" if self.fast_mode == True else None)
        self.browser.get(self.url.replace("$", str(self.current_page)))
        scroll_limit = 10000
        count = 0
        while True and count < scroll_limit:
            last_height = self.browser.execute_script("return document.body.scrollHeight")
            WebDriverWait(self.browser, self.scroll_pause_time)
            new_height = self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            if new_height == last_height:
                break
            last_height = new_height
            count += 1
        WebDriverWait(self.browser, self.scroll_pause_time)
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        self.loopAccountPage(soup)

    def loopAccountPage(self, account_page) -> None:
        content = account_page.find(id='content')
        if content != None:
            items = content.find_all(class_='bg-white shadow rounded-md dark:bg-gray-900 -mx-2 lg:mx-0')
            print("[{} Accounts]".format(str(len(items))))
            for item in items:
                profile = item.find(class_='flex flex-1 items-center space-x-4')
                link = profile.find_all("a")[0]["href"]
                name = item.find(class_='block capitalize font-semibold dark:text-gray-100').getText()
                # print("Model {}, Profile {}".format(name, link))
                self.scrapeAccount(name, link)
            self.account_page()
        else:
            print("[No Posts]")

    def scrapeAccount(self, name, account_url) -> None:
        self.profile_browser.get(account_url)
        scroll_limit = 3000
        count = 0
        while True and count < scroll_limit:
            last_height = self.profile_browser.execute_script("return document.body.scrollHeight")
            WebDriverWait(self.profile_browser, self.scroll_pause_time)
            new_height = self.profile_browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            if new_height == last_height:
                break
            last_height = new_height
            count += 1
        WebDriverWait(self.profile_browser, self.scroll_pause_time)
        soup = BeautifulSoup(self.profile_browser.page_source, 'html.parser')
        detail_section = soup.find(class_='flex lg:flex-row flex-col items-center lg:py-8 lg:space-x-8')
        model_name = name.lstrip().rstrip()
        model_img = detail_section.find('img')['src'] if detail_section != None else 'https://fapello.com/assets/images/avatar.jpg'
        model_url = account_url.replace("https://fapello.com/", "").replace("/", "")
        socials = soup.find(class_='lg:w/8/12 flex-1 flex flex-col lg:items-start items-center')
        if socials is not None:
            names = socials.find_all('p')
            if names is not None:
                if len(names) > 0:
                    p1 = names[0]
                    if "onlyfans" in p1.getText().lower() or "youtube" in p1.getText().lower() or "patreon" in p1.getText().lower() or "twitter" in p1.getText().lower() or "instagram" in p1.getText().lower() or "tiktok" in p1.getText().lower() or "facebook" in p1.getText().lower() or "camsoda" in p1.getText().lower():
                        other_names = ""
                    else:
                        other_names = p1.getText()
                else:
                    other_names = ""
            links = socials.find_all("a")
            if len(links) > 0:
                onlyfans = ""
                patreon = ""
                instagram = ""
                twitter = ""
                snapchat = ""
                tiktok = ""
                facebook = ""
                youtube = ""
                camsoda = ""
                for link in links:
                    link = link['href']
                    if "onlyfans" in link:
                        onlyfans = link
                    if "patreon" in link:
                        patreon = link
                    if "instagram" in link:
                        instagram = link
                    if "twitter" in link:
                        twitter = link
                    if "snapchat" in link:
                        snapchat = link
                    if "tiktok" in link:
                        tiktok = link
                    if "facebook" in link:
                        facebook = link
                    if "youtube" in link:
                        youtube = link
                    if "camsoda" in link:
                        camsoda = link
                #self.update_model_social_accounts(other_names, onlyfans, patreon, instagram, twitter, snapchat, tiktok, facebook, youtube)
                model_id = self.accountStore(model_name, model_img, model_url, other_names, onlyfans, patreon, instagram, twitter, snapchat, tiktok, facebook, youtube, camsoda)
                #print(model_id)
        content = soup.find(id='content')
        items = content.find_all(class_='max-w-full lg:h-64 h-40 rounded-md relative overflow-hidden uk-transition-toggle')
        print("Posts: {}".format(len(items)))
        print("|----------------------------------------------------------------------------------------------|\n")
        for item in items:
            self.item_count += 1
            if self.profile_browser == True and self.item_count > 80:
                break
            img = item.find('img')
            is_video = False
            video_check = img['src'].replace("_300px", "").replace(".jpg", ".mp4")
            try:
                check_is_video = requests.get(video_check, timeout=200)
                if check_is_video.status_code == 200 or check_is_video.status_code == 201:
                    is_video = True
                source = img['src'].replace("_300px", "").replace(".jpg", ".mp4") if is_video == True else img['src'].replace("_300px", "")
                self.postStore(model_id[0], is_video, source)
            except requests.exceptions.Timeout:
                continue
        self.item_count = 0

    def accountStore(self, name, picture, url, other_names, onlyfans, patreon, instagram, twitter, snapchat, tiktok, facebook, youtube, camsoda) -> int:
        already_exist = self.accountCheck(url)
        print("\n|----------------------------------------------------------------------------------------------|")
        print("Account: {}".format(name))
        if already_exist == False:
            self.cursor.execute('INSERT INTO Model (name, picture, url, other_names, onlyfans, patreon, instagram, twitter, snapchat, tiktok, facebook, youtube, camsoda) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (name, picture, url, other_names, onlyfans, patreon, instagram, twitter, snapchat, tiktok, facebook, youtube, camsoda))
            self.cnx.commit()
            self.cursor.execute('SELECT id, name FROM Model WHERE url = %s LIMIT 1', (url,))
            fetch = self.cursor.fetchall()
            model_id = fetch[0]
            return model_id
        else:
            print("[Account already exist]")
            self.cursor.execute('SELECT id, name FROM Model WHERE url = %s LIMIT 1', (url,))
            fetch = self.cursor.fetchall()
            return fetch[0] # model id

    def accountCheck(self, url) -> bool:
        self.cursor.execute('SELECT url FROM Model WHERE url = %s LIMIT 1', (url,))
        fetch = self.cursor.fetchall()
        count = self.cursor.rowcount
        if count > 0: return True
        return False
            
    def postStore(self, model_id, content_type, source) -> None:
        already_exist = self.postCheck(source)
        print("Post: {}".format(source.replace("https://fapello.com/", "/")))
        if already_exist == False:
            self.cursor.execute('INSERT INTO Post (model_id, provider, content_type, source) VALUES (%s, %s, %s, %s)', (model_id, 'fapello', content_type, source))
            self.cnx.commit()
        else:
            print("[Post already exist]")

    def postCheck(self, source) -> bool:
        self.cursor.execute('SELECT source FROM Post WHERE source = %s LIMIT 1', (source,))
        fetch = self.cursor.fetchall()
        count = self.cursor.rowcount
        if count > 0: return True
        return False

init = ModelMiner()