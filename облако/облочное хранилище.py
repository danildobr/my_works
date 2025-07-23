#                Курсовая работа «Резервное копирование»
# Возможна такая ситуация, что мы хотим показать друзьям фотографии из социальных сетей, но соц. сети могут
# быть недоступны по каким-либо причинам. Давайте защитимся от такого.
# Нужно написать программу для резервного копирования фотографий с профиля(аватарок) пользователя vk в
# облачное хранилище Яндекс.Диск.
# Для названий фотографий использовать количество лайков, если количество лайков одинаково, то добавить дату загрузки.
# Информацию по сохраненным фотографиям сохранить в json-файл.

# Задание:
# Нужно написать программу, которая будет:
# Получать фотографии с профиля. Для этого нужно использовать метод photos.get.
# Сохранять фотографии максимального размера(ширина/высота в пикселях) на Я.Диске.
# Для имени фотографий использовать количество лайков.
# Сохранять информацию по фотографиям в json-файл с результатами.
# Обратите внимание: инструкция для получения токена для ВК находится в вашем личном кабинете в итоговом блоке по модулю.

# Входные данные:
# Пользователь вводит:

# id пользователя vk;
# токен с Полигона Яндекс.Диска. Важно: Токен публиковать в github не нужно!
# Выходные данные:
# json-файл с информацией по файлу:
#     [{
#     "file_name": "34.jpg",
#     "size": "z"
#     }]
# Измененный Я.диск, куда добавились фотографии.​​
# Обязательные требования к программе:
# Использовать REST API Я.Диска и ключ, полученный с полигона.
# Для загруженных фотографий нужно создать свою папку.
# Сохранять указанное количество фотографий(по умолчанию 5) наибольшего размера (ширина/высота в пикселях) на Я.Диске
# Сделать прогресс-бар или логирование для отслеживания процесса программы.
# Код программы должен удовлетворять PEP8.
# У программы должен быть свой отдельный репозиторий.
# Все зависимости должны быть указаны в файле requiremеnts.txt.​
# Необязательные требования к программе:
# Сохранять фотографии и из других альбомов.
# Сохранять фотографии на Google.Drive.
from tqdm import tqdm
import requests
import json
import configparser


class VK_API:
    def __init__(self, access_token, api_version='5.199'):
        self.access_token = access_token
        self.api_version = api_version
        self.base_url = 'https://api.vk.com/method'
                
    def _resolve_user_id(self, identifier):
        """Определяет user_id по screen_name или ID"""
        try:
            if not str(identifier).isdigit():
                url = f'{self.base_url}/users.get'
                params = {
                    'user_ids': identifier,
                    'access_token': self.access_token,
                    'v': self.api_version
                    }
                response = requests.get(url, params=params)
                data = response.json()
                return data['response'][0]['id']
            return int(identifier)
        except (KeyError, IndexError) as e:
            raise Exception(f'Ошибка обработки данных screen_name или ID: {e}')
                
    def my_foto(self, identifier, album='wall'):
        '''получаем json файл с нашими фотографиями'''
        try:
            user_id = self._resolve_user_id(identifier)
            vk_url = f'{self.base_url}/photos.get'
            params = {
                'owner_id': user_id,
                'album_id': album,
                'extended': 1,
                'photo_sizes': 1,
                'access_token': self.access_token, 
                'v': self.api_version,
                }
            response = requests.get(vk_url, params=params)
            data = response.json()
            if 'error' in data:
                raise ValueError (f"VK API Error: {data['error']['error_msg']}")
            return data['response']['items']
        except (KeyError, IndexError) as e:
            raise Exception(f'Ошибка обработки данных от VK API: {e}')

    def process_photos(self, photos, count=5):
        '''фильтруем размеры и оставляем только максимальные размеры'''
        try:
            processed = []
            for photo in photos:
                likes = photo['likes']['count']
                date = photo['date']
                max_size = max(photo['sizes'], key=lambda s: s['width'] * s['height'])
                processed.append({
                    'likes': likes,
                    'date': date,
                    'url': max_size['url'],
                    'size_type': max_size['type']
                })
            return processed[:count]
        except (KeyError, IndexError) as e:
            raise Exception(f'Ошибка обработки данных фотографий: {e}')
        
class YD_API:
    def __init__(self, yandex_token):
        self.yandex_token = yandex_token
        self.base_url = 'https://cloud-api.yandex.net/v1/disk/resources' 
    
    def creating_folder(self, folder_name):
        '''создаем новую папку на яндекс диске'''
        try:
            headers = {'Authorization': self.yandex_token}
            params = {'path': folder_name}
            response = requests.put(self.base_url, headers=headers, params=params)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка сети при создании папки на Яндекс.Диске: {e}")
        
    def upload_to_yandex(self, folder_name,selected_photos):
        '''добавление фото на яндекс диск''' 
        uploaded = []
        for photo in tqdm(selected_photos, colour= 'green', desc='Загрузка фотографий'):
            file_name = f"{photo['likes']}.jpg"
            if any(f['file_name'] == file_name for f in uploaded):
                file_name = f"{photo['likes']}_{photo['date']}.jpg"
        
            headers = {'Authorization': f'{self.yandex_token}'}
            params = {
                'path': f'{folder_name}/{file_name}',
                'url': photo['url']
                }
            response = requests.post(f'{self.base_url}/upload', params=params, headers=headers)
            if response.status_code == 202:
                uploaded.append({
                    'file_name': file_name,
                    'size': photo['size_type']
                    })
            else:
                raise Exception(f"Ошибка загрузки файла {file_name}: {response.text}")
        return uploaded
    
    
def load_config():
    '''Загружает конфигурацию из файла'''
    try:
        config = configparser.ConfigParser()
        config.read('мои работы=)\config к облаку.ini') 
        return config
    except Exception as e:
        raise Exception(f"Ошибка загрузки конфигурации: {e}")
    

def save_report(uploaded_info, filename='photos_info.json'):
    try:
        with open(filename, 'w') as f:
            json.dump(uploaded_info, f, indent=4)
        print("\nВыполненно! Проверте Yandex Disk и файл photos_info.json") 
    except Exception as e:
        raise Exception(f"Ошибка сохранения отчета: {e}")

def main():
    config = load_config()
    vk_identifier = input("Введите ID/screen_name пользователя VK: ").strip()
    folder_name = input('Как бы вы хотели назвать папку: ').strip()
    
    vk_album = VK_API(config['VK']['access_token'])
    yd_upgrade = YD_API(config['YANDEX']['yandex_token']) 
    
    photos = vk_album.my_foto(vk_identifier)
    selected_photos = vk_album.process_photos(photos)

    yd_upgrade.creating_folder(folder_name)
    uploaded_info = yd_upgrade.upload_to_yandex(folder_name, selected_photos)
    
    save_report(uploaded_info)
    
if __name__ == '__main__':
    main()