import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def every_downloads_chrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = document.querySelector('downloads-manager')
            .shadowRoot.getElementById('downloadsList').items;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)

def enable_download_headless(browser, download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)

cwd = os.getcwd()

# Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--verbose')
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2,
    "download.default_directory": f"{cwd}/zoom_call",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing_for_trusted_sources_enabled": False,
    "safebrowsing.enabled": False
})
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')
driver = webdriver.Chrome(executable_path=f'{cwd}/chrome/chromedriver', chrome_options=chrome_options)
download_dir = f"{cwd}/zoom_call"
enable_download_headless(driver, download_dir)


daily_motion_link = 'https://www.dailymotion.com'
# base_video_href="https://www.dailymotion.com/search/greetings/videos"
pages = []
not_pages = []
# driver.get(base_video_href)

# Get Download text file
# try:
#     search_btn = WebDriverWait(driver, 15).until(
#                 EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[3]/button')))
#     driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/button').click()
# except:
#     pass

# try:
#     time.sleep(4)
#     for i in range(1, 1000):
#         try:
#             driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
#             WebDriverWait(driver, 15).until(
#                 EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/div/main/div/div/div[1]/div[2]/div[{i}]/div[2]/div[1]/div[1]/a')))
#             x = driver.find_element(By.XPATH, f'/html/body/div[1]/div/main/div/div/div[1]/div[2]/div[{i}]/div[2]/div[1]/div[1]/a').get_attribute('href')
#             page_link = f'{x}'
#             pages.append(page_link)
#             driver.execute_script("window.scrollTo(document.body.scrollHeight, 0)")
#         except Exception as e:
#             not_pages.append(i)
#             print(e)
# except KeyboardInterrupt:
#     pass
# except Exception as e:
#     print(e)



# print(len(pages))
# daily_motion_links = open('dailymotion_greetings.txt', "w")
# for element in pages:
#     daily_motion_links.write(element)
#     daily_motion_links.write('\n')



# To Start DOWNLOADS
with open("download_files.txt", "r") as f:
    line_numbers = list(range(7, 50))
    lines = []
    for i, line in enumerate(f):
        if i in line_numbers:
            lines.append(line.strip())
        elif i > 50:
            break

download_address = []
undownloaded_links = []

for link in lines:
    print(f"Video Index: {lines.index(link) + 1}")
    try:
        driver.get('https://1qvid.com/')
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/section/form/div/button')))
        link_paster = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/form/div/input')
        link_paster.send_keys(link)
        driver.find_element(By.XPATH, '/html/body/div[1]/div/section/form/div/button').click()
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/section/div[1]/div[2]/div/a[1]')))
        driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[1]/div[2]/div/a[1]').click()
        time.sleep(10)
        paths = WebDriverWait(driver, 40, 1).until(every_downloads_chrome)
    except Exception as e:
        print(link)
        undownloaded_links.append(link)
        print(e)


# for link in undownloaded_links:
#     print(f"Undownloaded Video Index: {undownloaded_links.index(link) + 1}")
#     try:
#         driver.get('https://1qvid.com/')
#         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/section/form/div/button')))
#         link_paster = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/form/div/input')
#         link_paster.send_keys(link)
#         driver.find_element(By.XPATH, '/html/body/div[1]/div/section/form/div/button').click()
#         WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/section/div[1]/div[2]/div/a[1]')))
#         driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[1]/div[2]/div/a[1]').click()
#         time.sleep(5)
#         paths = WebDriverWait(driver, 45, 1).until(every_downloads_chrome)
#     except Exception as e:
#         print(e)