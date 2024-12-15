# Event Driven API - Steps

## Install SQLite3
```bash
sudo apt install sqlite3
```

## Check Installation
```bash
sqlite3 --version
```

## Create a directory `event_driven_api` and initiate a DB
```bash
mkdir event_driven_api
sqlite3 my_database.db
```

## Create table `posts`

```bash

CREATE TABLE posts (post_id TEXT, genre TEXT, likes INTEGER, comments INTEGER, timestamps TEXT, popularity_score REAL);

INSERT INTO posts (post_id, likes, comments, timestamps, popularity_score) VALUES ('post1','books', 10, 5, '2024-12-01 10:00:00', 15.0);
INSERT INTO posts (post_id, likes, comments, timestamps, popularity_score) VALUES ('post2','fashion', 20, 8, '2024-12-01 11:00:00', 25.0);
INSERT INTO posts (post_id, likes, comments, timestamps, popularity_score) VALUES ('post3','jobs', 5, 2, '2024-12-01 12:00:00', 7.0);
INSERT INTO posts (post_id, likes, comments, timestamps, popularity_score) VALUES ('post4','tech', 15, 10, '2024-12-01 13:00:00', 20.0);
INSERT INTO posts (post_id, likes, comments, timestamps, popularity_score) VALUES ('post5','books', 8, 3, '2024-12-01 14:00:00', 11.0);
```

## Install Redis

## Install python dependencies
```bash
pip install redis
```

## Launch Request Response Based API
```bash
python event_driven_interaction.py
```

## Launch `notify_user` service
```bash
python notify_user.py
```

## Launch `increment_likes` service
```bash
python increment_likes.py
```


## Check the response time in Postman
```javascript
{
    "post_id": "post1",
    "interaction_type": "like",
    "user_id": "user1"
}
```
