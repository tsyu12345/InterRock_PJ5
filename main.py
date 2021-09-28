from concurrent.futures.process import ProcessPoolExecutor
from scrap import Scraping
import scrap
import PySimpleGUI as sig
import traceback
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
import sys
import concurrent.futures
import threading as th
#from multiprocessing import Pool
import time

class SelectArea:
    def __init__(self):
       
        sig.theme('BluePurple')

    def area_list(self):
        prefs = '北海道,青森県,岩手県,宮城県,秋田県,山形県,福島県,茨城県,栃木県,群馬県,埼玉県,千葉県,東京都,神奈川県,新潟県,富山県,石川県,福井県,山梨県,長野県,岐阜県,静岡県,愛知県,三重県,滋賀県,京都府,大阪府,兵庫県,奈良県,和歌山県,鳥取県,島根県,岡山県,広島県,山口県,徳島県,香川県,愛媛県,高知県,福岡県,佐賀県,長崎県,熊本県,大分県,宮崎県,鹿児島県,沖縄県'
        list_pref = prefs.split(',')
        return list_pref

    def layout(self):
        pref_list = self.area_list()
        L = []
        cnt = 0
        for i in range(8):
            add = []
            for j in range(6):
                if cnt != 47:
                    add.append(sig.Checkbox(
                        pref_list[cnt], key=pref_list[cnt]))
                    cnt += 1
            L.append(add)
        L.append([sig.Button('OK', key='OK')])
        return L

    def display(self):
        window = sig.Window('エリア選択', layout=self.layout())
        self.pref = []
        while True:
            event, value = window.read()
            print(event)
            print(value)
            for v in value.keys():
                if value[v] == True:
                    self.pref.append(v)
            print(self.pref)
            if event in ("Quit", None, 'OK'):
                break
        window.close()
        return self.pref


class Job():
    def __init__(self, path, area_list, junle):
        self.path = path
        self.area_list = area_list
        self.junle = junle
        self.scrap = Scraping(path)
        #self.sub_scrap = Scraping(path, use_sub_driver=False) 
        self.scrap.init_work_book()
        self.url_scrap_flg = False
        self.info_scrap_flg = False
        self.scrap_cnt = 0 #info_scrap count
        self.scrap_sum = 1 #sum count of scraiping
        self.check_flg = False
        self.end_flg = False
        self.detati_flg = False
        self.exception_flg = False

    def __search(self):
        for area in self.area_list:
            if self.junle == 'すべてのジャンル':
                junle_list = [
                    "ヘアサロン",
                    "ネイル・まつげサロン",
                    "リラクサロン",
                    "エステサロン",
                    ]
                for menu in junle_list: 
                    self.scrap.url_scrap(area, menu)
            else:
                self.scrap.url_scrap(area, self.junle)

    def run(self):
        self.url_scrap_flg = True
        self.detati_flg = True
        with concurrent.futures.ProcessPoolExecutor(max_workers=None) as executer:
            future = executer.submit(self.__search)
        #thread = th.Thread(target=self.__search)
        #thread.start()
        #InfoScraping Process
        scraped_row = 2 #初期値2行目
        readyed_row = 1 #初期値1行目
        self.info_scrap_flg = True
        
        while self.info_scrap_flg:
            if future.done() == True and readyed_row != 1 and self.url_scrap_flg == True:
                #url_scrapが終了したとき
                self.scrap.sub_driver.quit()
                self.url_scrap_flg = False
            
            if self.url_scrap_flg == False and scraped_row == readyed_row+1 and self.info_scrap_flg == True:
                #全抽出処理終了判定
                print("break!")
                self.info_scrap_flg = False
                break

            for row in range(scraped_row, readyed_row, 2):
               
                if (self.scrap.sheet.cell(row=row, column=8).value not in ('', None)   #URL抽出済
                    and self.scrap.sheet.cell(row=row, column=2).value == None):#info_scrap未実施                     
                    print("scrap:" + str(row))
                    if self.scrap_cnt % 100 == 0:
                        self.scrap.restart(row)
                    self.scrap.loadHtml(row)
                    self.scrap_cnt += 1
                elif self.scrap.sheet.cell(row=row, column=8).value == '' : 
                    #（予防策）info_scrapで対象都道府県でないときに生成される空行（空文字）に当たった場合。
                    pass
                elif self.scrap.sheet.cell(row=row, column=8).value == None:#まだ未検索
                    self.scrap.book.save(self.path)
                    scraped_row = row
                    break #更新のためbreak
            

            
            scraped_row = readyed_row+1
            readyed_row = self.scrap.sheet_row #最大読み込み行数の更新
            print("row is renewd")
       
        #save data file
        self.detati_flg = False
        #self.scrap.main_driver.quit()
        self.scrap.driver.quit()
        self.scrap.book.save(self.scrap.path)
        # finishing scrap
        self.check_flg = True
        while scrap.check(self.path) == False:
            scrap.apper_adjst(self.path)
        print("OK")
        self.check_flg = False
        self.end_flg = True

    """
        for r in range(2, self.scrap.sheet.max_row+1):
            try:
                if self.scrap_cnt % 100 == 0:
                    self.scrap.restart(r)
                self.scrap.info_scrap(r)
            except TimeoutException:
                self.exception_flg = True
                self.scrap.driver.quit()
                self.scrap.book.save(self.path)
                time.sleep(120)
                self.exception_flg = False
                self.scrap.driver = webdriver.Chrome(executable_path=self.scrap.driver_path, options=self.scrap.options)
                self.scrap.info_scrap(r)
            else:
                self.scrap_cnt += 1
        self.detati_flg = False
        #sig.popup_no_buttons('保存中...。', non_blocking=True, auto_close=True)
        self.scrap.driver.quit()
        self.scrap.book.save(self.scrap.path)
        self.info_scrap_flg = False
    """

    def retry(self):
        """
        Scrapingが失敗したとき（自動再起動でも）手動で再スクレイピングする。
        branch:dev_retry_scraping
        """
    def cancel(self):
        try:
            self.scrap.book.save(self.path)
            self.scrap.driver.quit()
            self.scrap.sub_driver.quit()
        except:
            pass


