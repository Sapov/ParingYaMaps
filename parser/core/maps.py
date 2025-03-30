import json
import time
import random

import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from parser.models import Links, Category, City

# from async_parse_site import run as parser_site
# import json_to_excel


class Parse:
    def __init__(self, location: str, organisation: str):
        self.item = None
        self.organisation = organisation
        self.location = location
        self.url = f'https://yandex.ru/maps/193/voronezh/search/{self.organisation} {location}'

        self.version_main = 134
        self.data = []
        self.elements = []
        self.link_list_items = []

    def __set_up(self):
        # '''no images'''
        options = Options()
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # options.add_experimental_option("prefs", prefs)  # без картинок"
        options.add_argument("--headless=new")
        self.driver = uc.Chrome(version_main=self.version_main, options=options)

    def __get_url(self):
        self.driver.get(self.url)

    def parse_page(self):
        """Получаем блоки элементов"""
        preview_count = elements_new = count = 0
        # while True:
        while count < 6:
            elements_new = self.driver.find_elements(By.CSS_SELECTOR, ".search-snippet-view")
            '''Прокрутка вниз'''
            self.driver.execute_script("arguments[0].scrollIntoView(true);", elements_new[-1])
            time.sleep(random.randint(0, 4))
            elements_new = self.driver.find_elements(By.CSS_SELECTOR, ".search-snippet-view")
            count = len(elements_new)
            print("COUNT=", count)
            if preview_count == count:
                break
            preview_count = count
        self.elements.extend(elements_new)
        print(len(self.elements), 'Элементов')
        self.__link_list()

    def __link_list(self):
        ''' Получаем ссылку, название, рейтинг, и количество оценок'''
        for i in self.elements:
            try:
                link = i.find_element(By.CSS_SELECTOR, '.search-snippet-view .link-overlay').get_attribute('href')
                print(link)
            except:
                print('NO link')
                print('Нет селектора:  ССЫЛКА')
                link = ''
            try:
                title = i.find_element(By.CSS_SELECTOR, '.search-business-snippet-view__title').text
            except:
                print('Нет селектора: НаЗвание')
                title = ''
            try:
                rating_yandex = i.find_element(By.CSS_SELECTOR, '.business-rating-badge-view__rating-text').text
            except:
                print('Нет селектора:  Рейтинг')
                rating_yandex = ''
            try:
                estimation = i.find_element(By.CSS_SELECTOR, '.business-rating-amount-view').text
            except:
                print('Наверно нет такого селектора: Оценки')
                estimation = ''
            item = {'link': link,
                    'title': title,
                    'rating_yandex': rating_yandex,
                    'estimation': estimation
                    }
            category = Category.objects.create(name_category = self.organisation)
            city = City.objects.create(name_city = self.location)
            Links.objects.update_or_create(category = category, сity_name=city, link=link, title=title, rate=rating_yandex, estimation=estimation)
            self.link_list_items.append(item)
        print('В СЛОВАРЕ: ', len(self.link_list_items))
        self.__save_data(self.link_list_items, 'links.json')
        for i in self.link_list_items:
            print('list item:', i)

        self.__open_page()

    def __open_page(self):
        '''Получаем со страницы телефон, адрес, сайт'''
        for index, val in enumerate(self.link_list_items):
            time.sleep(random.randint(1, 5))
            try:
                items = {} | val
                self.driver.get(val['link'])
                items.setdefault('name', self.driver.find_element(By.TAG_NAME, 'H1').text)
                items.setdefault('phone',
                                 self.driver.find_element(By.CSS_SELECTOR, '.orgpage-phones-view__phone-number').text)
                items.setdefault('address',
                                 self.driver.find_element(By.CSS_SELECTOR, '.orgpage-header-view__address').text)
                try:
                    items.setdefault('site',
                                     self.driver.find_element(By.CSS_SELECTOR, '.business-urls-view__text').text)
                except:
                    items['site'] = ''
                category, created = Category.objects.get_or_create(name_category=self.organisation)
                if created:
                    print('Категория создана')
                else:
                    print('Категория уже существует')

                city = City.objects.create(name_city=self.location)
                Links.objects.update_or_create(category=category,
                                               сity_name=city,
                                               link=items['link'],
                                               title=items['title'],
                                               rate=items['rating_yandex'],
                                               phone=items['phone'],
                                               address=items['address'],
                                               site=items['site'],
                                               )
                self.data.append(items)
                print(items, '\n', '*' * 10)
            except:
                print('Какая то ошибка')
        self.__save_data(self.data, 'test_site.json')

    def __save_data(self, data: list, name_file: str):
        with open(name_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def run(self):
        self.__set_up()
        self.__get_url()
        self.parse_page()
        # parser_site(self.data)
        # json_to_excel.main(self.organisation)
