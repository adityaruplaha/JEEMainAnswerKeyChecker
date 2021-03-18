import json
import re

class KeyScraper:
    def __init__(self):
        self.data = {
            "questions" : {
                "mcq" : [],
                "numerical" : []
            }
        }

    @staticmethod
    def sane_int(x):
        if x == 'D':
            return 'D'
        try:
            return int(x)
        except ValueError:
            return None

    @staticmethod
    def sane_float(x):
        if x == 'D':
            return 'D'
        try:
            return float(x)
        except ValueError:
            return None

    def dump(self, file):
        json.dump(self.data, file)

class ProvisionalKeyScraper(KeyScraper):
    def parse(self, file):
        data = file.read()

        mcq_reg = re.compile(r'Objective\s+(\d+)\s+(\d+)', re.M)
        mcqs = mcq_reg.finditer(data)

        for match in mcqs:
            self.data["questions"]["mcq"].append({
                "question_id" : int(match.group(1)),
                "answer" : self.sane_int(match.group(2))
            })

        numerical_reg = re.compile(r'Descriptive\s+(\d+)\s+(\d+)', re.M)
        nums = numerical_reg.finditer(data)

        for match in nums:
            self.data["questions"]["numerical"].append({
                "question_id" : int(match.group(1)),
                "answer" : self.sane_float(match.group(2))
            })


class FinalKeyScraper(KeyScraper):
    def parse(self, file):
        data = file.read()

        mcq_reg = re.compile(r'\s+(\d{11})\s{3,6}(\d{11}|D)', re.M)
        mcqs = mcq_reg.finditer(data)

        for match in mcqs:
            answer = self.sane_int(match.group(2))
            if answer == 'D':
                print(f"SCRAPE: {int(match.group(1))} dropped.")
            self.data["questions"]["mcq"].append({
                "question_id" : int(match.group(1)),
                "answer" : self.sane_int(match.group(2))
            })

        numerical_reg = re.compile(r'\s+(\d{11})\s{3,6}(\d{1,10}|D)\s', re.M)
        nums = numerical_reg.finditer(data)

        for match in nums:
            answer = self.sane_float(match.group(2))
            if answer == 'D':
                print(f"SCRAPE: {int(match.group(1))} dropped.")
            self.data["questions"]["numerical"].append({
                "question_id" : int(match.group(1)),
                "answer" : self.sane_float(match.group(2))
            })
