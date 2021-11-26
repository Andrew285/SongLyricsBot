import telebot
from bs4 import BeautifulSoup
import requests
import os
from selenium import webdriver   # for webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options


chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

song_bot = telebot.TeleBot("2128007635:AAHuDH8KQlA_RwNDSHE_v2ME2I4tHizdWV8")

replaced_singer = ""

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en,uk-UA;q=0.9,uk;q=0.8,en-US;q=0.7",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36",
    "From": "bostapchuk23@gmail.com"
}

# proxies = {
#     "http": "http://218.252.244.104:80"
# }

# @song_bot.message_handler(content_types=["text"])
# def get_singer(message):
#     global replaced_singer
#     mssg = message.text
#     replaced_singer = mssg.replace(" ", "+")
#     msg = song_bot.send_message(message.chat.id, "Now enter the song name:")
#     song_bot.register_next_step_handler(msg, get_song)

@song_bot.message_handler(content_types=["text"])
def get_song(message):
    mssg = message.text
    # replaced_song = mssg.replace(" ", "+")
    # song_bot.send_message(message.chat.id, f"{replaced_song}")
    song_bot.send_message(message.chat.id, "Wait a minute...")

    driver.get("https://www.pisni.org.ua/")
    input_box = driver.find_element_by_class_name("nav_input")
    input_box.send_keys(mssg)

    input_button = driver.find_element_by_class_name("icon-tb pisni-icon-search-24")
    input_button.click()

    page = driver.find_element_by_tag_name("body").text
    song_bot.send_message(message.chat.id, page)

    songs = driver.find_elements_by_class_name("li")

    for i in songs:
        song_bot.send_message(message.chat.id, i.text)

#-----------------------------------GOOGLE------------------------------------------------------------------------
#     driver.get(f"https://www.google.com/search?q={replaced_song}+lyrics")
#     page_google = driver.find_element_by_tag_name("body").text
#
#     str_text = page_google
#     if "Knowledge Result" in str_text and "Source:" in str_text:
#         start_index = str_text.index("Knowledge Result")
#         last_index = str_text.index("Source:")
#
#         result_text = str_text[start_index: last_index]
#         song_bot.send_message(message.chat.id, result_text)
#
# #--------------------------------------PISNI.UA------------------------------------------------------------------
#     else:
#
#         driver.get(f"https://www.google.com/search?q={replaced_song}+lyrics+pisni.ua")
#         driver.get(driver.find_element_by_xpath("/html/body/div[7]/div/div[10]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/a").get_attribute("href"))
#         page = driver.find_elements_by_css_selector("p")
#
#         if page:
#             full_text = ""
#             for i in page:
#                 full_text += i.text + "\n"
#             song_bot.send_message(message.chat.id, full_text)
#
#         else:
#             driver.get(f"https://www.google.com/search?q={replaced_song}+lyrics+genius")
#             driver.get(driver.find_element_by_xpath("/html/body/div[7]/div/div[10]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/a").get_attribute("href"))
#             page = driver.find_element_by_tag_name("body").text
#
#             str_text = page
#             if "Featuring" in str_text and "About" in str_text:
#                 start_index = str_text.index("Featuring")
#                 last_index = str_text.index("About")
#
#                 result_text = str_text[start_index: last_index]
#                 song_bot.send_message(message.chat.id, result_text)
#             else:
#                 song_bot.send_message(message.chat.id, "Bot can't find song lyrics")




song_bot.infinity_polling()