import json
import re

from base_scraper import BaseScraper

class KeyScraper(BaseScraper):
    def __init__(self, scraper : str):
        super().__init__(scraper=scraper)
        self.data = {
            "questions" : {
                "mcq" : [],
                "numerical" : []
            }
        }

    def parse_as(self, file, kind):
        data = file.read()

        regs = self.get_regexes(kind=kind)
        mcqs = regs['mcq'].finditer(data)

        if self.metadata["method"] == "qid_oid":
            for match in mcqs:
                self.data["questions"]["mcq"].append({
                    "question_id" : int(match.group('qid')),
                    "answer" : self.sane_int(match.group('ans'))
                })
        elif self.metadata["method"] == "qid_opt":
            for match in mcqs:
                self.data["questions"]["mcq"].append({
                    "question_id" : int(match.group('qid')),
                    "answer" : self.sane_str(match.group('ans'))
                })
        else:
            pass # WTF

        nums = regs['numerical'].finditer(data)

        for match in nums:
            self.data["questions"]["numerical"].append({
                "question_id" : int(match.group('qid')),
                "answer" : self.sane_float(match.group('ans'))
            })

class ProvisionalKeyScraper(KeyScraper):
    def __init__(self, scraper : str):
        super().__init__(scraper=scraper)

    def parse(self, file):
        return super().parse_as(file, 'provisional_answer')

class FinalKeyScraper(KeyScraper):
    def __init__(self, scraper : str):
        super().__init__(scraper=scraper)

    def parse(self, file):
        return super().parse_as(file, 'final_answer')
