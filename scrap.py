from typing import Counter
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException, InvalidSwitchToTargetException, NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
import openpyxl as px
from openpyxl.styles import PatternFill
from bs4 import BeautifulSoup as bs
import time
import datetime
import re
import requests as rq
import threading as th
import sys
import os
import PySimpleGUI as sig


class Scraping():
    book = px.Workbook()
    sheet = book.worksheets[0]
    RETRY = 3
    TIMEOUT = 15

    def __init__(self, path):
        self.path = path
        # init driver
        self.driver_path = resource_path('chromedriver_win32/chromedriver.exe')
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("start-maximized")
        self.options.add_argument("enable-automation")
        self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-infobars")
        self.options.add_argument('--disable-extensions')
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-browser-side-navigation")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')
        prefs = {"profile.default_content_setting_values.notifications": 2}
        self.options.add_experimental_option("prefs", prefs)
        browser_path = resource_path('chrome-win/chrome.exe')
        self.options.binary_location = browser_path
        self.driver = webdriver.Chrome(executable_path=self.driver_path, options=self.options)
        self.counter = 0
        self.page_count = 1
        #self.area = area
        #self.store_class = store_class

    def init_work_book(self):
        menu = [
            "ジャンル",
            "店舗名",
            "店舗名カナ",
            "電話番号",
            "都道府県コード",
            "都道府県",
            "市区町村・番地",
            "店舗URL",
            "詳細データ取得日",
            "料金プラン着地",
            "月額料金",
            "お店のホームページ",
            "パンくず",
            "ヘッダー画像有無",
            "こだわり有無",
            "スライド画像数",
            "キャッチコピー",
            "アクセス・道案内",
            "営業時間",
            "定休日",
            "支払い方法",
            "設備",
            "カット価格",
            "席数",
            "スタッフ数",
            "駐車場",
            "こだわり条件",
            "備考",
            "スタッフ募集",
            "最終更新日"
        ]
        for c in range(1, 30+1):
            self.sheet.cell(row=1, column=c, value=menu[c-1])
        self.sheet.freeze_panes = "A2"

        self.book.save(self.path)

    def all_scrap(self, area_list):  # 全件抽出
        class_menu = [
            "ヘアサロン",
            "ネイル・まつげサロン",
            "リラクサロン",
            "エステサロン",
        ]
        for area in area_list:
            for junle in class_menu:
                self.counter = 0
                self.url_scrap(area, junle)
            print(area + "search complete.")

    def url_scrap(self, area, store_junle):
        #MAX_RETRY = 3
        print("starting ChromeDriver.exe....")
        
        self.driver.get("https://beauty.hotpepper.jp/top/")  # top page
        sr_class = self.driver.find_element_by_link_text(store_junle)#ジャンル選択
        sr_class.click()
        time.sleep(5)
        search = self.driver.find_element_by_css_selector('#freeWordSearch1')
        search.send_keys(area + Keys.ENTER)
        time.sleep(2)
        result_pages = self.driver.find_element_by_css_selector(
            'p.pa.bottom0.right0').text
        page_num = re.split('[/ ]', result_pages)
        pages = re.sub(r"\D", "", page_num[1])
        print("pages : " + pages)
        self.page_count = int(pages)
        for i in range(int(pages)):
            #sig.OneLineProgressMeter("掲載URLの抽出中...", self.counter, int(pages))
            try:
                html = self.driver.page_source
                soup = bs(html, 'lxml')
                links_list = soup.select("div.slcHeadContentsInner > h3 > a")
                for a in links_list:
                    url = a.get('href')
                    r = self.sheet.max_row
                    self.sheet.cell(row=r+1, column=1, value=store_junle)#ジャンル
                    self.sheet.cell(row=r+1, column=6, value=area)#エリア
                    self.sheet.cell(row=r+1, column=8, value=url)#URL
                    #print(self.sheet.cell(row=r+1, column=8).value)
                try:
                    pre_url = self.driver.current_url
                    pre_index = i
                    next_btn = self.driver.find_element_by_link_text("次へ")
                    next_btn.click()
                    time.sleep(1)
                except NoSuchElementException:
                    break
            except (WebDriverException, TimeoutException):
                self.book.save(self.path)
                self.driver.quit()
                time.sleep(10)
                print("starting ChromeDriver.exe....")
                self.driver = webdriver.Chrome(
                    executable_path=self.driver_path, options=self.options)
                self.driver.get(pre_url)
                next_btn = self.driver.find_element_by_link_text("次へ")
                next_btn.click()
                time.sleep(1)
                continue
            else:
                pass
            self.counter += 1

        self.book.save(self.path)
        print("search complete")
        #self.driver.close()

    def info_scrap(self, index):
        #conunter = 0
        try:
            url = self.sheet.cell(row=index, column=8).value
            self.driver.get(url)
        except (WebDriverException, TimeoutException):
            time.sleep(10)
            self.restart(url)
        else:
            pass
        html = self.driver.page_source
        soup = bs(html, 'lxml')
        table_value = soup.select(
            'div.mT30 > table > tbody > tr > td')
        table_menu = soup.select(
            'div.mT30 > table > tbody > tr > th')
          # 住所の抽出（少々処理があるため別で書き出す）
        pref_tf = True
        for j, e in enumerate(table_menu):
            if e.get_text() == "住所":
                all_address = table_value[j].get_text()
                prefecture_search = re.search(
                    '東京都|北海道|(?:京都|大阪)府|.{2,3}県', all_address)
                address_low = re.split(
                    '東京都|北海道|(?:京都|大阪)府|.{2,3}県', all_address)  # 県名とそれ以降を分離
                prefecture = prefecture_search.group()  # 県名
                if prefecture != self.sheet.cell(row=index, column=6).value:
                    self.sheet.cell(row=index, column=8, value="")
                    self.sheet.cell(row=index, column=6, value="")
                    self.sheet.cell(row=index, column=1, value="")
                    pref_tf = False
                jis_code = self.call_jis_code(prefecture)
                municipality = address_low[1]  # それ以降
                break
        print("都道府県：" + prefecture)
        print("市区町村番地：" + municipality)
        # 指定エリアでないとき、下記処理を行わない
        try:
            if pref_tf:
                store_name_tag = soup.select_one('p.detailTitle > a')
                store_name = store_name_tag.get_text()
                print("店名：" + store_name)
                st_name_kana_tag = soup.select_one(
                    'div > p.fs10.fgGray')
                st_name_kana = st_name_kana_tag.get_text()
                print("店名カナ：" + st_name_kana)
                try:
                    tel_tag = soup.select_one(
                        'div.mT30 > table > tbody > tr > td > a')
                    tel_url = tel_tag.get('href')
                    respons_tel = rq.get(tel_url)
                    html_tel = respons_tel.text
                    soup_tel = bs(html_tel, 'lxml')
                    tel_num_tag = soup_tel.select_one(
                        'table > tr > td')
                    tel_num = tel_num_tag.get_text()
                    tel_num = str(tel_num)
                    tel_num = tel_num.replace(' ', "")
                    print("TEL : " + tel_num)
                except:
                    tel_num = ""
                    pass
                    # ヘッダー画像の有無
                try:
                    self.driver.find_element_by_css_selector(
                        'div.slnHeaderSliderPhoto.jscViewerPhoto')
                    head_img_yn = "有"
                    # self.sheet.cell(row=index, column=14, value="有")
                except NoSuchElementException:
                    head_img_yn = "無"
                    # self.sheet.cell(row=index, column=14, value="無")
                    pass
                catch_copy_tag = soup.select_one('div > p > b > strong')
                catch_copy = catch_copy_tag.get_text()

                pankuzu_tag = soup.select('#preContents > ol > li')
                pankuzu = ""
                for pan in pankuzu_tag:
                    pankuzu += pan.get_text()
                print(pankuzu)

                slide_img_tag = soup.select(
                    'div.slnTopImgCarouselWrap.jscThumbWrap > ul > li')
                slide_cnt = len(slide_img_tag)

                # write Excel
                self.sheet.cell(row=index, column=2, value=store_name)
                self.sheet.cell(row=index, column=3, value=st_name_kana)
                self.sheet.cell(row=index, column=4, value=tel_num)
                self.sheet.cell(row=index, column=5, value=jis_code)
                self.sheet.cell(row=index, column=6, value=prefecture)
                self.sheet.cell(row=index, column=7, value=municipality)
                self.sheet.cell(row=index, column=9, value=self.scrap_day())
                self.sheet.cell(row=index, column=13, value=pankuzu)
                self.sheet.cell(row=index, column=16, value=slide_cnt)
                self.sheet.cell(row=index, column=17, value=catch_copy)
                self.sheet.cell(row=index, column=14, value=head_img_yn)
                # 他の情報処理
                try:
                    for j in range(2, len(table_value)):
                        for c in range(1, self.sheet.max_column):
                            if table_menu[j].get_text() == self.sheet.cell(row=1, column=c).value:
                                self.sheet.cell(
                                    row=index, column=c, value=table_value[j].get_text())
                                break
                except RuntimeError:
                    pass
            else:
                print("prefname is False")
        except:
            #self.book_save()
            pass

    def restart(self, index):
        self.book.save(self.path)
        self.driver.quit()
        time.sleep(5)
        self.driver = webdriver.Chrome(executable_path=self.driver_path, options=self.options)
        url = self.sheet.cell(row=index, column=8).value
        self.driver.get(url)

    def call_jis_code(self, key):
        pref_jiscode = {
            "北海道": '01',
            "青森県": '02',
            "岩手県": '03',
            "宮城県": '04',
            "秋田県": '05',
            "山形県": '06',
            "福島県": '07',
            "茨城県": '08',
            "栃木県": '09',
            "群馬県": 10,
            "埼玉県": 11,
            "千葉県": 12,
            "東京都": 13,
            "神奈川県": 14,
            "新潟県": 15,
            "富山県": 16,
            "石川県": 17,
            "福井県": 18,
            "山梨県": 19,
            "長野県": 20,
            "岐阜県": 21,
            "静岡県": 22,
            "愛知県": 23,
            "三重県": 24,
            "滋賀県": 25,
            "京都府": 26,
            "大阪府": 27,
            "兵庫県": 28,
            "奈良県": 29,
            "和歌山県": 30,
            "鳥取県": 31,
            "島根県": 32,
            "岡山県": 33,
            "広島県": 34,
            "山口県": 35,
            "徳島県": 36,
            "香川県": 37,
            "愛媛県": 38,
            "高知県": 39,
            "福岡県": 40,
            "佐賀県": 41,
            "長崎県": 42,
            "熊本県": 43,
            "大分県": 44,
            "宮崎県": 45,
            "鹿児島県": 46,
            "沖縄県": 47
        }
        code = pref_jiscode[key]
        print(code)
        return code

    def scrap_day(self):
        dt_now = datetime.datetime.now()
        year = str(dt_now.year)
        month = str(dt_now.month)
        day = str(dt_now.day)
        hour = str(dt_now.hour)
        min = str(dt_now.minute)
        data_day = year + "," + month + day + "," + hour + min
        print(data_day)
        return data_day


