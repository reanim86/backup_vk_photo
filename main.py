import requests
from pprint import pprint

def get_vk_photo(id, album_id='profile'):
    """
    Функция получает информацию о фото в виде json, на  вход подаем id пользователя и id альбома
    """
    url_vk = 'https://api.vk.com/method/photos.get'
    token_vk = ''
    version_api_vk = '5.131'
    vk_id = id
    vk_album_id = album_id
    params = {
        'access_token': token_vk,
        'v': version_api_vk,
        'owner_id': vk_id,
        'album_id': vk_album_id,
        'extended': '1',
#        'photo_sizes': '1'

    }
    response = requests.get(url=url_vk, params=params)
    return response.json()
# def name_photo(vk_photo_dict):
#     for vk_photo in vk_photo_dict:






vk = get_vk_photo('7397173')
#vk_photo = vk['items']
pprint(vk['items'])