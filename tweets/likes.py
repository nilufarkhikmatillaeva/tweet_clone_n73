from typing import Any

from core.db_settings import execute_query, get_connection


def like_tweet(user_id, tweet_id):
    # Check if already liked
    query = "SELECT * FROM likes WHERE user_id = %s AND tweet_id = %s"
    params = (user_id, tweet_id)
    result = execute_query(query=query, params=params, fetch="one")
    if result:
        print("You already liked this tweet.")
        return False

    # Insert new like
    insert_query = "INSERT INTO likes (user_id, tweet_id) VALUES (%s, %s)"
    insert_params = (user_id, tweet_id)
    if execute_query(query=insert_query, params=insert_params):
        print("Tweet liked successfully!")
        return True
    return False

def count_likes(tweet_id):
    query = "SELECT COUNT(*) FROM likes WHERE tweet_id = %s"
    params = (tweet_id,)
    result = execute_query(query=query, params=params, fetch="one")
    return result[0] if result else 0

from core.db_settings import execute_query

def unlike_tweet(user_id, tweet_id):
    query = "DELETE FROM likes WHERE user_id = %s AND tweet_id = %s"
    params = (user_id, tweet_id)
    if execute_query(query=query, params=params):
        print("Tweet unliked!")
        return True
    else:
        print("Something went wrong.")
        return False

from core.db_settings import execute_query

def show_tweets_by_likes():
    query = """
        SELECT t.id, t.tweet, COUNT(l.id) AS likes
        FROM tweets t
        LEFT JOIN likes l ON t.id = l.tweet_id
        GROUP BY t.id
        ORDER BY likes DESC, t.id DESC
    """
    rows = execute_query(query=query, fetch="all")
    for r in rows:
        print(f"{r[0]}. {r[1]} - {r[2]} likes")



def get_liked_users(tweet_id: object) -> bool | None | Any:
    query = """
        SELECT u.username, l.created_at
        FROM likes l
        JOIN users u ON l.user_id = u.id
        WHERE l.tweet_id = %s
        ORDER BY l.created_at DESC
    """
    params = (tweet_id,)
    return execute_query(query=query, params=params, fetch="all")