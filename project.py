from bs4 import BeautifulSoup
import lxml
from lxml import etree
import sys
import requests
from requests.exceptions import (
    RequestException,
    HTTPError,
    ConnectionError,
    Timeout,
    TooManyRedirects,
)
import pyttsx3
import argparse


def main(sound, city):
    global city_name, city_time
    city_name = city
    if city:
        city_time = timenow(city)
    else:
        print("No city specified")

    if sound:
        say(city_time)

    print(city_time)

#   timenow function: Scrapes the website and returns worldclock times at the moment:
def timenow(city: str) -> str:
    url = "https://www.timeanddate.com/worldclock/full.html"
    try:
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, "lxml")
        tags = soup.find_all("td")
        cities = list()
        times = list()
        for tag in tags:
            if tags.index(tag) % 2 == 0:
                cities.append(tag.text)
            else:
                times.append(tag.text)
        worldclock = {key: value for key, value in zip(cities, times)}
        for key, value in worldclock.items():
            if city.capitalize() in key:
                return value.split(" ")[1]
        else:
            sys.exit("❌ Could not find the city!")
         
    #   ERROR HANDLING
    except HTTPError as e:
        sys.exit("❌ HTTP error occurred:", e)
    except ConnectionError as e:
        sys.exit("❌ Network connection error occurred:", e)
    except Timeout as e:
        sys.exit("❌ Timeout error occurred:", e)
    except TooManyRedirects as e:
        sys.exit("❌ Too many redirects occurred:", e)
    except RequestException as e:
        sys.exit("❌ An error occurred:", e)


#   say function: A text-to-speech function built with pyttsx3:
def say(text: str):
    engine = pyttsx3.init()
    engine.say(f"The Time In {city_name} is {text}.")
    engine.runAndWait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--sound", action="store_true", help="activates text-to-speech feature")
    parser.add_argument("--city", help="city name")

    args = parser.parse_args()

    main(args.sound, args.city)
