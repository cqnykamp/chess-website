import csv

'''I need a way to ensure that my files don't have any repeats'''
def __init__(self, csv_file_name):        
    with open(csv_file_name) as file:
        csv_reader = csv.reader(file, delimiter=',')
        counter = 1
        athletes = open("athletes.csv", "a")
        noc = open("noc_region.csv", "a")
        season = open("season.csv", "a")
        game = open("game.csv", "a")
        sport_cat = open("sport_cat.csv", "a")
        events = open("events.csv", "a")
        while counter < len(csv_reader):
            line = csv_reader[counter]
            create_athletes(athletes, line)
            create_noc(noc, line, counter)

        athletes.close
        noc.close
        season.close
        game.close
        sport_cat.close
        events.close
        

    pass

def create_athletes(self, file, line):
    file.write(line[0] + ","+ line[1])
    return

def create_noc(self, file, line, id):
    file.write(id + "," + line[7] + "," +  line[6])

