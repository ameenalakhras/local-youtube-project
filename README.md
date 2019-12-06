# local youtube project
`a website to download youtube videos and playlists for offline usage locally on the users PC`

-  the website structure is made in the assumption that it will transform later on into a Desktop app using Django.


### the website supports:
- download single youtube video.
- download a youtube public playlist.
- watch downloaded videos.
- watch videos in a playlist.
- download the youtbue playlist without downloading the videos.


## running the project:
#### 1- you must python 3.6 before running the next commands check [python official website](https://www.python.org/downloads/release/python-360/) fore more

#### 2- run the following commands in cmd:
- pip install -r requirements.txt
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver 8000

#### 3-open 127.0.0.1:8000/



## to do list:
- add docker to the website
- combine account_auth app and logAuthentication app.
- activate mp3 download.
- provide a phone view for the website.
