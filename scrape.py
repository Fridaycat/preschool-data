from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd

# 初始化 WebDriver（請確保 chromedriver 路徑正確）
driver = webdriver.Chrome()

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
