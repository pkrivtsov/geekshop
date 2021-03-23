from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'facebook':
        return

    # print (response)
    """ response
    {'id': '3718181...',
     'name': 'Павел Кривцов', 
     'email': 'pkrivtsov@yandex.ru',
     'picture': {'data': {'height': 200, 'is_silhouette': False, 'url': 'url', 'width': 200}}, 
     'link': 'url',
     'access_token': 'EAAGbZBogxECgBAIj...', 
     'expires': 5178, 'granted_scopes': ['user_link', 'email', 'public_profile']}
    """

    access_token = response['access_token']

    # api_url = f"https://graph.facebook.com/v10.0/me?fields=id%2Cemail%2Cbirthday%2Clink&access_token={access_token}"

    api_url = urlunparse(('https',
                          'graph.facebook.com',
                          '/v10.0/me',
                          None,
                          urlencode(OrderedDict(fields=','.join(('id', 'email', 'birthday', 'link')),
                                                access_token=response['access_token'])),
                          None
                          ))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()
    # print(data)
    """ data =
    {'id': '3718181...', 'email': 'pkrivtsov@yandex.ru', 'birthday': '06/30/1983', 'link': 'url'}
    """
    user.email = data['email']
    user.shopuserprofile.aboutMe = data['link']

    if data['birthday']:
        birthday = datetime.strptime(data['birthday'], '%m/%d/%Y').date()

        age = timezone.now().date().year - birthday.year
        print(f'{birthday} {age}')
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.facebook.FacebookOAuth2')

    user.save()
