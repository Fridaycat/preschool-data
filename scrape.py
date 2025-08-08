import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
import csv

def scrape_page(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find("table", {"id": "ContentPlaceHolder1_gvData"})
    if not table:
        print("找不到資料表格")
        return []

    rows = table.find_all("tr")[1:]  # 跳過表頭
    page_data = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue
        name = cols[0].get_text(strip=True)
        address = cols[1].get_text(strip=True)
        phone = cols[2].get_text(strip=True)
        approved_num = cols[3].get_text(strip=True)
        page_data.append([name, address, phone, approved_num])
    return page_data

def main():
    options = uc.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    driver = uc.Chrome(options=options)

    try:
        url = "https://ap.ece.moe.edu.tw/webecems/pubSearch.aspx"
        driver.get(url)
        time.sleep(5)

        all_data = []
        page_num = 1

        while True:
            print(f"正在爬取第 {page_num} 頁...")
            page_data = scrape_page(driver)
            if not page_data:
                print("本頁無資料或無法取得，結束爬取。")
                break
            all_data.extend(page_data)

            try:
                next_button = driver.find_element("id", "ContentPlaceHolder1_gvData_ctl13_btnNext")
                if "disabled" in next_button.get_attribute("class"):
                    print("已到最後一頁，結束。")
                    break
                next_button.click()
                page_num += 1
                time.sleep(5)
            except Exception as e:
                print("找不到下一頁按鈕或無法點擊，結束。", e)
                break

        with open("preschool_data_all_pages.csv", "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["幼兒園名字", "地址", "電話", "核定人數"])
            writer.writerows(all_data)

        print(f"共抓取 {len(all_data)} 筆資料，已存入 preschool_data_all_pages.csv")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
