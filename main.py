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

counter_song = 0
song_links = None
page_url = None
@song_bot.message_handler(content_types=["text"])
def get_song(message):
    global counter_song
    global page_url
    mssg = message.text
    song_bot.send_message(message.chat.id, "Wait a minute...")

    driver.get("https://www.pisni.org.ua/")

    input_box = driver.find_element_by_xpath("/html/body/div[1]/table/tbody/tr/td[10]/input[1]")
    input_box.send_keys(f"{mssg}")

    input_button = driver.find_element_by_xpath("/html/body/div[1]/table/tbody/tr/td[10]/a[1]")
    input_button.click()

    page_url = driver.current_url

    driver.get(driver.find_element_by_xpath(f"/html/body/table[2]/tbody/tr/td[1]/div/table[2]/tbody/tr[{counter_song+2}]/td[1]/a").get_attribute("href"))
    song_text = driver.find_element_by_class_name("songwords").text

    menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    menu.add(types.KeyboardButton("Previous"),
                   types.KeyboardButton("Next"),
                    types.KeyboardButton("Song Words"),
             types.KeyboardButton("Author + Song Name"))
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
                 types.KeyboardButton("Next"),
                 types.KeyboardButton("Search By Words"),
                 types.KeyboardButton("Author + Song Name"))
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
                     types.KeyboardButton("Next"),
                     types.KeyboardButton("Search By Words"),
                     types.KeyboardButton("Author + Song Name"))
            user_choice = song_bot.send_message(message.chat.id, f"{song_text}", reply_markup=menu)
            song_bot.register_next_step_handler(user_choice, choose_song_action)
        else:
            song_bot.send_message(message.chat.id, "There is no previous song")

    elif message.text == "Search By Words":
        counter_song = 0
        song_bot.send_message(message.chat.id, "Type words:")
        song_bot.register_next_step_handler(message.text, get_song)

    elif message.text == "Author + Song Name":
        counter_song = 0
        user_song = song_bot.send_message(message.chat.id, "Type:")
        song_bot.register_next_step_handler(user_song, get_song_az)

def get_song_az(message):
    mssg = message.text
    song_bot.send_message(message.chat.id, "Wait a minute...")

    driver.get("https://www.azlyrics.com/")

    input_box = driver.find_element_by_xpath("/html/body/nav[1]/div/div[2]/form/div/div/input")
    input_box.send_keys(f"{mssg}")

    input_button = driver.find_element_by_xpath("/html/body/nav[1]/div/div[2]/form/div/span/button")
    input_button.click()

    # page_url = driver.current_url

    driver.get(driver.find_element_by_xpath(f"/html/body/div[2]/div/div/div/table/tbody/tr[1]/td/a").get_attribute("href"))
    song_text = driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[5]").text

    menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    menu.add(types.KeyboardButton("Previous"),
             types.KeyboardButton("Next"),
             types.KeyboardButton("Song Words"),
             types.KeyboardButton("Author + Song Name"))
    user_choice = song_bot.send_message(message.chat.id, f"{song_text}", reply_markup=menu)
    song_bot.register_next_step_handler(user_choice, choose_song_action)

song_bot.infinity_polling()