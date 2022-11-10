
CREATE TABLE users (
    id int,
    username text
);


CREATE TABLE openings (
    id int,
    opening_name text
);


CREATE TABLE games (
    id text,
    white_player_id integer,
    black_player_id integer,
    turns integer,
    moves text,
    white_player_rating integer,
    black_player_rating integer,
    victory_status text,
    winner text,
    rated_status boolean,
    opening_id integer,
    increment_code text
);