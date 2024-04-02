import datetime
import os.path
import time

from decouple import config
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from selenium import webdriver
from selenium.webdriver.common.by import By

SCOPES = ["https://www.googleapis.com/auth/calendar"]


"""
The function `create_event` is part of a script to create Google Calendar events based on data obtained by web scraping. 
It takes six parameters:

- `name`: A string representing the summary of the event to be created.
- `location`: A string representing the location of the event to be created.
- `description`: A string representing the description of the event to be created.
- `start`: A string with ISO format representing the start date and time of the event.
- `end`: A string with ISO format representing the end date and time of the event.
- `jb`: A string with the value of either "j" OR "b". If "j", the event is linked to the "Match" Calendar. If "b", 
  the event is linked to the "Referee" Calendar.

It returns nothing, but as a side effect, it creates a new event in the Google Calendar with the specified `name`,
`location`, `description`, `start`, and `end` and prints the link to the created event.
"""

def create_event(name, location, description, start, end, jb):
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
            
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        event = {
            'summary': name,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start,
                'timeZone': 'Europe/Budapest',
            },
            'end': {
                'dateTime': end,
                'timeZone': 'Europe/Budapest',
            }
        }
        cal_id = "primary"
        if jb == "j":
            cal_id = config("CAL_ID_MATCH")
        elif jb == "b":
            cal_id = config("CAL_ID_REF")
        event = service.events().insert(calendarId=cal_id, body=event).execute()
        print('Event created: ', event.get('htmlLink'))

    except HttpError as error:
        print(f"An error occurred: {error}")


merkozeskod = input('Mérkőzéskód: ')

jatekos_v_biro = input('Játékosként vagy bíróként (j/b): ').lower()
while jatekos_v_biro != "j" and jatekos_v_biro != "b":
    jatekos_v_biro = input('Játékosként vagy bíróként (j/b): ').lower()

# web scraping using selenium

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
driver.get(f"https://mksz.hu/jegyzokonyv/{merkozeskod}")
time.sleep(3)

helyszin = driver.find_element(by=By.XPATH, value="/html/body/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/table["
                                                  "3]/tbody/tr[2]/td[1]").text[9:]

hazai = driver.find_element(by=By.XPATH, value="/html/body/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/table["
                                               "1]/tbody/tr/td[1]").text[2:]

vendeg = driver.find_element(by=By.XPATH, value="/html/body/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/table["
                                                "1]/tbody/tr/td[3]").text[2:]

idopont_raw = driver.find_element(by=By.XPATH, value="/html/body/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/table["
                                                     "3]/tbody/tr[1]/td[1]").text

idopont = datetime.datetime.strptime(idopont_raw, "%Y. %m. %d. - %H:%M")

# we call the create event function to insert a new event into google calendar
create_event(f"{hazai} - {vendeg}",
             helyszin,
             f"https://www.mksz.hu/jegyzokonyv/{merkozeskod}",
             idopont.strftime("%Y-%m-%dT%H:%M:%S"),
             (idopont + datetime.timedelta(minutes=50)).strftime("%Y-%m-%dT%H:%M:%S"),
             jatekos_v_biro)
