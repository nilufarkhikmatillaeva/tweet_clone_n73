from typing import Any
from core.db_settings import execute_query

def like_tweet(user_id: int, tweet_id: int) -> bool:
    """
    Like a tweet if not already liked.
    Returns True if liked successfully, else False.
    """
    query = "SELECT * FROM likes WHERE user_id = %s AND tweet_id = %s"
    params = (user_id, tweet_id)
    result = execute_query(query=query, params=params, fetch="one")

    if result:
        print("You already liked this tweet.")
        return False

    query = "INSERT INTO likes (user_id, tweet_id) VALUES (%s, %s)"
    params = (user_id, tweet_id)
    if execute_query(query=query, params=params):
        print("Tweet liked successfully!")
        return True
    print("Failed to like tweet.")
    return False


def count_likes(tweet_id: int) -> int:
    """
    Count how many likes a tweet has.
    Returns the number of likes.
    """
    query = "SELECT COUNT(*) FROM likes WHERE tweet_id = %s"
    params = (tweet_id,)
    result = execute_query(query=query, params=params, fetch="one")
    return result[0] if result else 0


def unlike_tweet(user_id: int, tweet_id: int) -> bool:
    """
    Unlike a tweet if it was previously liked.
    Returns True if unliked , else False.
    """
    query = "DELETE FROM likes WHERE user_id = %s AND tweet_id = %s"
    params = (user_id, tweet_id)
    if execute_query(query=query, params=params):
        print("Tweet unliked!")
        return True
    print("Failed to unlike tweet.")
    return False


def show_tweets_by_likes(limit: int = 10, offset: int = 0) -> list[Any]:
    """
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