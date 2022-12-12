# touhou-ost-listener
Plays Touhou music with some options for good experience

### Requirements
- Python
- Selenium (pip install selenium)
- Google Chrome browser
- Version of chromedriver that compatible with your Google Chrome (https://chromedriver.chromium.org/downloads)

### Usage:
Program can play music from start to end, from random second for N seconds. Can wait for user's input before a next track.
You can turn on/off repetitions of tracks and add/remove some music from main playlist. That's all.
Next track is always chosen randomly.
You can go sleep with this...

SWITCHERS.ini - List of games, you can enable/disable game that needs to be enabled/disabled...
currentbaseNums.ini - Tracks from giant current_urls list separated
current_urls, current_timings - URLs and their lenghts

base, temp_urls - For adding your own tracks in main playlist (using Excel and good hands)

Waiting for something to happen? (1 - repeat, 0 or something - continue)
