from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from gameEntry import gameEntry
import requests
import json
from collections import namedtuple

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1hJjy6i2IZgFRaTxkzex4b4B2ElhJeBS5qGxs6_HaH0Q'
DATA_RANGE = '2020-2021!I7:N36'

def validateCredentials():
    creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def jsonDecoder(inDict):
    return namedtuple('X', inDict.keys())(*inDict.values())

def main():
    
    creds = validateCredentials()

    service = build('sheets', 'v4', credentials=creds)

   
    # Call the Sheets API
    sheet = service.spreadsheets()

    #Call for our spreadsheet data
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=DATA_RANGE).execute()
    values = result.get('values', [])
    gamesList = []
    if not values:
        print('No data found.')
    else:
        print('Date, Game:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            gameInfo = []
            for item in row:
                gameInfo.append(item) # 0- Date 1- Time (Not Needed) 2-Team1 3-Score1 4-Team2 5-Score2 
            gamesList.append(gameEntry(gameInfo))

    
    headers = {
    'x-rapidapi-host': "therundown-therundown-v1.p.rapidapi.com",
    'x-rapidapi-key': "fc38ba7c2amshb4f7ac7fa53eec6p1572d9jsn3c5562ed234b"
    }
    scheduleURL = "https://therundown-therundown-v1.p.rapidapi.com/sports/4/schedule"
    
    #softbreak tmp
    tmpI = 0
    oldDate = ""

    for game in gamesList:
        #Get the Date
        #Request that date's schedule from the API
        newDate = game.printDate()

        #Check to make sure we arent pulling the same date
        if(oldDate != newDate):
            query = {"limit":"25", "from": game.printDate()}
            response = requests.request("GET", scheduleURL, headers=headers, params=query)
            scheduleObject = json.loads(response.text)

        #Each game is represented by event,a dictionary
        homeTeam = game.home.rsplit(' ', 1)[0]
        awayTeam = game.visitor.rsplit(' ', 1)[0]
        for event in scheduleObject['schedules']:

            #Compare home and away teams, if it's the same, save the event ID
            if(homeTeam == event["home_team"] and awayTeam == event["away_team"]):
               print(event["event_id"])
               game.eventID  = event["event_id"]

        oldDate = newDate
        #Compare each event to the current game
        #Once proper eventID is found, query again for the event's odds
        #Write those odds, to the spreadsheet (might save for different loop)
        tmpI += 1
        if tmpI > 2:
            break
        

if __name__ == '__main__':
    main()