import requests
from pprint import pprint

def get_vk_photo(id, album_id='profile'):
    """
    Функция получает информацию о фото в виде json, на  вход подаем id пользователя и id альбома
    """
    url_vk = 'https://api.vk.com/method/photos.get'
    token_vk = 'vk1.a.zRNlJVtMlj4kFnPEbiqxoowK0TtzKUibE2y9CZLgViXR0PYyjGvuSyF_J0nub0bg-r4AOMtkMyNHgQU56LaMc7DQo8LDRwm469soUVb_ZIjFVZvi6MdzSGekPDFsjdETgRg_4NN-5heyNwIxFdnBOuCflDqF_Q0XHrMcY3TeFY2WbE3qAHfKGLk-T6opJQ85'
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
    """
    Функция выбирает фото наибольшего размера, на вход принимает словарь с фото
    """
    temp_dict_photo = {}
    necessary_photo = {}
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



vk = get_vk_photo('7397173')
vk_photo = vk['items']
pprint(get_size_photo(vk_photo[2]))
#pprint(vk_photo[2])
#pprint(name_photo(vk_photo[0]))
#pprint(vk_photo)
