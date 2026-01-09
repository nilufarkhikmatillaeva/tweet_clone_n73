"""
All tables queries
"""

users = """
        CREATE TABLE users (
            id bigserial primary key,
            username varchar(255) not null unique,
            email varchar(255) not null unique,
            password varchar(255) not null,
            created_at timestamp default current_timestamp
            )
            """
tweets = """
        CREATE TABLE tweets (
            id bigserial primary key,
            user_id bigint references users(id) on delete cascade,
            tweet text not null,
            created_at timestamp default current_timestamp
            )
            """
likes = """
        CREATE TABLE likes (
            id bigserial primary key,
            user_id bigint references users(id) on delete cascade,
            tweet_id bigint references tweets(id) on delete cascade,
            created_at timestamp default current_timestamp
            )
            """

