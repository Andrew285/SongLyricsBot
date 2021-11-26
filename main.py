import telebot
from bs4 import BeautifulSoup
import requests
import os
from selenium import webdriver   # for webdriver
from telebot import types
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

counter_song = 0
song_links = None
page_url = None
@song_bot.message_handler(content_types=["text"])
def get_song(message):
    global counter_song
    global page_url
    mssg = message.text
    # replaced_song = mssg.replace(" ", "+")
    # song_bot.send_message(message.chat.id, f"{replaced_song}")
    song_bot.send_message(message.chat.id, "Wait a minute...")

    driver.get("https://www.pisni.org.ua/")

    # page = driver.find_element_by_tag_name("body").text
    # song_bot.send_message(message.chat.id, page)

    input_box = driver.find_element_by_xpath("/html/body/div[1]/table/tbody/tr/td[10]/input[1]")
    input_box.send_keys(f"{mssg}")

    input_button = driver.find_element_by_xpath("/html/body/div[1]/table/tbody/tr/td[10]/a[1]")
    input_button.click()

    page_url = driver.current_url

    # page = driver.find_element_by_tag_name("body").text
    # song_bot.send_message(message.chat.id, page)

    # song_links = driver.find_elements_by_class_name("li")

    # for i in songs:
    #     song_bot.send_message(message.chat.id, i.text)

    driver.get(driver.find_element_by_xpath(f"/html/body/table[2]/tbody/tr/td[1]/div/table[2]/tbody/tr[{counter_song+2}]/td[1]/a").get_attribute("href"))
    song_text = driver.find_element_by_class_name("songwords").text

    menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    menu.add(types.KeyboardButton("Previous"),
                   types.KeyboardButton("Next"))
    user_choice = song_bot.send_message(message.chat.id, f"{song_text}", reply_markup=menu)
    song_bot.register_next_step_handler(user_choice, choose_song_action)

def choose_song_action(message):
    global page_url
    global counter_song
    if message.text == "Next":
        counter_song += 1
        driver.get(f"{page_url}")
        driver.get(driver.find_element_by_xpath(f"/html/body/table[2]/tbody/tr/td[1]/div/table[2]/tbody/tr[{counter_song+2}]/td[1]/a").get_attribute("href"))
        song_text = driver.find_element_by_class_name("songwords").text

        menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        menu.add(types.KeyboardButton("Previous"),
                 types.KeyboardButton("Next"))
        user_choice = song_bot.send_message(message.chat.id, f"{song_text}", reply_markup=menu)
        song_bot.register_next_step_handler(user_choice, choose_song_action)

    elif message.text == "Previous":
        if counter_song > 0:
            counter_song -= 1
            driver.get(f"{page_url}")
            driver.get(driver.find_element_by_xpath(f"/html/body/table[2]/tbody/tr/td[1]/div/table[2]/tbody/tr[{counter_song + 2}]/td[1]/a").get_attribute("href"))
            song_text = driver.find_element_by_class_name("songwords").text

            menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            menu.add(types.KeyboardButton("Previous"),
                     types.KeyboardButton("Next"))
            user_choice = song_bot.send_message(message.chat.id, f"{song_text}", reply_markup=menu)
            song_bot.register_next_step_handler(user_choice, choose_song_action)
        else:
            song_bot.answer_callback_query(message.chat.id, "There is no previous song")


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