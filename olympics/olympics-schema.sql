CREATE TABLE athletes(
    id SERIAL
    full_name text
);
CREATE TABLE noc(
    id SERIAL
    noc text
);
CREATE TABLE region(
    id SERIAL
    region text
);
CREATE TABLE game(
    id SERIAL
    year integer
    game text
    city text
);
CREATE TABLE sports_category( 
    id SERIAL
    category text
);
CREATE TABLE events(
    id SERIAL
    category_id SERIAL
    event_name text
);
CREATE TABLE {
    athlete_id SERIAL
    noc text
    region text
    game_id SERIAL
    event_id SERIAL
    
}