
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
    increment_code text,
    opening_ply integer,

    opening1 int,
    opening2 int,
    opening3 int,
    opening4 int,

    checks smallint,
    captures smallint,
    en_passants smallint,
    castles smallint,
    promotions smallint,

    capturing_kings smallint,
    capturing_queens smallint,
    capturing_rooks smallint,
    capturing_knights smallint,
    capturing_bishops smallint,
    capturing_pawns smallint,

    captured_queens smallint,
    captured_rooks smallint,
    captured_knights smallint,
    captured_bishops smallint,
    captured_pawns smallint
);
