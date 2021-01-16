import tweepy
from datetime import datetime
from dateutil.relativedelta import relativedelta
from PIL import Image, ImageDraw, ImageFont
import os

COLORS  = {
    "FOREGROUND": "#57cc8a",
    "BACKGROUND": "#242930",
    "WHITE": "#FFFFFF",
}
FONTS = {
    "TITLE": ImageFont.truetype(".github/fonts/OpenSans-Regular.ttf",40),
    "NUMBERS": ImageFont.truetype(".github/fonts/OpenSans-ExtraBold.ttf",60),
    "SUBTITLE": ImageFont.truetype(".github/fonts/OpenSans-Light.ttf",20),
}


def drawnumbers(draw,numbers):
    width = 1500
    num = len(numbers)
    offset = width/num
    x = offset/2
    for number in numbers:
        draw.text((x,250),f"{number[1]}", fill=COLORS["FOREGROUND"], font=FONTS["NUMBERS"],anchor="mm")
        draw.text((x,300),f"{number[0]}", fill=COLORS["WHITE"], font=FONTS["SUBTITLE"],anchor="mm")
        x = x + offset

def drawheader(data):
    img = Image.new('RGB',(1500,500),color=COLORS["BACKGROUND"])
    d=ImageDraw.Draw(img)
    d.text((750,50),f"{data['name']}'s Twitter Stats", fill=COLORS["FOREGROUND"], font=FONTS["TITLE"],anchor="mm")
    d.text((750,100),f"Twitter Age: {data['age']}",fill=COLORS["WHITE"],font=FONTS["SUBTITLE"],anchor="mm")
    drawnumbers(d, [
        ("Followers",data['followers']),
        ("Tweets",data['tweets']),
        ("Lists I am on",data['lists']),
        ("Tweets Liked",data['likes']),
    ])
    d.multiline_text((750,450),"This Header Image has been generated using code. The code runs every 2 hours\nCode: github.com/haideralipunjabi/twitter-header-python",fill=COLORS["WHITE"],font=FONTS["SUBTITLE"],anchor="mm",align="center")
    img.save("header.png")

def get_api():
    auth = tweepy.OAuthHandler(os.environ["CONSUMER_KEY"],os.environ["CONSUMER_SECRET"])
    auth.set_access_token(os.environ["ACCESS_TOKEN"],os.environ["ACCESS_TOKEN_SECRET"])
    return tweepy.API(auth)
   
def get_data(api):
    data = api.me()._json
    rd = relativedelta(datetime.now(),datetime.strptime(data["created_at"],"%a %b %d %H:%M:%S +0000 %Y"))
    return {
        "name": data["name"],
        "age": f"{rd.years} years, {rd.months} months, {rd.days} days",
        "followers": data["followers_count"],
        "lists": data["listed_count"],
        "tweets": data["statuses_count"],
        "likes": data["favourites_count"]
    }

api = get_api()
drawheader(get_data(api))
api.update_profile_banner('header.png')