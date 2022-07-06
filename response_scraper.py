import json
import re

from base_scraper import BaseScraper
class ResponseScraper(BaseScraper):
    def __init__(self, scraper : str):
        super().__init__(scraper=scraper)
        self.data = {
            "candidate" : {},
            "test" : {},
            "questions" : {
                "mcq" : [],
                "numerical" : []
            }
        }

    def get_regexes(self):
        return super().get_regexes('response')

    def parse(self, file, parse_candidate_details=True, parse_test_details=True): 
        data = file.read()

        regs = self.get_regexes()

        if parse_candidate_details:
            for i in ["application_no","name","roll"]:
                self.data["candidate"][i] = regs[i].search(data).group(1)
        if parse_test_details:
            for i in ["test_date"]:
                self.data["test"][i] = regs[i].search(data).group(1)
        
        mcqs = regs["mcq"].finditer(data)

        if self.metadata["method"] == "qid_oid":
            for match in mcqs:
                self.data["questions"]["mcq"].append({
                    "question_id" : int(match.group('qid')),
                    "option_1" : int(match.group('o1id')),
                    "option_2" : int(match.group('o2id')),
                    "option_3" : int(match.group('o3id')),
                    "option_4" : int(match.group('o4id')),
                    "chosen" : super().sane_int(match.group('chosen'))
                })
        elif self.metadata["method"] == "qid_opt":
            for match in mcqs:
                self.data["questions"]["mcq"].append({
                    "question_id" : int(match.group('qid')),
                    "chosen" : super().sane_str(match.group('chosen'))
                })
        else:
            pass # WTF

        nums = regs["numerical"].finditer(data)

        for match in nums:
            self.data["questions"]["numerical"].append({
                "question_id" : int(match.group('qid')),
                "given" : super().sane_float(match.group('given'))
            })