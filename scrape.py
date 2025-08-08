from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--disable-extensions")
options.add_argument("--disable-dev-tools")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("--window-size=1920,1080")

# 不要設定 user-data-dir（這是錯誤的來源）
driver = webdriver.Chrome(options=options)

# 打開網站
url = "https://ap.ece.moe.edu.tw/webecems/pubSearch.aspx"
driver.get(url)
time.sleep(2)  # 等待網頁加載

# 模擬點擊「查詢」按鈕，不輸入條件查全部
search_button = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btnSearch")
search_button.click()
time.sleep(3)

# 存放資料
data = []

# 逐頁抓資料
while True:
    rows = driver.find_elements(By.XPATH, "//table[@id='ctl00_ContentPlaceHolder1_gvList']/tbody/tr")[1:]  # 跳過標題列

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 7:
            name = cols[1].text.strip()
            address = cols[4].text.strip()
            phone = cols[5].text.strip()
            capacity = cols[6].text.strip()
            data.append([name, address, phone, capacity])

    # 嘗試點下一頁（如果有的話）
    try:
        next_link = driver.find_element(By.LINK_TEXT, "下一頁")
        next_link.click()
        time.sleep(2)
    except:
        break  # 沒有下一頁就跳出

driver.quit()

# 轉換為 DataFrame 並匯出 CSV
df = pd.DataFrame(data, columns=["幼兒園名稱", "地址", "電話", "核定人數"])
df.to_csv("幼兒園列表.csv", index=False, encoding="utf-8-sig")
print("✅ 資料抓取完成！已匯出為 CSV")
