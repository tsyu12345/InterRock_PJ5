from selenium import webdriver

def catch_driver(driver:webdriver):
    driver.get('https://www.google.com/?hl=ja')

if __name__ == '__main__':
    print("start chrome driver...")
    driver = webdriver.Chrome(executable_path='chromedriver_win32/chromedriver.exe')
    catch_driver(driver=driver)


