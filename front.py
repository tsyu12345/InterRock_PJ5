from scrap import Scraping
import scrap
import PySimpleGUI as sig
from PySimpleGUI.PySimpleGUI import Frame, SaveAs, T, Text
import sys
#from concurrent.futures import ThreadPoolExecutor as TPE
import threading as th


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
            [sig.InputText(key='path'), sig.SaveAs(
                "選択", file_types=([('Excelファイル', '*.xlsx')]))]
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
            [sig.ProgressBar(100, orientation="h",
                             size=(20, 20), key="progbar")],
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
        self.win = sig.Window("HotPepperBeautyスクレイピングツール",
                              self.layout(), icon="icon2.ico")
        #self.sub_win = sig.Window("抽出実行", self.pop_layout(), icon="icon2.ico")
        running = False
        comp_flg = False
        detati = False
        loading = True
        #executer = TPE(max_workers=2)
        while comp_flg == False:
            self.event, self.value = self.win.read()
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
                    area_list = self.value['pref_name'].split(",")
                    job = Job(self.value['path'], area_list,
                              self.value['store_class'])
                    th1 = th.Thread(target=job.run, daemon=True)
                    th1.start()
                    running = True
                    while running:

                        if job.url_scrap_flg:
                            #sig.popup_no_buttons('掲載URLを抽出処理中です。ブラウザの動作を止めないでください。', non_blocking=True, auto_close=True)
                            page_cnt = job.scrap.page_count
                            prog_count = job.scrap.counter
                            try:
                                cancel = sig.one_line_progress_meter("処理中です...", prog_count, page_cnt, 'prog', "掲載URLを抽出しています。しばらくお待ちください。",orientation='h')

                            except TypeError:
                                cancel = sig.OneLineProgressMeter(
                                    "処理中です...", 0, 1, 'prog', "現在準備中です。")
                            
                            if cancel == False and job.detati_flg == True and job.end_flg == False:
                                print("detati in ")
                                sig.popup_no_buttons('中止処理中です...。', non_blocking=True, auto_close=True)
                                detati = True
                                running = False
                                break
                            
                        #cancel = sig.popup_cancel('抽出処理中です。これには数時間かかることがあります。\n中断するには’Cancelled’ボタンを押してください。')
                        if job.info_scrap_flg:
                            try:   
                                cancel = sig.one_line_progress_meter("処理中です...", job.scrap_cnt, job.scrap_sum, 'prog', "店舗情報を抽出しています。\nこれには数時間かかることがあります。", orientation='h',)
                            except (TypeError, RuntimeError):
                                cancel = sig.OneLineProgressMeter(
                                    "処理中です...", 0, 1, 'prog', "現在準備中です。")
                                pass

                            if cancel == False and job.detati_flg == True and job.end_flg == False:
                                print("detati in ")
                                detati = True
                                running = False
                                break
                            
                        if job.check_flg:
                            sig.popup_no_buttons('ただいま抽出データチェック中です。あと少しで完了です。', non_blocking=True, auto_close=True, keep_on_top=True)
                            while job.end_flg == False:
                                comp_flg = False
                            comp_flg = True
                            running = False
                            break
            
            if comp_flg:
                sig.popup('お疲れ様でした。抽出完了です。保存先を確認してください\n' +
                    self.value['path'], keep_on_top=True)
                break
            
            if detati:
                try:
                    job.cancel()
                    #executer.shutdown(wait=False)
                    sig.popup("処理を中断しました。途中保存ファイル先は下記です。\n" +
                              self.value['path'])
                    break
                except TypeError:
                    break
            # when window close
            if self.event in ("Quit", None):
                break
        self.win.close()
        #executer.shutdown(wait=False)
        sys.exit()

    def input_checker(self):
        checker = [False, False, False]
        if self.value['pref_name'] == "" :#or re.fullmatch('東京都|北海道|(?:京都|大阪)府|.{2,3}県', self.value['pref_name']) == None:
            text2 = "都道府県　※入力値が不正です。例）東京都, 北海道, 大阪府"
            self.win['pref_title'].update(text2, text_color='red')
            self.win['pref_name'].update(background_color='red')
        else:
            text2 = "都道府県"
            self.win['pref_title'].update(text2, text_color='purple')
            self.win['pref_name'].update(background_color='white')
            checker[0] = True
        if self.value['store_class'] == "":
            self.win['class_title'].update("ジャンル選択　※選択必須です。", text_color='red')
            # win['store_class'].update(background_color = 'red')
        else:
            self.win['class_title'].update("ジャンル選択", text_color='purple')
            checker[1] = True
        if self.value['path'] == "":
            self.win['path_title'].update(
                'フォルダ選択 ※保存先が選択されていません。', text_color='red')
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
        self.scrap.init_work_book()
        self.url_scrap_flg = False
        self.info_scrap_flg = False
        self.scrap_cnt = 0
        self.scrap_sum = 1
        self.check_flg = False
        self.end_flg = False
        self.detati_flg = False

    def run(self):
        # url scraiping
        print("hre")
        self.url_scrap_flg = True
        if self.junle == 'すべてのジャンル':
            self.detati_flg = True
            self.scrap.all_scrap(self.area_list)
        else:
            print("in run elif")
            for area in self.area_list:
                self.scrap.counter = 0
                self.detati_flg = True
                self.scrap.url_scrap(area, self.junle)
        # info scraiping
        self.detati_flg = False
        self.url_scrap_flg = False
        self.info_scrap_flg = True
        self.detati_flg = True
        self.scrap_sum = self.scrap.sheet.max_row
        for r in range(2, self.scrap.sheet.max_row+1):
            if self.scrap_cnt % 100 == 0:
                self.scrap.restart(r)
            self.scrap.info_scrap(r)
            self.scrap_cnt += 1
        self.detati_flg = False
        self.info_scrap_flg = False
        #sig.popup_no_buttons('保存中...。', non_blocking=True, auto_close=True)
        self.scrap.driver.quit()
        self.scrap.book.save(self.path)

        # finishing scrap
        self.check_flg = True
        while scrap.check(self.path) == False:
            scrap.apper_adjst(self.path)
        print("OK")
        self.check_flg = False
        self.end_flg = True


    def cancel(self):
        self.scrap.book.save(self.path)
        self.scrap.driver.quit()


if __name__ == '__main__':
    main_win = Windows()
    main_win.display()
