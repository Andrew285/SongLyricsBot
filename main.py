import telebot
from bs4 import BeautifulSoup
import requests
import os
from selenium import webdriver   # for webdriver
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
    replaced_song = mssg.replace(" ", "+")
    song_bot.send_message(message.chat.id, f"{replaced_song}")

#-----------------------------------GOOGLE------------------------------------------------------------------------
    driver.get(f"https://www.google.com/search?q={replaced_song}+lyrics")
    page_google = driver.find_element_by_tag_name("body").text

    str_text = page_google
    if "Knowledge Result" in str_text and "Source:" in str_text:
        start_index = str_text.index("Knowledge Result")
        last_index = str_text.index("Source:")

        result_text = str_text[start_index: last_index]
        song_bot.send_message(message.chat.id, result_text)

#--------------------------------------PISNI.UA------------------------------------------------------------------
    else:

        driver.get(f"https://www.google.com/search?q={replaced_song}+lyrics+pisni.ua")
        driver.get(driver.find_element_by_xpath("/html/body/div[7]/div/div[10]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/a").get_attribute("href"))
        page = driver.find_element_by_tag_name("body").text

        str_text = page
        song_bot.send_message(message.chat.id, str_text)
        if "А-Я" in str_text and "Оцініть" in str_text:
            start_index = str_text.index("А-Я")
            last_index = str_text.index("Оцініть")

            result_text = str_text[start_index: last_index]
            song_bot.send_message(message.chat.id, result_text)

#-------------------------------------------AZLYRICS---------------------------------------------------------------
        # else:
        #     driver.get(f"https://www.google.com/search?q={replaced_singer}+{replaced_song}+lyrics+azlyrics")
        #     driver.get(driver.find_element_by_xpath("/html/body/div[7]/div/div[10]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/a").get_attribute("href"))
        #     page = driver.find_element_by_tag_name("body").text
        #
        #     str_text = page
        #     song_bot.send_message(message.chat.id, str_text)
        #     if "А-Я" in str_text and "Оцініть цю пісню" in str_text:
        #         start_index = str_text.index("А-Я")
        #         last_index = str_text.index("Оцініть цю пісню")
        #
        #         result_text = str_text[start_index: last_index]
        #         song_bot.send_message(message.chat.id, result_text)
#------------------------------------------------------------GENIUS-------------------------------------------------------------
        else:
            driver.get(f"https://www.google.com/search?q={replaced_song}+lyrics+genius")
            driver.get(driver.find_element_by_xpath("/html/body/div[7]/div/div[10]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/a").get_attribute("href"))
            page = driver.find_element_by_tag_name("body").text

            str_text = page
            if "Featuring" in str_text and "About" in str_text:
                start_index = str_text.index("Featuring")
                last_index = str_text.index("About")

                result_text = str_text[start_index: last_index]
                song_bot.send_message(message.chat.id, result_text)
            else:
                song_bot.send_message(message.chat.id, "Bot can't find song lyrics")
# #------------------------------------------ON-HIT---------------------------------------------------------------
#             else:
#                 page_hit = requests.get(f"https://www.google.com/search?q={replaced_singer}+{replaced_song}+lyrics", headers=headers)
#                 song_bot.send_message(message.chat.id, "page_hit")
#                 if page_hit:
#                     song_bot.send_message(message.chat.id, f"{page_hit.status_code}")
#                 else:
#                     song_bot.send_message(message.chat.id, "No request")
#                 # page_hit = requests.get(f"https://www.vpnmentor.com/tools/search-from/{replaced_singer}+{replaced_song}+lyrics")
#                 soup = BeautifulSoup(page_hit.text, "lxml")
#
#                 # str_text = soup.text
#                 first_link = soup.find_all("a")[17]['href']
#                 new_page = requests.get(f"https://www.google.com/{first_link}")
#                 new_soup = BeautifulSoup(new_page.text, "lxml")
#
#                 str_text = new_soup.text
#                 # print(str_text)
#                 if "Поиск" in str_text and "Тексты песен" in str_text:
#                     start_index = str_text.index(f"Поиск") + 7
#                     last_index = str_text.index(f"Тексты песен")
#                     result_text = str_text[start_index:last_index].strip()
#                     song_bot.send_message(message.chat.id, result_text)
#
# #----------------------------------------------------GENIUS-------------------------------------------------------------
#                 else:
#                     page_genius = requests.get(f"https://www.google.com/search?q={replaced_singer}+{replaced_song}+lyrics+genius", headers=headers)
#                     song_bot.send_message(message.chat.id, "page_genius")
#                     if page_genius:
#                         song_bot.send_message(message.chat.id, f"{page_genius.status_code}")
#                     else:
#                         song_bot.send_message(message.chat.id, "No request")
#                     # page_genius = requests.get(f"https://www.vpnmentor.com/tools/search-from/{replaced_singer}+{replaced_song}+lyrics+genius")
#                     soup = BeautifulSoup(page_genius.text, "lxml")
#
#                     first_link = soup.find_all("a")[17]['href']
#                     new_page = requests.get(f"https://www.google.com/{first_link}")
#                     new_soup = BeautifulSoup(new_page.text, "lxml")
#
#                     str_text = new_soup.text
#                     # print(str_text)
#                     if "LYRICS" in str_text and "MORE ON GENIUS" in str_text:
#                         start_index = str_text.index(f"LYRICS") + 7
#                         last_index = str_text.index(f"MORE ON GENIUS")
#                         result_text = str_text[start_index:last_index].strip()
#                         song_bot.send_message(message.chat.id, result_text)
#                     else:
#                         song_bot.send_message(message.chat.id, "Bot can't find the song lyrics")
song_bot.infinity_polling()