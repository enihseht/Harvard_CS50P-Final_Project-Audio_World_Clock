from project import dictmaker, timenow, city_finder, reqcheck
import pytest
import requests


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


def test_reqcheck():
    assert type(reqcheck("https://youtube.com")) == bool
    assert reqcheck("https://youtube.com") == True
