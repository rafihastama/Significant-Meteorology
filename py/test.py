import re
import xml.etree.ElementTree as ET
import lxml.etree as et
import pandas as pd
import json


def main():
    a = ['160']
    with open('flight_level.json') as file:
        data = json.load(file)
        for d in data:
            z = str(d['Flight Level'])
            if z == a[0]:
                print(d['Feet'], d['Meter'])


if __name__ == "__main__":
    main()
