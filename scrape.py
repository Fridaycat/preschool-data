import undetected_chromedriver as uc
import time

def main():
    options = uc.ChromeOptions()
    options.add_argument('--headless=new')  # Chrome 新版 headless 模式
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    driver = uc.Chrome(options=options)

    try:
        url = "https://ap.ece.moe.edu.tw/webecems/pubSearch.aspx"
        driver.get(url)
        time.sleep(5)  # 等待頁面載入與JS執行

        print("頁面標題:", driver.title)

        # 你可以加上你爬資料的邏輯，像是：
        # page_source = driver.page_source
        # 用 BeautifulSoup 或其他工具解析

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