def resource_path(relative_path):#バイナリフィルのパスを提供
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

def apper_adjst(path):#空白行を削除する
    book = px.load_workbook(path)
    sheet = book.worksheets[0]
    for r in range(2, sheet.max_row+1):
        print("check" + str(r))
        #sig.OneLineProgressMeter('内容チェック中...', r-1, sheet.max_row-1, args="データの内容をチェック中...です。")
        if sheet.cell(row=r, column=1).value == "" or sheet.cell(row=r, column=1).value == None:
            sheet.delete_rows(r)
    book.save(path)

def check(path):
    book = px.load_workbook(path)
    sheet = book.worksheets[0]
    for r in range(2, sheet.max_row+1):
        print("check" + str(r))
        #sig.OneLineProgressMeter('内容チェック中...', r-1, sheet.max_row-1)
        if sheet.cell(row=r, column=2).value in ("", " ", None):
            fill =  PatternFill(patternType='solid', fgColor='ffff00')
            sheet['B'+str(r)].fill = fill
            sheet.cell(row=r, column=2, value='抽出不可')
        if sheet.cell(row=r, column=1).value == "" or sheet.cell(row=r, column=1).value == None:
            return False
    book.save(path)
    return True

if __name__ == "__main__":
    job = Scraping('./kouti_test.xlsx')
    job.init_work_book()
    job.url_scrap('高知県', 'ヘアサロン')
    for r in range(2, job.sheet.max_row+1):
        sig.OneLineProgressMeter("処理中です。しばらくお待ちください。", r, job.sheet.max_row)
        job.info_scrap(r)
    job.book.save('./kouti_test.xlsx')
    job.driver.quit()
    while check('./kouti_test.xlsx') == False:
        apper_adjst('./kouti_test.xlsx')
        job.book.save('./kouti_test.xlsx')
    
