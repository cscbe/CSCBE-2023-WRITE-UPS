INSERT INTO users (username, password) VALUES (
    'Admin', 
    '$2a$12$OMXRomyyqT8LEEAVnCuqzO1a88Yt01pvlu7mfj85zHlFCvT7Rk0zK'
);


INSERT INTO photos (title, url, user_id, visible) VALUES 
(
    'Welcome to Horizon',
    'https://cybersecuritychallenge.be/assets/images/header-bg.jpg',
    LAST_INSERT_ID(), 
    1
),
(
    -- TODO: change before distributing to contestants.
    'CSC{This_is_why_you_should_use_prepared_statements}',
    'https://cybersecuritychallenge.be/assets/images/header-bg.jpg',
    LAST_INSERT_ID(), 
    0
);