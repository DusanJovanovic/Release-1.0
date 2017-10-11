# -*- coding: utf-8 -*-
"""
This code is made in haste. No tests, no exceptions, no defensive coding.
Its main purpose is to show my web scraping abilities.
"""

import requests
import json
from bs4 import BeautifulSoup
from payload import Payload
import time


def get_region_codes(region):
    """
   This function is not finished completely.
   It is oversimplified and it needs better implementation.
   However it is possible to find city codes such as Basel and Winterthur
   which will be enough for our example.
   This function retreives a list of dictionaries which contains codes for
   the cities and regions.
   This function may be implemented as a static method in class Payload in future releses.
   Example dicts: {Key: 188542, DisplayText: "Winterthur", Range: 3, Zip: null}
   {Key: 188000, DisplayText: "Basel", Range: 3, Zip: null}
   {Key: 196298, DisplayText: "Sion", Range: 3, Zip: null}
   {Key: 353, DisplayText: "1528 Surpierre", Range: 4, Zip: "1528"}
   """
    r = requests.post("http://www.urbanhome.ch/Region/GetSearchItems", json={"countryID": 0})
    codes = json.loads(r.text)
    for code in codes:
        if code["DisplayText"] == region:
            return str(code["Key"])
    return ""


def retreive_links(payload):
    """
    POST method sends json file with search params and receives a json file.
    Key "Rows" contains all we need to retrieve links that match our search criteria.
    """
    r = requests.post("http://www.urbanhome.ch/Search/DoSearch", json=payload)
    obj = json.loads(r.text)
    soup = BeautifulSoup(obj["Rows"], "lxml")
    list_li = soup.find_all("li")
    for el_index, el in enumerate(list_li):
        # raw string from onclick is full of \'" which I could clean with 4 replace methods
        # there is probably a better way to clean it but it works for now
        link = el["onclick"].replace("'", "").replace("\"window.open(", "").replace("\\", "").replace(");", "")
        print("{} out of {} links.".format(el_index + 1, len(list_li)))
        yield link


def parse_link(link, region):
    """
    This function is also not finished.
    I need more clarification on json structure.
    Also either links must be translated from German to English or retreived text.
    I hope that this implementation can work for now as an example.
    """
    data = {}
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "lxml")
    data["name"] = soup.find("h1").text
    zip_code = soup.find("span", {"itemprop": "postalCode"}).text
    data["address"] = {
            "city": soup.find("span", {"itemprop": "addressLocality"}).text[:-3],
            "street": soup.find("span", {"itemprop": "streetAddress"}).text,
            "zipCode": 0 if zip_code is None else zip_code, }
    additionalFeatures = soup.find("div", {"class": "a d"})
    small = additionalFeatures.find_all("small")
    data["additionalFeatures"] = {}
    for feature in small:
        data["additionalFeatures"][feature.text.replace("✓", "")] = True

    with open("{}_{}_{}.json".format(region,
              time.strftime("%d-%m-%Y"),
              time.strftime("%H_%M_%S")), "wt", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def main():
    region = "Winterthur"
    payload_winterthur = Payload()
    winterthur_code = get_region_codes(region)
    payload_winterthur.change_region(winterthur_code)
    for link in retreive_links(payload_winterthur.payload):
        parse_link(link, region)


if __name__ == "__main__":
    main()
