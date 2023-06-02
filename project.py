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
            return tmp_dict(final_key).split(" ")[1]
        else:
            sys.exit("❌ City Not Found!")
    else:
        return tmp_dict[final_key].split(" ")[1]


        
def city_finder(user_input: str) -> str:
    tmp_dict = dictmaker()
    result = ""
    tmp_key_letters = list()
    tmp_user_input_letters = list()
    for letter in user_input.capitalize():
        tmp_user_input_letters.append(letter)
#    score = 0
    for key, _ in tmp_dict:
        if result:
            return result
            break
        else:
            for letter in key:
                tmp_key_letters.append(letter)
            if tmp_key_letters[0] == tmp_user_input_letters[0] and tmp_key_letters[1] == tmp_user_input_letters[1] and tmp_key_letters[2] == tmp_user_input_letters[2]:
                result = "".join(tmp_key_letters)
                answer = input(f"Did You Mean {result}?")
                if answer.lower() in ["yes", "y", "yup", "yeah"]:
                    result = "".join(tmp_key_letters)
                    break
                else:
                    sys.exit("Please Try Again!")
            else:
                continue   
    return result


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
