import requests
import logging
import json
from tqdm import tqdm
from datetime import datetime


with open('token.txt', 'rt') as f:
    token_vk1 = f.read().strip()


logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w", format="%(asctime)s %(levelname)s %(message)s")
logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")


class VK:

    url = 'https://api.vk.com/method/'

    def __init__(self, token_vk, version="5.131"):
        self.params = {"access_token": token_vk, 'v': version}

    def get_vk_img(self, vk_id, album_id): # VK_ID - id пользователя VK
        j_dict = []
        photos = []
        photos_get_url = self.url + 'photos.get'
        photos_get_params = {"photo_sizes": 1, "owner_id": vk_id, "album_id": album_id}
        res = requests.get(photos_get_url, params={**self.params, **photos_get_params}).json()
        for i in res['response']['items']:
            img_url = (i['sizes'][-1]['url'])
            img_name = (f'{i["id"]} {datetime.utcfromtimestamp(i["date"]).strftime("%Y-%m-%d")} {img_url.split("?")[0].split("/")[-1]}')
            j_dict.append({"failname": img_name, "saze": i["sizes"][-1]["type"]})
            photos.append({'name': img_name, 'url': img_url})
            with open('file.json', 'w', encoding='utf8') as f:
                json.dump(j_dict, f, ensure_ascii=False, indent=2)
        return photos


class YaUp:
    def __init__(self, token_ya):
        self.token = token_ya

    def get_headers(self):
        return {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {self.token}'}

    def create_folder(self, path):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        requests.put(url, params={"path": path}, headers=headers)

    def ya_up(self, vk_list_dict, folder):
        url_ya = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        count = 0
        how_many = input(f'Изображений в албоме {len(vk_list_dict)}. Сколько из них загрузить на Яндекс Диск?')
        for i in tqdm(range(int(how_many))):
            params = {"url": vk_list_dict[i]['url'], "path": f'{folder}/{vk_list_dict[i]["name"]}'}
            response = requests.post(url_ya, headers=headers, params=params)
            count += 1
            if response.status_code == 202:
                logging.info(f'File {vk_list_dict[i]["name"]} have been uploaded successfully.')
        return 'Загрузка завершена!'


if __name__ == '__main__':
    id_album = ""
    path = 'Netologi3'
    token_ya1 = ''
    id = ''
    v = VK(token_vk1)
    y = YaUp(token_ya1)
    y.create_folder(path)
    print(y.ya_up(v.get_vk_img(id, id_album), path))