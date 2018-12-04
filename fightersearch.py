import pandas as pd
import json
import requests





def fightersearch():  # function to search fighters and display win/loss record



    UFC = requests.get('http://ufc-data-api.ufc.com/api/v1/us/fighters')  # request the api with fighter data

    UFC = json.dumps(UFC.json(), indent=4)  #

    data = json.loads(UFC)

    choice = input(
        'Search a fighter: ').lower().title()  # user enters name of a fighter to be searched(not case sensitive)

    for fighter in data:  # if the fighter the user searches is in the api the name is displayed along with their wins and losses
        if fighter['first_name'].lower().title() + ' ' + fighter['last_name'].lower().title() == choice:
            print(choice, ':')
            print('Wins:', fighter['wins'], ' losses:', fighter['losses'], 'net wins: '
                  , (fighter['wins'] - (fighter['losses'])))
        else:
            print('Fighter not found! ')
            break




def main():
    fightersearch()  # fighter search  function called


if __name__ == "__main__": main()
