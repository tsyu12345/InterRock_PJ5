from scrap import Scraping
import scrap
import PySimpleGUI as sig
from PySimpleGUI.PySimpleGUI import SaveAs, Text
import re
import logging as log
import threading as th
import sys

class Windows:

    def __init__(self):
        # window tema
        sig.theme('BluePurple')
        self.width = 700
        self.height = 300
        self.w_pad = (self.width / 7, 0)
        self.done = False

    def layout(self):
        L1 = [
            [sig.Text("都道府県",
                      key='pref_title', size=(60, None))],
            [sig.InputText(key=('pref_name')), sig.Button('エリア選択')],
            [sig.Text("ジャンル選択", key="class_title", size=(60, None)), ],
            [sig.InputOptionMenu(self.menu_list(), key=(
                "store_class"), size=(40, None))]
        ]

        L2 = [
            [sig.Text("フォルダ選択", key='path_title', size=(60, None))],
            [sig.InputText(key='path'), sig.SaveAs("選択", file_types=( [('Excelファイル','*.xlsx')]))]
        ]
        L = [
            [sig.Frame("抽出条件", L1)],
            [sig.Frame("保存先", L2)],
            [sig.Button("抽出実行")]
        ]
        return L
    def pop_layout(self):
        L = [
            [sig.Text("抽出実行中…")],
            [sig.ProgressBar(100, orientation="h", size=(20, 20), key="progbar")],
            [sig.Cancel('中止')],
        ]
        return L

    def menu_list(self):
        class_menu = [
            "ヘアサロン",
            "ネイル・まつげサロン",
            "リラクサロン",
            "エステサロン",
            "すべてのジャンル"
            ]
        return class_menu

    def display(self):
        self.win = sig.Window("HotPepperBeautyスクレイピングツール", self.layout(), icon="icon2.ico")
        #self.sub_win = sig.Window("抽出実行", self.pop_layout(), icon="icon2.ico")
        count = 0
        i = 0
        while True:
            self.event, self.value = self.win.read()
            area_list = self.value['pref_name'].split(",")
            print(area_list)
            th1 = th.Thread(target=main, args=(area_list, self.value['store_class'], self.value['path']), daemon=True)
            print(self.event, self.value)
            if self.event == 'エリア選択':
                sub_win = SelectArea()
                self.pref_list = sub_win.display()
                add = ""
                for i in range(len(self.pref_list)):
                    if i == len(self.pref_list)-1:
                        add += self.pref_list[i]
                    else:
                        add += self.pref_list[i] + ","
                self.win['pref_name'].update(add)
            if self.event == '抽出実行':
                check = self.input_checker()
                if check:
                    i += 1
                    #th1.setDaemon(True)
                    th1.start()
                    #count = 1
                    #sub_event, sub_value = self.sub_win.read()
                    #self.sub_win['progbar'].update_bar(50)
                    cancel = sig.popup_cancel('抽出処理中です。これには数時間かかることがあります。\n中断するには’Cancelled’ボタンを押してください。')
                    print(cancel)
                    if cancel in ('Cancelled', None):
                        sys.exit()
            #th1.join()
                    self.done = True
                    #sig.popup('お疲れ様でした。抽出終了です。ファイルを確認してください。\n保存先：'+self.value['path'], keep_on_top=True)
            #when window close
            if self.event in ("Quit", None) or self.done:
                break
        self.win.close()

    def input_checker(self):
        checker = [False, False, False]
        if self.value['pref_name'] == "" :#or re.fullmatch('東京都|北海道|(?:京都|大阪)府|.{2,3}県') == None:
            text2 = "都道府県　※入力値が不正です。例）東京都, 北海道, 大阪府"
            self.win['pref_title'].update(text2, text_color='red')
            self.win['pref_name'].update(background_color='red')
        else:
            text2 = "都道府県"
            self.win['pref_title'].update(text2, text_color='purple')
            self.win['pref_name'].update(background_color = 'white')
            checker[0] = True
        if self.value['store_class'] == "":
            self.win['class_title'].update("ジャンル選択　※選択必須です。", text_color='red')
            # win['store_class'].update(background_color = 'red')
        else:
            self.win['class_title'].update("ジャンル選択", text_color='purple')
            checker[1] = True
        if self.value['path'] == "":
            self.win['path_title'].update('フォルダ選択 ※保存先が選択されていません。',text_color='red')
            self.win['path'].update(background_color="red")
        else:
            self.win['path_title'].update(text_color='purple')
            self.win['path'].update(background_color="white")
            checker[2] = True
        
        if False in checker:
            return False
        else:
            return True

class SelectArea:
    def __init__(self):
        width = 500
        height = 500
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
                    add.append(sig.Checkbox(pref_list[cnt], key=pref_list[cnt]))
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

class Job(Scraping):
    def __init__(self, path):
        super().__init__(path)
        super().init_work_book()
    
    def URL_scraping(area_list, junle):
        if junle == 'すべてのジャンル':
            super().all_scrap(area_list)
        else:
            for area in area_list:
                super().url_scrap(area, junle)
    
    def info_scraiping(self):
        
        for r in range(2, super().sheet.max_row+1):
            sig.OneLineProgressMeter("ただいま処理中です。これには数時間かかることがあります。", r-1, super().sheet.max_row-1)
            super().info_scrap(r)
        super().book.save(super().path)
        #finishing scrap
        while scrap.check(super().path) == False:
            scrap.apper_adjst(super().path)
        sig.popup('お疲れ様でした。抽出終了です。ファイルを確認してください。\n保存先：' +
                  super().path, keep_on_top=True)
        
def main(area_list, junle, path):
    job = Job(path=path)
    job.URL_scraping(area_list, junle)
    job.info_scraiping()
        
if __name__ == '__main__':
    main_win = Windows()
    main_win.display()



