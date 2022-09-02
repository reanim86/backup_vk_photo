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
        'photo_sizes': '1'

    }
    response = requests.get(url=url_vk, params=params)
    photo = response.json()
    return photo['response']

def get_size_photo(photo_dict):
    necessary_photo = {}
    for photo in photo_dict['sizes']['type']:
        if photo == 'w':
            necessary_photo['size'] = 'w'
            necessary_photo['url'] = photo['url']
        elif photo == 'z':
            necessary_photo['size'] = 'z'
            necessary_photo['url'] = photo['url']
        elif photo == 'y':
            necessary_photo['size'] = 'y'
            necessary_photo['url'] = photo['url']
        elif photo == 'x':
            necessary_photo['size'] = 'x'
            necessary_photo['url'] = photo['url']
        elif photo == 'r':
            necessary_photo['size'] = 'r'
            necessary_photo['url'] = photo['url']
        elif photo == 'q':
            necessary_photo['size'] = 'q'
            necessary_photo['url'] = photo['url']
        elif photo == 'p':
            necessary_photo['size'] = 'p'
            necessary_photo['url'] = photo['url']
        elif photo == 'o':
            necessary_photo['size'] = 'o'
            necessary_photo['url'] = photo['url']
        elif photo == 'm':
            necessary_photo['size'] = 'm'
            necessary_photo['url'] = photo['url']
        elif photo == 's':
            necessary_photo['size'] = 's'
            necessary_photo['url'] = photo['url']
    return necessary_photo



vk = get_vk_photo('7397173')
vk_photo = vk['items']
#pprint(get_size_photo(vk_photo[2]))
pprint(vk_photo[0])
#pprint(name_photo(vk_photo[0]))
#pprint(vk_photo)
