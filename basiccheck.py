#!/usr/bin/python3

import argparse
import re
import errno
import os
import sys
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup



def main():
    parser = argparse.ArgumentParser(description="Checks to make sure basic accessibility parameters are met.")

    parser.add_argument("Path", metavar="path", type=str, help="the path to the HTML file to check")

    args = parser.parse_args()

    path = args.Path

    # If path given is a url
    if (bool(urlparse(path).netloc)):
        html = BeautifulSoup(requests.get(path).text, "html.parser")
    # Check to make sure file exists
    else:
        try:
            f = open(path, "r")
        except OSError:
            print("Error - Could not read file: " + path, file=sys.stderr)
            sys.exit()
        html = BeautifulSoup(f.read(), "html.parser")
        f.close()

    #print(html)

    # Checks to make sure all images have an alt attribute
    for image in html.find_all("img"):
        #print(image)
        if (image.get("alt") is None):
            print("Warning - " + str(image) + " does not have an alt attribute")
        #else if image.get("alt") == "":
        #    print("Warning - " + str(image) " has alt=\"\". If this is intentional, ignore this warning.")

    # Checks to make sure input fieds have some kind of labeling
    # https://www.w3.org/WAI/tutorials/forms/labels/
    # https://webaim.org/techniques/forms/controls
    #for inputfield in html.find_all("input"):

    # Looks for drastic changes in header sizes (e.g. h1 to h3)
    headers = html.find_all(re.compile("^h[1-6]$"))
    for i in range(len(headers) - 1):
        if int(headers[i].name[1]) + 2 <= int(headers[i + 1].name[1]):
            print("Warning - There is a drastic change in header size from " + str(headers[i]) + " to " + str(headers[i+1]))
            #print(int(headers[i].name[1]) + 2)
            #print(headers[i + 1].name[1])

    # Checks to make sure all underlined text are links
    for underline in html.find_all("u"):
        print("Warning - Reserve underlined text for links only: " + str(underline))

    # Checks to make sure all font awesome icons use <span>
    itags = html.find_all("i", class_="fa")
    if len(itags) == 0:
        print("Nice Job - All your font awesome icons use <span>.")
    else:
        for itag in itags:
            print("Warning - Change the following <i> to <span>: " + str(itag))

    for itag in html.find_all("i"):
        if "fa" in itag["class"]:
            continue

        print("Warning - Please replace the following <i> tag with an <em> tag: " + str(itag))

    for utag in html.find_all("u"):
        if "fa" in utag["class"]:
            continue

        print("Warning - Please replace the following <u> tag with a <strong> tag: " + str(utag))

    for atag in html.find_all("a"):
        if len(atag.contents) == 0:
            print("Warning - The following <a> tag must contain some text: " + str(atag))


if __name__=="__main__":
    main()
