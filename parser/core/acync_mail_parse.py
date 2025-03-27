import json
import re
import time

import aiohttp
import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup as bs


async def get_page(item: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        print(item)
        try:
            if item['site'] != '':
                url = f"http://{item['site']}"
                async with session.get(url, ssl=False) as result:
                    try:
                        if result.status == 200:
                            page = await result.text()
                            print(f'Данные со страницы {url}')
                            item['mail'] = search_mail(page)
                            item['whatsapp'] = search_wa_me(page)
                            item['telegram'] = search_telega(page)

                        return item
                    except:
                        print('Нет данных')
        except:
            print('Сайт не ответил')


def search_mail(page):
    soup = bs(page, "html.parser")
    emails = set()
    for index, link in enumerate(soup.find_all("a", attrs={"href": re.compile("^mailto:")})):
        # Достаём email-адреса из тегов с mailto
        email = link.get("href").replace("mailto:", "")
        emails.add(email)
    to_mail = search_mail_in_text(soup.text)
    emails.add(to_mail)
    print('Почта со страницы', emails)

    print('=' * 30)
    return list(emails) if len(emails) != 0 else []


def search_mail_in_text(text):
    mailre = re.compile(r'[a-zA-Z0-9._%+-]+@+[a-zA-Z0-9._%+-]+(\.[a-zA-Z]{2,4})')
    mo = mailre.search(text)
    print(mo.group() if mo else '')
    return mo.group() if mo else ''


def search_wa_me(page):
    whatsapp = re.compile(r'https:\/\/wa.me\/\d{11}')
    whatsapp_2 = re.compile(r'https:\/\/wa.clck.bar\/\w+')
    mo = whatsapp.findall(page)
    mo1 = whatsapp_2.findall(page)
    lst = list(set(mo + mo1))
    print('НОМЕР WHATSSAPP', lst)
    return lst


def search_telega(page):
    telega = re.compile(r'https:\/\/t.me\/\w+')
    mo = telega.findall(page)
    lst = list(set(mo))
    print('НОМЕР TETELGRAMM', lst, '\n')
    return lst


def open_file():
    with open('scv_json/test_site.json', 'r', encoding='utf-8') as file:
        json_items = json.load(file)
        print(json_items)
        return json_items


def save_data(new_list):
    with open(f'scv_json/temp_mail.json', 'w', encoding='utf-8') as file:
        json.dump(new_list, file, ensure_ascii=False, indent=4)


async def main():
    items = [i for i in open_file()]
    requests = [get_page(item) for item in items]
    lst = await asyncio.gather(*requests)
    save_data(lst)
    print(lst)


def run():
    start = time.time()
    asyncio.run(main())
    print('Время выполнения: ', time.time() - start)

if __name__ == '__main__':
    run()