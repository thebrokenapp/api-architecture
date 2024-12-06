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

## Create two tables: `interaction` and `post`

```bash
CREATE TABLE interactions (post_id TEXT, interaction_type TEXT, interaction_by TEXT, timestamp TEXT);
CREATE TABLE posts (post_id TEXT, likes INTEGER, comments INTEGER, timestamps TEXT, popularity_score REAL);
.exit
```

## Install Redis

## Install python dependencies
```bash
pip install redis
```

## Launch Request Response Based API
```bash
python request_response_api.py
```
## Check the response time in Postman
```javascript
{
    "post_id": "post1",
    "interaction_type": "like",
    "user_id": "user1"
}
```

## Launch Event Driven API
```bash
python event_driven_interaction.py
```

## Check response time in Postman
