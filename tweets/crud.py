from typing import Any
from core.db_settings import execute_query

def add_tweet(user_id: int, content: str) -> bool:
    """
    Add a new tweet for the given user.
    Returns True if posted successfully, otherwise False.
    """
    query = "INSERT INTO tweets (user_id, tweet) VALUES (%s, %s)"
    params = (user_id, content)
    if execute_query(query=query, params=params):
        print("Tweet posted successfully!")
        return True
    print("Failed to post tweet.")
    return False


def show_all_tweets(limit: int = 10, offset: int = 0) -> list[Any]:
    """
    Get all tweets with pagination.
    Returns a list of (id, tweet, created_at, username).
    """
    query = """
        SELECT t.id, t.tweet, t.created_at, u.username
        FROM tweets t
        JOIN users u ON t.user_id = u.id
        ORDER BY t.created_at DESC
        LIMIT %s OFFSET %s
    """
    params = (limit, offset)
    return execute_query(query=query, params=params, fetch="all")


def show_my_tweets(user_id: int) -> list[Any]:
    """
    Get all tweets posted by the given user.
    Returns a list of (id, tweet, created_at).
    """
    query = """
        SELECT id, tweet, created_at
        FROM tweets
        WHERE user_id = %s
        ORDER BY created_at DESC
    """
    params = (user_id,)
    return execute_query(query=query, params=params, fetch="all")


def delete_tweets(user_id: int, tweet_id: int) -> bool:
    """
    Delete a tweet if it belongs to the given user.
    Returns True if deleted successfully, otherwise False.
    """
    query = "DELETE FROM tweets WHERE id = %s AND user_id = %s"
    params = (tweet_id, user_id)
    if execute_query(query=query, params=params):
        print("Tweet deleted successfully.")
        return True
    print("Failed to delete tweet.")
    return False


def get_liked_tweets(user_id: int, limit: int = 10, offset: int = 0) -> list[Any]:
    """
    Get all tweets liked by the given user.
    Returns a list of (tweet_id, tweet, username, created_at).
    """
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


def show_tweets_by_likes(limit: int = 10, offset: int = 0) -> list[Any]:
    """
    Get all tweets ordered by number of likes.
    Returns a list of (id, tweet, likes).
    """
    query = """
        SELECT t.id, t.tweet, COUNT(l.id) AS likes
        FROM tweets t
        LEFT JOIN likes l ON t.id = l.tweet_id
        GROUP BY t.id
        ORDER BY likes DESC, t.id DESC
        LIMIT %s OFFSET %s
    """
    params = (limit, offset)
    return execute_query(query=query, params=params, fetch="all")


def get_liked_users(tweet_id: int) -> list[Any]:
    """
    Get all users who liked a specific tweet.
    Returns a list of (username, created_at).
    """
    query = """
        SELECT u.username, l.created_at
        FROM likes l
        JOIN users u ON l.user_id = u.id
        WHERE l.tweet_id = %s
        ORDER BY l.created_at DESC
    """
    params = (tweet_id,)
    return execute_query(query=query, params=params, fetch="all")


