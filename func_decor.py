#!

""" Decorators and data base."""

import requests
import sqlite3
import random
from lxml import html


url = 'https://www.google.com'
conn = sqlite3.connect("site_checked.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS randtext (url text, attribute_text text)")
conn.commit()


def write_data_to_database(func):
    """
    Decorator, who write result of
    get_random_text(address) in database.
    :param func: get_random_text.
    :return: decorator1
    """

    def decorator1(address):
        cur.execute("INSERT INTO randtext VALUES (?, ?)", (address, str(func(address))))
        conn.commit()
    return decorator1


def check_url_in_database(func):
    """
    Decorator, who checked url in database.
    If the url is in the database, it return
    all the 'text' lines from the table, otherwise
    the text is taken from the get_random_text(address).
    :param func: get_random_text.
    :return: text or list with 'text' lines.
    """

    def decorator2(address):
        sql = "SELECT * FROM randtext WHERE url=?"
        cur.execute(sql, [url])
        info_list = cur.fetchall()
        for line in info_list:
            if address in line:
                sql = "SELECT attribute_text FROM randtext WHERE url=?"
                cur.execute(sql, [url])
                txt_list = cur.fetchall()
                result = [txt_list[i][0] for i in range(len(txt_list))]
                return result
            else:
                return func(address)
    return decorator2


@write_data_to_database
@check_url_in_database
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
