from fake_headers import Headers
from pprint import pprint
import requests 
import bs4
from tqdm import tqdm

data_perfumes = []
# создаем пустой список 

for el in tqdm(range(1,5), desc="Обработка данных"):
    # в цикле будем проходить по страничкам
    iledebeaute = f'https://iledebeaute.ru/catalog/parfyumeriya/tip-has_discount-iz-prom/?utm_source=yandex&utm_medium=cpc&utm_campaign=pc_rf_p_tgo_brand_ile_de_beaute_old%7C113321203&utm_content=ST%3Asearch%7CS%3Anone%7CAP%3Ano%7CPT%3Apremium%7CP%3A1%7CDT%3Adesktop%7CRI%3A55%7CRN%3AТюмень%7CCI%3A113321203%7CGI%3A5476724696%7CPI%3A52666066770%7CAI%3A16382255100%7CKW%3A---autotargeting%7CMT%3A%7CMK%3A&utm_term=---autotargeting&referrer=reattribution%3D1&yclid=8570866345276866559&page={el}'
    # формируем URL
    respons = requests.get(iledebeaute, headers=Headers(browser='chrome', os='win').generate())
    # делаем get запрос
    soup = bs4.BeautifulSoup(respons.text,features='lxml')
    # создаем обхек парсинга
    perfumes_list = soup.find_all('div', class_='css-79elbk css-mwukus')
    # находим все товары
    for perfume in perfumes_list:
        # в цикле проходимся по каждому товару
        price_no_discount = perfume.find('div',class_='css-1slxu8').text.strip().replace('¤', '').replace('\xa0', ' ')
        # цена без скидки
        price_discount = perfume.find('div',class_='css-1svydga').text.strip().replace('¤', '').replace('\xa0', ' ')
        # цена со скидкой 
        discount = perfume.find('div',class_='css-1jj7j4t').text.strip()
        # сколько составляет скидка
        brand = perfume.find('div',class_='css-10alpk0 css-mwukus').text.strip()
        # бренд товара
        title = perfume.find('div',class_='css-14k4spz css-mwukus')['title']
        # названия товара
        volume = perfume.find('div',class_='css-yj7sn4 css-mwukus')
        if volume:
            volume = volume.text.strip()
        # сколько МЛ в товаре
        else: ''
        data_perfumes.append({
            'Бренд':brand,
            'Модель' : title,
            'Объем' : volume,
            'Цена без скидки' : price_no_discount,
            'Цена со скидкой' : price_discount,
            'Скидка' : discount
            })
        # формируем словарь
        
pprint(data_perfumes) 
# выводим весьсписок товара
print(f'Всего товара: {len(data_perfumes)}')
# выводим колличество тавара 