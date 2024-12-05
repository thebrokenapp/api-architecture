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

## Create Interaction REST API
