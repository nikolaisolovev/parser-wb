import requests
import re
import csv
from models import Items


class ParseWB:
    def __init__(self, url: str):
        self.brand_id = self.__get_brand_id(url)

    @staticmethod
    def __get_brand_id(url: str):
        regex = "(?<=brand=)\d+"
        brand_id = re.search(regex, url)[0]

        return brand_id

    def parse(self):
        page_number = 1
        self.__create_csv()
        while True:
            response = requests.get(
                f'https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=control&TestID=237&appType=1&curr=rub&dest=-1257786&fbrand={self.brand_id}&page={page_number}&query=%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%D0%BA%D0%B0%D1%80%D1%82%D0%B0&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,1,31,66,110,48,22,71,114&resultset=catalog&sort=popular&spp=33&suppressSpellcheck=false',
            )
            page_number += 1
            items_info = Items.model_validate(response.json()['data'])
            if not items_info.products:
                break
            self.__save_csv(items_info)

    def __create_csv(self):
        with open('wb_data.csv', mode='w', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'название', 'цена', 'бренд', 'продаж', 'рейтинг', 'в наличии'])

    def __save_csv(self, items):
        with open('wb_data.csv', mode='a', newline="") as file:
            writer = csv.writer(file)

            for product in items.products:
                writer.writerow(
                    [product.id,
                     product.name,
                     product.salePriceU,
                     product.brand,
                     product.sale,
                     product.rating,
                     product.volume]
                                )


if __name__ == '__main__':
    ParseWB('https://www.wildberries.ru/catalog/0/search.aspx?page=1&sort=popular&search=%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%D0%BA%D0%B0%D1%80%D1%82%D0%B0&fbrand=27445').parse()
