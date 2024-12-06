CREATE TABLE user (user_id TEXT PRIMARY KEY, genre TEXT, affinity_score TEXT);
CREATE TABLE interactions (post_id TEXT, interaction_type TEXT, interaction_by TEXT, timestamp TEXT);
CREATE TABLE posts (post_id TEXT, genre TEXT, likes INTEGER, comments INTEGER, timestamps TEXT, popularity_score REAL);



INSERT INTO posts (post_id, likes, comments, timestamps, popularity_score) VALUES ('post1', 10, 5, '2024-12-01 10:00:00', 15.0);
INSERT INTO posts (post_id, likes, comments, timestamps, popularity_score) VALUES ('post2', 20, 8, '2024-12-01 11:00:00', 25.0);
INSERT INTO posts (post_id, likes, comments, timestamps, popularity_score) VALUES ('post3', 5, 2, '2024-12-01 12:00:00', 7.0);
INSERT INTO posts (post_id, likes, comments, timestamps, popularity_score) VALUES ('post4', 15, 10, '2024-12-01 13:00:00', 20.0);
INSERT INTO posts (post_id, likes, comments, timestamps, popularity_score) VALUES ('post5', 8, 3, '2024-12-01 14:00:00', 11.0);


INSERT INTO interactions (post_id, interaction_type, interaction_by, timestamp) VALUES ('post1', 'like', 'user1', '2024-12-01 15:00:00');
INSERT INTO interactions (post_id, interaction_type, interaction_by, timestamp) VALUES ('post2', 'like', 'user2', '2024-12-01 15:10:00');
INSERT INTO interactions (post_id, interaction_type, interaction_by, timestamp) VALUES ('post3', 'comment', 'user3', '2024-12-01 15:20:00');
INSERT INTO interactions (post_id, interaction_type, interaction_by, timestamp) VALUES ('post4', 'like', 'user4', '2024-12-01 15:30:00');
INSERT INTO interactions (post_id, interaction_type, interaction_by, timestamp) VALUES ('post5', 'like', 'user5', '2024-12-01 15:40:00');