def menu_list():
    """
    defniction store class
    """
    class_menu = [
        "ヘアサロン",
        "ネイル・まつげサロン",
        "リラクサロン",
        "エステサロン",
        "すべてのジャンル"
    ]
    return class_menu

def layout():
    """
    defniction main window layout
    """

    L1 = [
        [sig.Text("都道府県",
                    key='pref_title', size=(60, None))],
        [sig.InputText(key=('pref_name')), sig.Button('エリア選択')],
        [sig.Text("ジャンル選択", key="class_title", size=(60, None)), ],
        [sig.InputOptionMenu(menu_list(), key=(
            "store_class"), size=(40, None))]
    ]

    L2 = [
        [sig.Text("フォルダ選択", key='path_title', size=(60, None))],
        [sig.InputText(key='path'), sig.SaveAs(
            "選択", file_types=([('Excelファイル', '*.xlsx')]))]
    ]
    L = [
        [sig.Frame("抽出条件", L1)],
        [sig.Frame("保存先", L2)],
        [sig.Button("抽出実行")]
    ]
    return L

def input_checker(win:sig.Window, value):
        checker = [False, False, False]
        if value['pref_name'] == "" :#or re.fullmatch('東京都|北海道|(?:京都|大阪)府|.{2,3}県', self.value['pref_name']) == None:
            text2 = "都道府県　※入力値が不正です。例）東京都, 北海道, 大阪府"
            win['pref_title'].update(text2, text_color='red')
            win['pref_name'].update(background_color='red')
        else:
            text2 = "都道府県"
            win['pref_title'].update(text2, text_color='purple')
            win['pref_name'].update(background_color='white')
            checker[0] = True
        if value['store_class'] == "":
            win['class_title'].update("ジャンル選択　※選択必須です。", text_color='red')
            # win['store_class'].update(background_color = 'red')
        else:
            win['class_title'].update("ジャンル選択", text_color='purple')
            checker[1] = True
        if value['path'] == "":
            win['path_title'].update(
                'フォルダ選択 ※保存先が選択されていません。', text_color='red')
            win['path'].update(background_color="red")
        else:
            win['path_title'].update(text_color='purple')
            win['path'].update(background_color="white")
            checker[2] = True

        if False in checker:
            return False
        else:
            return True

def main():
    sig.theme('BluePurple')
    width = 700
    height = 300
    w_pad = (width / 7, 0)
    win = sig.Window("HotPepperBeautyスクレイピングツール",layout(), icon="e6832bee44cfe3a3844f0a2587ee4bc4_xxo.ico")
    #self.sub_win = sig.Window("抽出実行", self.pop_layout(), icon="icon2.ico")
    running = False
    comp_flg = False
    detati = False
    loading = True
    #executer = TPE(max_workers=2)
    while comp_flg == False:
        event, value = win.read()
        print(event, value)

        if event == 'エリア選択':
            sub_win = SelectArea()
            pref_list = sub_win.display()
            add = ""
            for i in range(len(pref_list)):
                if i == len(pref_list)-1:
                    add += pref_list[i]
                else:
                    add += pref_list[i] + ","
            win['pref_name'].update(add)

        if event == '抽出実行':
            check = input_checker(win, value)
            if check:
                area_list = value['pref_name'].split(",")
                job = Job(value['path'], area_list, value['store_class'])
                #job_thread = th.Thread(target=job.run, daemon=True)
                #job_thread.start()
                with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executer:
                    executer.submit(job.run,)
                running = True
                while running:
                    if job.info_scrap_flg:
                        try:   
                            cancel = sig.one_line_progress_meter("処理中です...", job.scrap_cnt, job.scrap.sheet_row, 'prog', "店舗情報を抽出しています。\nこれには数時間かかることがあります。", orientation='h',)
                        except (TypeError, RuntimeError):
                            cancel = sig.OneLineProgressMeter(
                                "処9理中です...", 0, 1, 'prog', "現在準備中です。")
                            pass

                        if cancel == False and job.detati_flg == True and job.end_flg == False:
                            print("detati in ")
                            detati = True
                            running = False
                            break

                        if job.exception_flg:
                            sig.popup_auto_close('読み込みがタイムアウトしました。120秒後に自動で再起動します。', keep_on_top=True)
                    
                    if job.check_flg:
                        while job.end_flg == False:
                            sig.popup_animated('animationGifs/images/icon_loader_f_ww_01_s1.gif',message="抽出データの確認を行っています。\nあと少しで完了します。")
                            comp_flg = False
                        comp_flg = True
                        running = False
                        break
        
        if comp_flg:
            sig.popup('お疲れ様でした。抽出完了です。保存先を確認してください\n' + value['path'], keep_on_top=True)
            break
        
        if detati:
            try:
                job.cancel()
                #executer.shutdown(wait=False)
                sig.popup("処理を中断しました。途中保存ファイル先は下記です。\n" + value['path'])
                break
            except TypeError:
                break
        # when window close
        if event in ("Quit", None):
            break
    win.close()
    #executer.shutdown(wait=False)
    sys.exit()

if __name__ == "__main__":
    main()