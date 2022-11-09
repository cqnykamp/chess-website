
import csv


def main():

    users = {}
    openings = {}

    opening_count = 0
    user_count = 0

    with open('data/original.csv') as dataset, \
        open('data/users.csv', 'w') as users_csv, \
        open('data/games.csv', 'w') as games_csv, \
        open('data/openings.csv', 'w') as openings_csv:

        reader = csv.reader(dataset, delimiter=',', quotechar='"')
        heading_row = next(reader)

        games_writer = csv.writer(games_csv)

        for row in reader:
            game_id = row[0]
            rated_status = row[1]
            turns = row[4]
            victory_status = row[5]
            winner = row[6]
            increment_code = row[7]
            white_username = row[8]
            white_rating = row[9]
            black_username = row[10]
            black_rating = row[11]
            moves = row[12]
            opening = row[14]
            
            
            white_user_id = None
            if white_username in users:
                white_user_id = users[white_username]
            else:
                white_user_id = user_count
                users[white_username] = white_user_id
                user_count += 1


            black_user_id = None
            if black_username in users:
                black_user_id = users[black_username]
            else:
                black_user_id = user_count
                users[black_username] = black_user_id
                user_count += 1


            opening_id = None
            if opening in openings:
                opening_id = openings[opening]
            else:
                opening_id = opening_count
                openings[opening] = opening_id
                opening_count += 1


            games_writer.writerow([game_id, white_user_id, black_user_id, turns, moves, white_rating, black_rating, victory_status, winner, opening_id, increment_code]) 
            

        users_writer = csv.writer(users_csv)
        for username in users:
            users_writer.writerow([users[username], username])

        openings_writer = csv.writer(openings_csv)
        for opening in openings:
            openings_writer.writerow([openings[opening], opening])




if __name__ == '__main__':
    main()