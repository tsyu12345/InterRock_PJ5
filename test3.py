from selenium import webdriver
from concurrent.futures import ProcessPoolExecutor
class Test():

    def __init__(self):
        #self.path = path
        self.driver_path = 'chromedriver_win32/chromedriver.exe'
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
        browser_path = 'chrome-win/chrome.exe'
        self.options.binary_location = browser_path
        #self.driver = webdriver.Chrome(executable_path=self.driver_path, options=self.options)
    
    def loadHtml(self):
        self.driver = webdriver.Chrome(executable_path = 'chromedriver_win32/chromedriver.exe', options=self.options)
        self.driver.get('https://qiita.com/yukitaka13-1110/items/2580b4fc6c8a30d34661')
        html = self.driver.page_source
        print(html)

if __name__ == "__main__":
    test = Test()
    executer = ProcessPoolExecutor(max_workers=None)
    futures = executer.submit(test.loadHtml)
    while True:
        if futures.done():
            futures.result()
            break
