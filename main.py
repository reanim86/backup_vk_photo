import requests
from pprint import pprint
from collections import Counter
import json
import copy
import time
from tqdm import tqdm
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def get_vk_photo(id, token, album_id='profile'):
    """
    Функция получает информацию о фото в виде json, на  вход подаем id пользователя и id альбома, если id альбома не
    передать, то берем фото профиля
    """
    url_vk = 'https://api.vk.com/method/photos.get'
    version_api_vk = '5.131'
    params = {
        'access_token': token,
        'v': version_api_vk,
        'owner_id': id,
        'album_id': album_id,
        'extended': '1',
        'photo_sizes': '1'

    }
    response = requests.get(url=url_vk, params=params)
    photo = response.json()
    return photo['response']

def get_size_photo(photo_dict):
    """
    Функция выбирает фото наибольшего размера
    """
    temp_dict_photo = {}
    necessary_photo = {}
    necessary_list = []
    necessary_photo['likes'] = photo_dict['likes']['count']
    necessary_photo['date'] = photo_dict['date']
    for photo in photo_dict['sizes']:
        temp_dict_photo[photo['type']] = photo['url']
    if 'w' in temp_dict_photo:
        necessary_photo['size'] = 'w'
        necessary_photo['url'] = temp_dict_photo['w']
    elif 'z' in temp_dict_photo:
        necessary_photo['size'] = 'z'
        necessary_photo['url'] = temp_dict_photo['z']
    elif 'y' in temp_dict_photo:
        necessary_photo['size'] = 'y'
        necessary_photo['url'] = temp_dict_photo['y']
    elif 'x' in temp_dict_photo:
        necessary_photo['size'] = 'x'
        necessary_photo['url'] = temp_dict_photo['x']
    elif 'r' in temp_dict_photo:
        necessary_photo['size'] = 'r'
        necessary_photo['url'] = temp_dict_photo['r']
    elif 'q' in temp_dict_photo:
        necessary_photo['size'] = 'q'
        necessary_photo['url'] = temp_dict_photo['q']
    elif 'p' in temp_dict_photo:
        necessary_photo['size'] = 'p'
        necessary_photo['url'] = temp_dict_photo['p']
    elif 'o' in temp_dict_photo:
        necessary_photo['size'] = 'o'
        necessary_photo['url'] = temp_dict_photo['o']
    elif 'm' in temp_dict_photo:
        necessary_photo['size'] = 'm'
        necessary_photo['url'] = temp_dict_photo['m']
    elif 's' in temp_dict_photo:
        necessary_photo['size'] = 's'
        necessary_photo['url'] = temp_dict_photo['s']
    return necessary_photo

def get_folder(name_folder):
    """
    Функция создает попаку куда будем загружать фото, на вход принимаем имя папки
    """
    url_ya = 'https://cloud-api.yandex.net/v1/disk/resources'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'OAuth {ya_token}'
    }
    params_ya = {
        'path': name_folder
    }
    response = requests.put(url=url_ya, headers=headers, params=params_ya)
    return

def upload_photo(list_photo, token):
    """
    Функция загружает фото на яндекс диск
    """
    url_ya = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'OAuth {token}'
    }
    for dict_photo in tqdm(list_photo):
        params = {
            'path': f'{folder_name}/{dict_photo["file_name"]}',
            'url': dict_photo['url']
        }
        response = requests.post(url=url_ya, headers=headers, params=params)
        time.sleep(0.2)
    return

def name_file(number, photo_in_vk):
    """
    Функция принимает количество все полученные фото из ВК, возвращает список необходимых для загрузки фото с
    присовенными именами
    """
    photo_list = []
    count_photo = []
    while number != 0:
        photo = get_size_photo(photo_in_vk[number - 1])
        photo['file_name'] = f'{photo["likes"]}.jpg'
        photo_list.append(photo)
        number -= 1
    for photo_vk in photo_list:
        count_photo.append(photo_vk['file_name'])
    count_name_photo = Counter(count_photo)
    for file, count_number in dict(count_name_photo).items():
        if count_number == 1:
            del count_name_photo[file]
    for photo_dict in photo_list:
        if photo_dict['file_name'] in count_name_photo:
            photo_dict['file_name'] = f'{photo_dict["likes"]}{photo_dict["date"]}.jpg'
    return photo_list

def save_json(save_dict):
    """
    Функция сохраняет информация по скопированным файлам в json файл vk_photo.json
    """
    temp_dict = copy.deepcopy(save_dict)
    for final_json in temp_dict:
        final_json.pop('date')
        final_json.pop('likes')
        final_json.pop('url')
    with open('vk_photo.json', 'w') as write_file:
        json.dump(temp_dict, write_file, indent=4)

def add_folder_google(name_folder='vk_photo'):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    # file_metadata = {
    #     'title': name_folder,
    #     'mimeType': 'application/vnd.google-apps.folder'
    # }
    # list_file = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    # for file in list_file:
    #     if file['title'] == name_folder:
    #         return list_file
    # folder = drive.CreateFile(file_metadata)
    # folder.Upload()
    file1 = drive.CreateFile({"mimeType": "text/csv", "parents": [{"kind": "drive#fileLink", "id": '1RssuhwOellfZultWHwoxPk9Ud4CsrzgS'}]})
    file1.SetContentFile("vk_photo.json")


add_folder_google()



# ya_token = ''
# vk_token = ''
# id_client = '7397173'
# id_album = '248721370'
# folder_name = 'vk_photo'
# vk = get_vk_photo(id_client, vk_token, id_album)
# count = vk['count']
# vk_photo = vk['items']
# files = name_file(count, vk_photo)
# get_folder(folder_name)
# upload_photo(files, ya_token)
# save_json(files)





