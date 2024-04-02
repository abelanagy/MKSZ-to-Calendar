This script scrapes the data of a Hungarian handball match and creates a google calendar event.

## Idea
This script solves a problem I had for some time, when I wanted to "import" my match dates into google calendar I had to do it manually.

I thought this could be easily automated, so I made a python script, which scrapes the webpage of MKSZ and after that it uses the google api to add a new calendar event to the specified account.

## Usage
If you want to use this application you should install all of the packages in requirements.txt.

Secondly, you should create your own credentials.json file, using this [guide](https://developers.google.com/calendar/api/quickstart/python).

Thirdly, you should use you own calendar ids, which you can get from your calendar's settings, mine looks like this: lotsofnumbersandletters@group.calendar.google.com

*You can also use "primary", instead of an id, which will point at your primary calendar.*

Finally, I recommend compiling an exe from this script, hence you could run it more easily and looks much nicer :). I used [this tool](https://pypi.org/project/auto-py-to-exe/) for converting.

If you need help using this script feel free to [contact me](mailto:abel.nagy26@gmail.com).