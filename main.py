from typing import Callable, Optional

from auth import login
from core import models
from core.db_settings import execute_query
from utils import menus
from tweets import crud, likes


def show_auth_menu() -> Callable | None:
    """
    Show auth menu
    :return: function based on option
    """
    print(menus.auth_menu)
    option = input("Enter your option: ")
    if option == "1":
        if login.login():
            print("Welcome to main menu")
            return show_main_menu()
        print("Username or password is incorrect")

    elif option == "2":
        if login.register():
            print("Please login now")

    elif option == "3":
        if login.validate():
            print("Welcome to main menu")
            return show_main_menu()
    elif option == "4":
        print("Good bye")
        return None

    return show_auth_menu()


# def show_all_tweets_menu() -> Callable:
#     """
#     Submenu for all tweets
#     :return:
#     """
#     print(menus.all_tweets_menu)
#     return show_all_tweets_menu()


def show_main_menu() -> Callable:
    """
    Show main menu to users
    :return: function based on option
    """
    print(menus.main_menu)
    option = input("Enter your option: ")
    if option == "1":
        crud.show_all_tweets()

    elif option == "2":
        crud.show_my_tweets()

    elif option == "3":
        crud.get_liked_tweets()

    elif option == "4":
        crud.add_tweet()

        # show all tweets function called
    return show_all_tweets_menu()

def show_all_tweet_menu() -> Optional[Callable]:
    current_page = 1
    while True:
        crud.show_all_tweets(current_page)
        action = input(
            " 0.Back\n"
            " 1.next\n"
            " 2.prev\n"
            " 3.Like the tweet\n"
            " 4.Unlike the tweet\n"
            " 5.Order by Likes\n >> "
        ).lower()

        if action == "0":
            return print("Went to the main menu")
        if action == "1":
            current_page += 1
            return crud.show_all_tweets(current_page)
        elif action == "2" and current_page > 1:
            current_page -= 1
            return crud.show_all_tweets(current_page)
        elif action == "3":
            return likes.like_tweet()
        elif action == "4":
            return likes.unlike_tweet(current_page)
        elif action == "5":
            return likes.show_tweets_by_likes()
        else:
            print("Invalid Number.")



if __name__ == '__main__':
    # create tables in here
    # execute_query(query=models.users)
    # execute_query(query=models.tweets)
    # execute_query(query=models.likes)
    execute_query(query=models.codes)
    show_auth_menu()

