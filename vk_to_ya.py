import requests
from pprint import pprint
import json
import datetime
import time
from tqdm import tqdm

class YandexDisk:


    def __init__(self, file_token='tokens/token_ya.txt'):
        # self.access_token = access_token
        self.file_token = file_token

    def header_auth(self):
        """формируем заголовок авторизации"""
        token = ya.gettoken()
        return {"Authorization": f"OAuth {token}"}

    def _get_link(self, path: str):
        """Метод получает ссылку на закачку файла"""
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {'path': path, 'overwrite': 'true'}
        res = requests.get(upload_url, params=params, headers=self.header_auth())
        status = res.status_code
        if status != 200:
            a = status
        else:
            a = res.json()
        return a

    def upload(self, path: str):
        """загружаем локальный файл на Яндекс Диск"""
        if not (url_json := self._get_link(path)) in (400, 401, 403, 405, 500):
            url = url_json['href']
            res_put_load = requests.put(url=url, data=open(path_from_vk, 'rb'))
        else:
            return url_json
        return res_put_load.status_code  # == 201

    def upload_from_vk(self, path: str, url: str):
        """загружаем локальный файл на Яндекс Диск"""
        params= {'path': path, 'url': url}
        res_post_load = requests.post(url=url, data=params, headers=self.header_auth())
        return res_post_load.status_code  # == 201

    def gettoken(self):
        with open(self.file_token, 'r') as file_object:
            return file_object.read().strip()



class IoJson:
    def __int__(self, in_file_json: str, out_file_json: str, data):
        self.in_file_json = in_file_json
        self.out_file_json = out_file_json
        self.data = data

    def read_json(file_name: str):
        with open(file_name) as file_object:
            data = json.load(file_object)
            return data

    def write_json(file_name: str, data):
        with open(file_name, 'w') as file_object:
            json.dump(data, file_object, ensure_ascii=False, indent=2)


class VK:

    def __init__(self, file_token='tokens/token_vk.txt', user_id='207289490', version='5.131',
                 base_url='https://api.vk.com/method/', quantity_photo=5):
        self.file_token = file_token
        self.user_id = user_id
        self.version = version
        self.base_url = base_url
        self.quantity_photo = quantity_photo

    def gettoken(self):
        with open(self.file_token, 'r') as file_object:
            return file_object.read().strip()

    def general_params(self):
        return {
            'access_token': self.gettoken(),
            'v': self.version
        }

    def get_users_info(self, user_ids: str, fields: str):
        params = {
            'user_ids': user_ids,
            'fields': fields,
        }
        return requests.get(f'{self.base_url}users.get', params={**params, **self.general_params()}).json()

    def photos_get(self):
        params = {'owner_id': self.user_id,
                  'album_id': 'wall',
                  'extended': '1',
                  }
        return requests.get(f'{self.base_url}photos.get', params={**params, **self.general_params()}).json()

    def max_find_photo(self, album_photos):
        '''get type and url photo max size'''
        height_width_size_max = 0
        for i in album_photos:
            if height_width_size_max < i['height'] * i['width']:
                height_width_size_max = i['height'] * i['width']
                type_size_max = i['type']
                url_size_max = i['url']
        return [type_size_max, url_size_max]

    def get_list_photos_and_inf(self):
        pass
        return ''

    # def create_name_file
vk = VK()
a = vk.photos_get()
count_photos = a['response']['count']
bar0 = 100/count_photos
bar1 = 0

for album in a['response']['items']:
    a = (str(album['likes']['count'])+'_'+
         str(datetime.datetime.fromtimestamp(album['date']).strftime('%Y%m%d_%H%M'))+'.jpg',
         vk.max_find_photo(album['sizes'])[0],vk.max_find_photo(album['sizes'])[1])
    b = f"{a[0][0]}.jpg {a[0]} {a[1]} {a[2]}"
    name_file = f'Upload/{a[0][0]}.jpg'
    url_file = f'{a[2]}'
    # filename = 'photo.jpg'
    foto_download = requests.get(url_file)
    with open(name_file, 'wb') as file:
        file.write(foto_download.content)
    bar1 += bar0
    print("*" * int(bar0), end='')
print(f'\nЗагружено {count_photos} файлов')
pass



    # ya = YandexDisk()
    # path_to_disk = f'Download/{name_file}'
    # path_from_vk = url_file
    # print(f'Качаем на я.диск: {path_to_disk}, с ВК {path_from_vk}')
    # status = ya.upload_from_vk(path_to_disk, path_from_vk)
    # if status != 202:
    #     res = f'Что то пошло не так! Ответ сервера: {status}'
    # else:
    #     res = f'Файл загружен на Яндекс Диск. Ответ сервера: {status}'
    # print(res)


pass
# pass
