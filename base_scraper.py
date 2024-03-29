import abc
import json
import re

class BaseScraper(abc.ABC):
    def __init__(self, scraper : str):
        known_scrapers = ["mains_2021", "mains_2022"]
        if scraper not in known_scrapers:
            raise ValueError("Given scraper doesn't exist.")
        self.scraper = scraper
        self.data = {}
        with open(f'scrapers/{self.scraper}/metadata.json') as f:
            self.metadata = json.load(f)

    def sane_int(self, x : str):
        x = x.strip()
        if x in self.metadata["null_list"]:
            return None
        try:
            return int(x)
        except ValueError:
            return None

    def sane_float(self, x : str):
        x = x.strip()
        if x in self.metadata["null_list"]:
            return None
        try:
            return float(x)
        except ValueError:
            return None

    def sane_str(self, x : str):
        x = x.strip()
        if x in self.metadata["null_list"]:
            return None
        return x

    def get_regexes(self, kind : str):
        scraper_file = open(f'scrapers/{self.scraper}/{kind}.json')
        data = json.load(scraper_file).items()
        scraper_file.close()
        return dict((k, re.compile(i, re.M)) for (k, i) in data)

    def dump_to(self, file):
        json.dump(self.data, file)