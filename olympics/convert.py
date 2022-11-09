'''
    CS 257 Software Design
    Prof. Jeff Ondich
    Author: Barinamene Nwike

    This program gets data from an olympic dataset from
    kaggkle 
    https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results
'''

import csv

game_count = 0
player_ids = []
noc_list = []
region_list = []
game_list = []
sports_list = []
event_list = []
'''I need a way to ensure that my files don't have any repeats'''
def __init__(self, csv_file_name):        
    with open(csv_file_name) as file:
        csv_reader = csv.reader(file, delimiter=',')
    collection = [open("athletes.csv", "a"), 
    open("noc.csv", "a"), 
    open("regions.csv", "a"),
    open("game.csv", "a"),
    open("sport_cat.csv", "a"),
    open("events.csv", "a")]
    file_writer(collection, csv_reader)

        
def file_writer(self, file_collection, reader):
    counter = 1
    while counter < len(reader):
        line = reader[counter]
        create_athletes(file_collection[0], line)
        create_noc(file_collection[1], line)
        create_regions(file_collection[2], line)
        create_game(file_collection[3], reader)
        create_sport_categories(file_collection[4], reader)
        create_events(file_collection[5], reader)
        counter+=1
    for text_file in file_collection:
        text_file.close


def create_athletes(self, file, line):
    if(line[0] not in player_ids):
        file.write(line[0] + ","+ line[1] + "\n")
        player_ids += line[0]
    pass

def create_noc(self, file, line):
    if(line[3] not in noc_list):
        noc_list.append(line[3])
        file.write(len(noc_list)+","+line[3]+"\n")
    pass

def create_regions(self, file, line):
    if(line[4] not in region_list):
        noc_list.append(line[4])
        file.write(len(noc_list) + ","+line[4]+"\n")
    pass

def create_game(self, file, line):
    if(line[5] not in game_list):
        game_list.append(line[5])
        file.write(len(game_list) +","+int(line[6]) +","+ line[5]+","+line[8]+"\n")
    pass

def create_sport_categories(self, file, line):
    if(line[9] not in sports_list):
        sports_list.append(line[9])
        file.write(len(sports_list) + ","+line[9]+"\n")
    pass

def create_events(self, file, line):
    if(line[10] not in event_list):
        event_list.append(line[10])
        file.write(len(event_list) + "," + line[9]+ "," +  line[10] + "\n")
    pass
