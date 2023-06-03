import pytest
import project
from project import dictmaker, timenow, city_finder, say


def test_dictmaker():
    assert type(dictmaker()) == dict
    worldclock = dictmaker()
    assert isinstance(worldclock, dict)
    assert len(worldclock) > 0


def test_timenow():
    worldclock = dictmaker()
    city = "Bucharest"
    assert type(timenow(city)) == str
    result = timenow(city)
    assert isinstance(result, str)
    assert len(result) > 0


def test_city_finder():
    worldclock = dictmaker()
    city = "Bucharest"
    result = city_finder(city)
    answer = "yes"
    assert isinstance(result, str)
    assert len(result) > 0


def test_say(capsys):
    city_name = 
    text = "Hello World!"
    say(text)
    captured = capsys.readouterr()
    assert captured.out.strip(
    ) == f"It is {text} in {city_name.replace('*', '')}."
