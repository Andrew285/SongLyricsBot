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

@song_bot.message_handler(content_types=["text"])
def get_singer(message):
    global replaced_singer
    mssg = message.text
    replaced_singer = mssg.replace(" ", "+")
    msg = song_bot.send_message(message.chat.id, "Now enter the song name:")
    song_bot.register_next_step_handler(msg, get_song)

def get_song(message):
    global replaced_singer
    mssg = message.text
    replaced_song = mssg.replace(" ", "+")
    song_bot.send_message(message.chat.id, f"{replaced_singer}+{replaced_song}")

#-----------------------------------GOOGLE------------------------------------------------------------------------
    # page_google = requests.get(f"https://www.google.com/search?q={replaced_singer}+{replaced_song}+lyrics", headers=headers)
    # page_google = requests.get(f"https://www.google.com/search?q={replaced_singer}+{replaced_song}+lyrics", headers=headers)
    driver.get(f"https://www.google.com/search?q={replaced_singer}+{replaced_song}+lyrics")
    page_google = driver.find_element_by_tag_name("body").text
    song_bot.send_message(message.chat.id, "Page_Google")
    # if page_google:
    #     song_bot.send_message(message.chat.id, f"{page_google.status_code}")
    # else:
    #     song_bot.send_message(message.chat.id,"No request")
    # page_google = requests.get(f"https://www.vpnmentor.com/tools/search-from/{replaced_singer}+{replaced_song}+lyrics", headers=headers)
    # soup = BeautifulSoup(page_google.text, "lxml")
    # if soup:
    #     song_bot.send_message(message.chat.id,"Soup")
    # elif soup is None:
    #     song_bot.send_message(message.chat.id,"None")
    # elif soup == "":
    #     song_bot.send_message(message.chat.id,"Empty")
    # else:
    #     song_bot.send_message(message.chat.id,"Error")

    str_text = page_google
    song_bot.send_message(message.chat.id, str_text)
    # if str_text:
    #     song_bot.send_message(message.chat.id, str_text[:150])
    # else:
    #     song_bot.send_message(message.chat.id, "Problem")
    if "Knowledge Result" in str_text and "Source:" in str_text:
        start_index = str_text.index("Knowledge Result")
        last_index = str_text.index("Source:")

        result_text = str_text[start_index: last_index]
        song_bot.send_message(message.chat.id, result_text)

#--------------------------------------PISNI.UA------------------------------------------------------------------
    else:
        song_bot.send_message(message.chat.id, "Error")
#         page_pisni = requests.get(f"https://www.google.com/search?q={replaced_singer}+{replaced_song}+lyrics+pisni.org.ua")
#         song_bot.send_message(message.chat.id, "page_pisni")
#         if page_pisni:
#             song_bot.send_message(message.chat.id, f"{page_pisni.status_code}")
#         else:
#             song_bot.send_message(message.chat.id, "No request")
#         # page_pisni = requests.get(f"https://www.vpnmentor.com/tools/search-from/{replaced_singer}+{replaced_song}+lyrics+pisni.org.ua", headers=headers)
#         soup = BeautifulSoup(page_pisni.text, "lxml")
#
#         # str_text = soup.text
#         first_link = soup.find_all("a")[17]['href']
#         new_page = requests.get(f"https://www.google.com/{first_link}")
#         new_soup = BeautifulSoup(new_page.text, "lxml")
#
#         str_text = new_soup.text
#         if "Друк" in str_text and "ІНФОРМАЦІЯ" in str_text:
#             # print(str_text)
#             start_index = str_text.index(f"Друк") + 4
#             last_index = str_text.index(f"ІНФОРМАЦІЯ")
#             result_text = str_text[start_index:last_index].strip()
#             song_bot.send_message(message.chat.id, result_text)
#
# #-------------------------------------------AZLYRICS---------------------------------------------------------------
#         else:
#             page_az = requests.get(f"https://www.google.com/search?q={replaced_singer}+{replaced_song}+lyrics+azlyrics", headers=headers)
#             song_bot.send_message(message.chat.id, "page_az")
#             if page_az:
#                 song_bot.send_message(message.chat.id, f"{page_az.status_code}")
#             else:
#                 song_bot.send_message(message.chat.id, "No request")
#             # page_az = requests.get(f"https://www.vpnmentor.com/tools/search-from/{replaced_singer}+{replaced_song}+azlyrics")
#
#             soup = BeautifulSoup(page_az.text, "lxml")
#
#             # str_text = soup.text
#             first_link = soup.find_all("a")[17]['href']
#             new_page = requests.get(f"https://www.google.com/{first_link}")
#             new_soup = BeautifulSoup(new_page.text, "lxml")
#
#             str_text = new_soup.text
#             if "Текст пісні" in str_text and "Writers" in str_text:
#                 # print(str_text)
#                 start_index = str_text.index(f"Текст пісні") + 4
#                 last_index = str_text.index(f"Writers")
#                 result_text = str_text[start_index:last_index].strip()
#                 song_bot.send_message(message.chat.id, result_text)
#
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