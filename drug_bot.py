"""Import everything required for parsing"""
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup

from aiogram import Bot, Dispatcher, types


class DrugBot:
    """Class that manages all drug bot logic"""


    def __init__(self):
        self.token = "PLACE YOUR TOKEN HERE"
        self.bot = Bot(token=self.token, parse_mode="HTML")
        self.dp = Dispatcher()
        self.target_url = 'http://www.omdrug.ru/information/drugs.php?find='


    def run(self):
        """Method that starts the bot"""
        self.dp.run_polling(self.bot)


    async def handle_message(self, message: types.Message):
        """Method that replies with a list of 10 cheapest drugs"""
        # Request all lines
        request_session = requests.Session()
        headers = {'User-Agent': 'Mozilla/5.0'}
        to_find = quote_plus(message.text)
        result = request_session.post(self.target_url + to_find, headers=headers)
        # Parse results from site
        table_body = self.parse_website_base(result.text)
        answer = self.parse_lines(table_body)
        await message.reply(answer)


    def parse_website_base(self, html):
        """Function that returns table containing lines with drugs in it"""
        soup = BeautifulSoup(html, "html.parser")
        table_holder = soup.find("div", {"id": "table_drugs_stores"})
        table = table_holder.find("table", {"class": "big_tab"})
        return table.findChildren("tbody")[0]


    def parse_lines(self, table_body):
        """Method that parses 10 lines and combines them into formatted answer"""
        index = 0
        result = ""
        for element in table_body.findChildren("tr"):
            if index == 0:
                index += 1
                continue
            children = element.findChildren("td")
            name = children[0].text
            location = children[1].findChildren("a")[0].text
            price = children[2].text
            result += name + "\nАдрес: " + location
            result += " \nЦена: " + price + " руб.\n\n"
            index += 1
            if index >= 10:
                break
        return result
