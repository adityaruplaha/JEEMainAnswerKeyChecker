import json
import re

class ResponseScraper:
    def __init__(self):
        self.data = {
            "candidate" : {},
            "test" : {},
            "questions" : {
                "mcq" : [],
                "numerical" : []
            }
        }

    @staticmethod
    def sane_int(x):
        if x == '--':
            return None
        try:
            return int(x)
        except ValueError:
            return None

    @staticmethod
    def sane_float(x):
        if x == '--':
            return None
        try:
            return float(x)
        except ValueError:
            return None


    def parse(self, file):
        application_no_reg = re.compile(r'Application No\s+(\d+)', re.M)
        name_reg = re.compile(r'Candidate Name\s+([\w ]+)', re.M)
        roll_reg = re.compile(r'Roll No\.\s+([\w\d]+)', re.M)
        test_date_reg = re.compile(r'Test Date\s+(\d{02}\/\d{02}\/\d{04})', re.M)
        test_time_reg = re.compile(r'Test Time\s+([\w\d\: \-]+)', re.M)

        data = file.read()

        self.data["candidate"]["application_no"] = application_no_reg.search(data).group(1)
        self.data["candidate"]["name"] = name_reg.search(data).group(1)
        self.data["candidate"]["roll"] = roll_reg.search(data).group(1)
        self.data["test"]["test_date"] = test_date_reg.search(data).group(1)
        self.data["test"]["test_time"] = test_time_reg.search(data).group(1)
        
        mcq_reg = re.compile(r'Question Type\s+:\s+MCQ\n\s+Question ID\s+:\s+(\d+)\n\s+Option 1 ID\s+:\s+(\d+)\n\s+Option 2 ID\s+:\s+(\d+)\n\s+Option 3 ID\s+:\s+(\d+)\n\s+Option 4 ID\s+:\s+(\d+)\n\s+Status\s+:\s+[\w\s]+\n\s+Chosen Option\s+:\s+([-\d]+)\n', re.M)
        mcqs = mcq_reg.finditer(data)

        for match in mcqs:
            self.data["questions"]["mcq"].append({
                "question_id" : int(match.group(1)),
                "option_1" : int(match.group(2)),
                "option_2" : int(match.group(3)),
                "option_3" : int(match.group(4)),
                "option_4" : int(match.group(5)),
                "chosen" : self.sane_int(match.group(6))
            })

        numerical_reg = re.compile(r'Given\s+([-\d]+)\n\s+Answer :\s+\s+Question Type\s+:\s+SA\n\s+Question ID\s+:\s+(\d+)', re.M)
        nums = numerical_reg.finditer(data)

        for match in nums:
            self.data["questions"]["numerical"].append({
                "question_id" : int(match.group(2)),
                "given" : self.sane_float(match.group(1))
            })

    def dump(self, file):
        json.dump(self.data, file)