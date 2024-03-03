from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def scrap():
    url = 'https://coinmarketcap.com/'

    op = Options()

    op.add_argument("--no-sandbox")
    op.add_argument("--headless")
    op.add_argument("start-maximized")
    op.add_argument("window-size=1900,1080")
    op.add_argument("disable-gpu")
    op.add_argument("--disable-software-rasterizer")
    op.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=op)
    driver.get(url)
    result = 50
    try:
        result = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div[3]/div[2]/div/span[1]').text
    except NoSuchElementException:
        print('Error occurred:')
        print(NoSuchElementException)
    driver.quit()
    print(result)
    return result
