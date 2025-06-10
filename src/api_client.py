import requests
from urllib3 import request

from src.user_info import UserProfile


class VkApiClient:
    """Клиент VK API"""

    def __init__(self, token) -> None:
        self.token = token
        self.base_url = "https://api.vk.com/method/"

    def get_request(self, method, params):
        """Запрос к api"""

        params.update({
            'access_token': self.token,
            'v': "5.199"
        })

        url = f"{self.base_url}{method}"
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if 'error' not in data:
                return data.get('response', {})
            print(f"ошибка: {data['error']['error_msg']}")
            return {}
        except requests.exceptions.RequestException as e:
            print(f"ошибка запроса: {e}")
            return {}

    def get_user_info(self, user_ids, fields = "first_name,last_name,city,bdate,photo_200"):
        """Возвращает список информации о пользователях"""

        request = self.get_request(
            'users.get',
            params={
                'user_ids': ','.join(user_ids),
                'fields': fields
            }
        )
        res = []
        for user in request:
            city_info = ""
            if 'city' in user:
                city_info = f"   Город: {user['city'].get('title', 'Город не указан')}\n"
            else:
                city_info = "   Город не указан\n"
            bdate_str = f"  🥳Дата рождения: {user['bdate']}\n" if 'bdate' in user else ""
            user_info =UserProfile(
                first_name=user.get('first_name', ''),
                last_name=user.get('last_name', ''),
                user_id=str(user.get('id', 'userid не указан')),
                birth_date=bdate_str,
                city=city_info,
                is_closed= "Профиль открыт\n" if  user.get('is_closed',False) else "Профиль закрыт\n"
            )
            res.append(user_info)
        return res



    def get_friends(self, user_id,count: int = 100, fields: str = "first_name,last_name,online,photo_50"):
        """Возвращает список друзей пользователя"""
        request = self.get_request(
            'friends.get',
            params=
            {
                'user_id': user_id,
                'count': count,
                'fields': fields
            })

        friends = []

        if 'items' in request:
            for friend in request['items']:
                bdate_str = f"  🥳Дата рождения: {friend['bdate']}\n" if 'bdate' in friend else ""
                user_info = UserProfile(
                    first_name=friend.get('first_name', ''),
                    last_name=friend.get('last_name', ''),
                    user_id=str(friend.get('id', 'userid не указан')),
                    birth_date=bdate_str,
                    online="Онлайн! " if friend.get('online', 0) == 1 else "не в сети("
                )
                friends.append(user_info)
        return friends



    def get_photo_albums(self, owner_id: int, covers: int = 1):
        """Возвращает список альбомов указанного пользователя"""
        return self.get_request(
            'photos.getAlbums',
            params=
            {
                'owner_id': owner_id,
                'need_covers': covers
            })




    def get_wall_posts(self, owner_id: int, count: int = 10, filtr: str = "owner"):
        """Возвращает посты со стены указанного пользователя"""
        return self.get_request(
        'wall.get',
                params={
                    'owner_id': owner_id,
                    'count': count,
                    'filter': filtr
                }
                )





