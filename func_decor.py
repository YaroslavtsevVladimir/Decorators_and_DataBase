#!

""" Decorators and data base."""

import requests
import sqlite3
import random
from lxml import html
from functools import wraps

url = "https://www.yandex.ru"
conn = sqlite3.connect("site_checked.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS randtext(url text, attribute_text text)")
conn.commit()


def cached(func):
    """
    Decorator, who checked url in database.
    If the url is in the database, it return
    the text line from the table, otherwise
    the text is taken from the get_random_text(address).
    :param func: get_random_text.
    :return: text from selected site.
    """

    @wraps(func)
    def wrapper(address):
        sql = "SELECT * FROM randtext WHERE url=?"
        cur.execute(sql, [url])
        info_list = cur.fetchall()
        if not info_list:
            func(address)
            return cur.execute("INSERT INTO randtext VALUES (?, ?)", (address, str(func(address))))
        else:
            result = info_list[0][1]
            return result
    return wrapper


@cached
def get_random_text(address):
    """
    Get random text in all HTML page.
    :param address: some url.
    :return: randomly selected text
    from the entire text.
    """

    page_html = requests.get(address).content.decode('utf-8')
    tree = html.fromstring(page_html)
    all_text = tree.xpath('./body//*/@id')
    rand_txt = random.choice(all_text)
    return rand_txt


def main():
    get_random_text(url)


if __name__ == '__main__':

    main()
    conn.commit()
    conn.close()
