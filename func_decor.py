#!

""" Decorators and data base."""

import requests
import sqlite3
import random
from lxml import html


def get_random_text(address):
    """
    Get random text in all HTML page.
    :param address: some url.
    :return: randomly selected text
    from the entire text.
    """

    page_html = requests.get(address).content.decode('utf-8')
    tree = html.fromstring(page_html)
    all_text = tree.xpath('./body//*/text()')
    rand_txt = random.choice(all_text)
    return rand_txt


def write_data_to_database(func):
    """
    Decorator, who write result of
    get_random_text(address) in database.
    :param func: get_random_text.
    :return: decorator1
    """

    def decorator1(address):
        cursor.execute("INSERT INTO randtext VALUES (?, ?)", (address, func(address)))
        conn.commit()
    return decorator1


def check_url_in_database(func):
    """
    Decorator, who checked url in database.
    If the url is in the database, it return
    all the 'text' lines from the table, otherwise
    th text is taken from the get_random_text(address)
    :param func: get_random_text(address)
    :return: text or list with 'text' lines.
    """

    def decorator2(address):
        sql = "SELECT * FROM randtext WHERE url=?"
        cursor.execute(sql, [url])
        info_lsit = cursor.fetchall()
        result = []
        for site in info_lsit:
            if address in site:
                sql = "SELECT text FROM randtext WHERE url=?"
                cursor.execute(sql, [url])
                txt_list = cursor.fetchall()
                result = [txt_list[i][0] for i in range(len(txt_list))]
                return result
            else:
                return func(address)
    return decorator2


def main():
    print(get_random_text(url))
    write_data = write_data_to_database(get_random_text)
    write_data(url)
    check_data = check_url_in_database(get_random_text)
    print(check_data(url))


if __name__ == '__main__':
    url = 'https://www.yandex.ru'
    conn = sqlite3.connect("site_checked.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE  IF NOT EXISTS randtext ('url', 'text')""")
    conn.commit()

    main()
    conn.commit()
    conn.close()
