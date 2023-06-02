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
import pyfiglet


def main(sound, city):
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


def dictmaker() -> dict:
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


# FIXME: This function is not working properly
def city_finder(city: str) -> str:
    tmp_dict = dictmaker()
    letters_real = list()
    found_city = ""
    letters_city = list()
    for letter in city.lower():
        letters_city.append(letter)
    letters_city = list(
        filter(lambda letter: letter not in ["a", "e", "o", "u", "i"], letters_city)
    )
    for key, _ in tmp_dict.items():
        letters_real = []
        for letter in key.lower():
            letters_real.append(letter)
        letters_real = list(
            filter(
                lambda letter: letter not in ["a", "e", "o", "u", "i", "*"],
                letters_real,
            )
        )
        common = len(set(letters_real).intersection(set(letters_city)))
        #        print(f"Real: {letters_real}\nCity: {letters_city}\nCommon: {common}\n Percent: {common / len(letters_real) * 10}")
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
    engine.say(f"It is {text} in {city_name}.")
    engine.runAndWait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "--sound", action="store_true", help="activates text-to-speech feature"
    )
    parser.add_argument("--city", help="city name")

    args = parser.parse_args()

    main(args.sound, args.city)
