#   Importing required modules
#   BeautifulSoup is required to be able to webscrape.
from bs4 import BeautifulSoup

#   lxml is required for parsing our content which is extracted with BeautifulSoup.
import lxml
from lxml import etree

#   sys is needed for both command line arguments and sys.exit() in error handlers.
import sys

#   requests is used to make sure that the connection is established and for error handling.
import requests
from requests.exceptions import (
    RequestException,
    HTTPError,
    ConnectionError,
    Timeout,
    TooManyRedirects,
)

#   pyttsx3 is a text-to-speech library
import pyttsx3

#   argparse is required for parsing the command line arguments and for error handling
import argparse

#   pyfiglet is used to have more beautiful outputs on the screen, using ASCII characters/art.
import pyfiglet


#   the main function needs to arguments which are sound and city. If sound argument exists, it will have an audio output as well.
def main(sound, city):
    #   city_name and city_time are global variables so that they can be accessed by our functions and to be changed later on.
    global city_name, city_time
    city_name = city.capitalize()
    if city:
        try:
            city_time = timenow(city)
        except ValueError:
            sys.exit("❌ Invalid City Name.")
    else:
        sys.exit("❌ No City Name.")

    print(pyfiglet.figlet_format(f"{city_name}:    {city_time}"))
    if sound:
        try:
            say(city_time)
        except ValueError:
            sys.exit("❌ Invalid City Name.")


#   dictmacker() returns a dictionary in which keys are city names and values are times at the moment.
def dictmaker() -> dict:
    url = "https://www.timeanddate.com/worldclock/full.html"
    try:
        response = requests.get(url)
        html_content = response.text
        #   making our soup
        soup = BeautifulSoup(html_content, "lxml")
        tags = soup.find_all("td")
        cities = list()
        times = list()
        #   tags with even indexes are going to be in city rows and those with odd indexes will be in times.
        for tag in tags:
            if tags.index(tag) % 2 == 0:
                cities.append(tag.text)
            else:
                times.append(tag.text)
        worldclock = {key: value for key, value in zip(cities, times)}
        return worldclock
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


#   timenow function: Scrapes the website and returns worldclock times at the moment:
def timenow(city: str) -> str:
    final_key = ""
    tmp_dict = dictmaker()
    for key, value in tmp_dict.items():
        if city.capitalize() in key:
            final_key = key
            break
        else:
            continue
    if not final_key:
        final_key = city_finder(city.capitalize())
        if final_key:
            return tmp_dict[final_key].split(" ")[1]
        else:
            sys.exit("❌ City Not Found!")
    else:
        return tmp_dict[final_key].split(" ")[1]


#   city_finder function: Searches for the city name in the dictionary when the input is not 100% correct according to our list, it will find the closest city to what the user has typed in and returns the key if the user agrees with the search.
def city_finder(city: str) -> str:
    tmp_dict = dictmaker()
    letters_real = list()
    found_city = ""
    letters_city = list()
    for letter in city.lower():
        letters_city.append(letter)
    #   we remove a, e, o, u, u from the word because it's tend to be one of the most common mistakes when people are typing words with keyboards.
    letters_city = list(
        filter(lambda letter: letter not in ["a", "e", "o", "u", "i"], letters_city)
    )
    for key, _ in tmp_dict.items():
        letters_real = []
        for letter in key.lower():
            letters_real.append(letter)
        #   "*" is used in front of each capital city in our dictionary, so we don't need it now, and we don't need it when using say function. We don't want the say function to say: Time in Bucharest asterics is 20:42
        letters_real = list(
            filter(
                lambda letter: letter not in ["a", "e", "o", "u", "i", "*"],
                letters_real,
            )
        )
        common = len(set(letters_real).intersection(set(letters_city)))
        #   after eliminating a, e, o , u and i from each word, if the similiarities between them are more than 70%, it will be shown up on the screen for the user to verify.
        if (common / len(letters_real)) * 10 > 7:
            answer = input(f"Did you mean {key.capitalize()}?    y/n   ")
            if answer in ["yes", "y", "yeah", "yup"]:
                found_city = key
                break
            else:
                continue
    global city_name
    city_name = found_city
    return found_city


#   say function: A text-to-speech function built with pyttsx3:
def say(text: str):
    engine = pyttsx3.init()
    engine.say(f"It is {text} in {city_name.replace('*', '')}.")
    engine.runAndWait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Have The World Clock With Only 2 Command Line Arguments! Don't Have Time To Read It On Your Screen? No Worries!, I Got You Covered With Text To Speech Feature!"
    )
    parser.add_argument(
        "--sound", action="store_true", help="activates text-to-speech feature"
    )
    parser.add_argument("--city", help="city name")

    args = parser.parse_args()

    main(args.sound, args.city)
