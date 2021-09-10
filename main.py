from response_scraper import ResponseScraper
from answer_scraper import ProvisionalKeyScraper
from answer_scraper import FinalKeyScraper
from checker import Checker

s = ResponseScraper(scraper='mains_2021')
with open("files/Recorded Response.txt") as f:
    s.parse(f, parse_candidate_details=False, parse_test_details=False)
with open("files/response.json", 'w') as f:
    s.dump_to(f)
    f.close()

''' ###
s = ProvisionalKeyScraper(scraper='mains_2021')
with open("files/Provisional Answer Key.txt") as f:
    s.parse(f)
with open("files/provisional_answer.json", 'w') as f:
    s.dump_to(f)
    f.close()

'''
s = FinalKeyScraper(scraper='mains_2021')
with open("files/Final Answer Key.txt") as f:
    s.parse(f)
with open("files/final_answer.json", 'w') as f:
    s.dump_to(f)
    f.close()
'''


with open("files/provisional_answer.json") as f:
    c = Checker(f)
'''
with open("files/final_answer.json") as f:
    c = Checker(f)
###

with open("files/response.json") as f:
    c.check(f)
    c.display_default()
