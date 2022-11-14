

import csv
import chess

import chess_util


def main():

    users = {}
    openings = {}

    opening_count = 0
    user_count = 0

    board = chess.Board()

    max_openings_found_per_game = 0


    with open('data/original.csv') as dataset, \
        open('data/users.csv', 'w') as users_csv, \
        open('data/games.csv', 'w') as games_csv, \
        open('data/openings.csv', 'w') as openings_csv:
        # open('data/games_openings.csv', 'w') as games_openings_csv:

        reader = csv.reader(dataset, delimiter=',', quotechar='"')
        heading_row = next(reader)

        games_writer = csv.writer(games_csv)
        # games_openings_writer = csv.writer(games_openings_csv)

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
            openings_unparsed = row[14]
            opening_ply = row[15]
            
            # Add this username to the userlist if not already there, and get it's corresponding id
            white_user_id = None
            if white_username in users:
                white_user_id = users[white_username]
            else:
                white_user_id = user_count
                users[white_username] = white_user_id
                user_count += 1

            # Add this username to the userlist if not already there, and get it's corresponding id
            black_user_id = None
            if black_username in users:
                black_user_id = users[black_username]
            else:
                black_user_id = user_count
                users[black_username] = black_user_id
                user_count += 1

            parsed_openings = openings_unparsed.split("|")
            for i in range(0, len(parsed_openings)):
                parsed_openings[i] = parsed_openings[i].strip()

            if len(parsed_openings) > max_openings_found_per_game:
                max_openings_found_per_game = len(parsed_openings)


            # Add these openings to the opening list if not already there, and get their corresponding ids

            # The numbe of elements in the list correspond to the number of field the db has for openings
            opening_ids = ['NULL', 'NULL', 'NULL', 'NULL']

            for i in range(0, len(parsed_openings)):
                opening = parsed_openings[i]
                if opening in openings:
                    opening_ids[i] = openings[opening]
                else:
                    openings[opening] = opening_count
                    opening_ids[i] = opening_count
                    opening_count += 1
            
            
            # Generate some data about what happened in the game
            checks = 0
            captures = 0
            en_passants = 0
            castles = 0
            promotions = 0

            board.reset()
            board.clear_stack()

            capturing_pieces = {
                'k': 0,
                'q': 0,
                'r': 0,
                'b': 0,
                'n': 0,
                'p': 0,
            }
            captured_pieces = {
                'q': 0,
                'r': 0,
                'b': 0,
                'n': 0,
                'p': 0,
            }

            for move_string in moves.split(" "):
                move = board.parse_san(move_string)

                if board.gives_check(move):
                    checks += 1
                if board.is_capture(move):
                    captures += 1
                    capturing_pieces[ chess_util.capturing_piece_type(board, move).lower() ] += 1
                    captured_pieces[ chess_util.captured_piece_type(board, move).lower() ] += 1

                if board.is_en_passant(move):
                    en_passants += 1
                if board.is_castling(move):
                    castles += 1
                if move.promotion != None:
                    promotions += 1

                board.push(move)


            # Write one game to our csv
            games_writer.writerow([
                game_id, white_user_id, black_user_id, turns, moves, white_rating, black_rating, \
                victory_status, winner, rated_status, increment_code, opening_ply, \
                opening_ids[0], opening_ids[1], opening_ids[2], opening_ids[3], \
                checks, captures, en_passants, castles, promotions, \

                capturing_pieces['k'], capturing_pieces['q'], capturing_pieces['r'], \
                capturing_pieces['n'], capturing_pieces['b'], capturing_pieces['p'], \


                captured_pieces['q'], captured_pieces['r'], captured_pieces['n'], \
                captured_pieces['b'], captured_pieces['p'],

            ])

            # for opening_id in opening_ids:
            #     games_openings_writer.writerow([game_id, opening_id])
            

        users_writer = csv.writer(users_csv)
        for username in users:
            users_writer.writerow([users[username], username])

        openings_writer = csv.writer(openings_csv)
        for opening in openings:
            openings_writer.writerow([openings[opening], opening])

        print("Max openings found per game is", max_openings_found_per_game)




if __name__ == '__main__':
    main()