from typing import Any

from core.db_settings import execute_query

def add_tweet(user_id, content):
    query = "INSERT INTO tweets (user_id, tweet) VALUES (%s, %s)"
    params = (user_id, content)
    if execute_query(query=query, params=params):
        print("Tweet posted successfully!")
        return True
    print("Failed to post tweet.")
    return False

def show_all_tweets(limit: object = 10, offset: object = 0) -> bool | None | Any:
    query = """
        SELECT t.id, t.tweet, t.created_at, u.username
        FROM tweets t
        JOIN users u ON t.user_id = u.id
        ORDER BY t.created_at DESC
        LIMIT %s OFFSET %s
    """
    params = (limit, offset)
    return execute_query(query=query, params=params, fetch="all")

def show_my_tweets(user_id):
    query = """
        SELECT id, tweet, created_at
        FROM tweets
        WHERE user_id = %s
        ORDER BY created_at DESC
    """
    params = (user_id,)
    return execute_query(query=query, params=params, fetch="all")

def delete_tweets(user_id, tweet_id):
    query = """
        DELETE FROM tweets WHERE id = %s AND user_id = %s  
        """
    params = (tweet_id, user_id)
    if execute_query(query=query, params=params):
        print("Tweet deleted successfully.")
        return True
    print("Failed to delete tweet.")
    return False

def get_liked_tweets(user_id, limit=10, offset=0):
    query = """
        SELECT t.id, t.tweet, u.username, t.created_at
        FROM likes l
        JOIN tweets t ON l.tweet_id = t.id
        JOIN users u ON t.user_id = u.id
        WHERE l.user_id = %s
        ORDER BY l.created_at DESC
        LIMIT %s OFFSET %s
    """
    params = (user_id, limit, offset)
    return execute_query(query=query, params=params, fetch="all")



