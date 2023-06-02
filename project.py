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


def main():
    print(timenow("Bucharest"))


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
            if city in key:
                return value

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


if __name__ == "__main__":
    main()
