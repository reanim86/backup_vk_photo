import requests
from collections import Counter
import json
import copy
import time
from tqdm import tqdm
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import configparser
from pprint import pprint
import io


def get_vk_photo(id, token, album_id='profile'):
    """
    Функция возвращает информацию о фото в виде словаря, на  вход подаем id пользователя и id альбома, если id альбома
    не передать, то берем фото профиля
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

def get_folder(name_folder='vk_photo'):
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

def upload_photo(list_photo, token, folder='vk_photo'):
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
            'path': f'{folder}/{dict_photo["file_name"]}',
            'url': dict_photo['url']
        }
        response = requests.post(url=url_ya, headers=headers, params=params)
        time.sleep(0.2)
    return

def name_file(number, photo_in_vk):
    """
    Функция принимает количество фото полученных из ВК, возвращает список необходимых для загрузки фото с
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
    """
    Функция создает папку на GoogleDrive в случае ее отсутствия
    """
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    file_metadata = {
        'title': name_folder,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    list_file = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file in list_file:
        if file['title'] == name_folder:
            return
    folder = drive.CreateFile(file_metadata)
    folder.Upload()
    return

def upload_photo_google(photo_list, name_dir='vk_photo'):
    """
    Функция загружает фото на GoogleDrive из директории temp_photo, при этом фалы не перезаписываются
    """
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    list_file = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    id_dir = ''
    for file in list_file:
        if file['title'] == name_dir:
            id_dir = file['id']

    for photo in tqdm(photo_list):
        access_token = gauth.attr['credentials'].access_token
        metadata = {
            'name': photo['file_name'],
            'parents': [id_dir]
        }
        files = {
            'data': ('metadata', json.dumps(metadata), 'application/json'),
            'file': io.BytesIO(requests.get(photo['url']).content)
        }
        r = requests.post(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            headers={"Authorization": "Bearer " + access_token},
            files=files
        )
        time.sleep(0.5)
    return

def get_user_id(screen_name, token):
    """
    Функция получает короткое имя пользователя ВК, вовзращает id этого пользователя
    """
    url_vk = 'https://api.vk.com/method/utils.resolveScreenName'
    version_api_vk = '5.131'
    params = {
        'access_token': token,
        'v': version_api_vk,
        'screen_name': screen_name

    }
    response = requests.get(url=url_vk, params=params)
    id = response.json()
    return id['response']['object_id']


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('token.ini')
    vk_token = config['UserID']['vk_token']
    ya_token = config['UserID']['ya_token']
    id_album = ''
    folder_name = 'photo_vk'
    add_folder_google(folder_name)
    get_folder(folder_name)
    id_client = input('Введите id пользователя VK, сли есть только короткое имя, нажмите Enter и введите его в ледующем окне ')
    user_name = input('Введите короткое имя пользователя ')
    if len(id_client) != 0:
        vk = get_vk_photo(id_client, vk_token)
    else:
        id_client = get_user_id(user_name, vk_token)
        vk = get_vk_photo(id_client, vk_token)
    count = vk['count']
    vk_photo = vk['items']
    user_number_photo = int(input('Введите количество фото которые хотите загрузить '))
    if user_number_photo <= count:
        files = name_file(user_number_photo, vk_photo)
    else:
        files = name_file(count, vk_photo)
    upload_photo(files, ya_token, folder_name)
    upload_photo_google(files, folder_name)
    save_json(files)





