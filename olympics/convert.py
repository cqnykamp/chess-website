import csv

game_count = 0
player_ids = []
game_list = []
sports_ids = []
'''I need a way to ensure that my files don't have any repeats'''
def __init__(self, csv_file_name):        
    with open(csv_file_name) as file:
        csv_reader = csv.reader(file, delimiter=',')
        write_files(csv_reader)

    pass

def write_files(self, csv_reader):
    counter = 1

    athletes = open("athletes.csv", "a")
    season = open("season.csv", "a")
    game = open("game.csv", "a")
    sport_cat = open("sport_cat.csv", "a")
    events = open("events.csv", "a")
    while counter < len(csv_reader):
        line = csv_reader[counter]
        create_athletes(athletes, line)
        counter+=1
    athletes.close
    season.close
    game.close
    sport_cat.close
    events.close
        

def create_athletes(self, file, line):
    if(line[0] not in player_ids):
        file.write(line[0] + ","+ line[1] + "\n")
        player_ids += line[0]
    pass

def create_sport_categories(self, file, line, id):
    if(line[9] not in sports_ids):
        file.write(id + ","+line[9])
    pass

def create_(self, file, line, id):
    file.write(str(id) + "," + line[7] + "," +  line[6] + "\n")
    pass

def create_game(self, file, line, id):
            if(line[5] not in game_list):
            create_game(game, line, game_count)
            game_count += 1
    file.write(str(id) +"," + LI )
    pass