import sys
import time
from datetime import datetime

from src.api_client import VkApiClient
from src.user_info import UserProfile


def print_user_info(users: list[UserProfile]):
    if not users:
        print("Информация не найдена")
        return
    print(f"информация о пользователях\n")
    i = 1
    for user in users:
        print(f"😎 User {i}:"
              f"userid: {user.user_id}"
              f" {user.first_name} {user.last_name}")
        if user.birth_date!="":
            print(user.birth_date)
        if user.city!="":
            print(user.city)
        print()
        i+=1
def print_user_friends(friends: list[UserProfile]):
    print(f"Найдено {len(friends)} друзей")
    for i, friend in enumerate(friends, 1):
        print(f"{i}. {friend.first_name} {friend.last_name} - {friend.online}")


def print_photo_albums(alb_data: dict):
    if not alb_data or 'items' not in alb_data:
        print("Нету фотоальбомов(")
        return
    albums = alb_data['items']
    print(f"Найдено {len(albums)} альбомов")
    i = 1
    for album in albums:
        print(f"{i}: {album.get('title')}")
        print( f"id: {album.get('id')}\n")
        print(f"date: {album['created']}")

        if 'description' in album and album['description']:
            print(f"Описание: {album['description']}...\n")
        i+=1
def print_posts(posts_data):
    posts = posts_data['items']
    print(f"Найдено {len(posts)} постов")
    for post in posts:
        print(datetime.fromtimestamp(post.get('date', 0)).strftime('%d.%m.%Y %H:%M'))
        print(post.get('text', ''))
        print(f"Лайки: {post.get('likes', {}).get('count', 0)}")
        print(f"Комменты: {post.get('comments', {}).get('count', 0)}")

def get_int_id(vk_api_client, user_input):
    """числовой ID пользователя по screen_name"""
    users = vk_api_client.get_user_info([user_input])
    if not users:
        print("Пользователь не найден")
        return None
    try:
        return int(users[0].user_id)
    except (ValueError, AttributeError):
        print("Не удалось получить ID пользователя")
        return None



def main():
    TOKEN = "vk1.a.jOY6EYWJUmhg6Be-su_KPUmklXxKjurc7vkigBMEPgjylavhBiIxBUnyOFcgaTcmkVm8mU1hV3XkISZx57-BQFe6-qb83onHAdLQsX4eZxcuXDm9iPoVHmHFwhDwpjasJ9rrMXkSxBWfBKJjeNFKtSm4IE_1Tfxb2QTu9Cosh1H6ZqLjZvUHBxRmfrzXuBH8cHDyzD0WSivAobchS55Bww"
    vk_api_client = VkApiClient(TOKEN)
    print("Выберите действие")
    print("Пользователь")
    print("Друзья")
    print("Фотоальбомы")
    print("Посты")

    while True:
        inp = input()
        if inp == "exit":
            sys.exit(0)
        user_input = input("Введите VK ID или screen_name: ").strip()
        if not user_input:
            print("ID не введен")
            continue

        int_id = get_int_id(vk_api_client, user_input)
        if int_id is None:
            continue

        try:
            if inp == "Пользователь":
                users = vk_api_client.get_user_info([user_input])
                print_user_info(users)

            elif inp == "Друзья":
                friends = vk_api_client.get_friends(int_id)
                print_user_friends(friends)

            elif inp == "Фотоальбомы":
                albums = vk_api_client.get_photo_albums(int_id)
                print_photo_albums(albums)

            elif inp == "Посты":
                posts = vk_api_client.get_wall_posts(int_id)
                print_posts(posts)

            else:
                print("Неизвестная команда")

        except Exception as e:
            print(f"Ошибка: {e}")
        time.sleep(0.5)

if __name__ == "__main__":
    main()




