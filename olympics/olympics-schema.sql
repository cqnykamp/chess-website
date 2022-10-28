CREATE TABLE athletes(
    id SERIAL
    full_name text
);
CREATE TABLE NOC(
    id SERIAL
    NOC text
    region text
);
CREATE TABLE season(
    id SERIAL
    season_name text
)
CREATE TABLE game(
    id SERIAL
    year integer
    season_id integer
    city text
)
CREATE TABLE sports_category{ 
    id SERIAL
    category text
}
CREATE TABLE events(
    id SERIAL
    category_id SERIAL
    event_name text
)
CREATE TABLE olympic