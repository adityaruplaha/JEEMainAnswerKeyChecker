from response_scraper import ResponseScraper
from answer_scraper import ProvisionalKeyScraper
from answer_scraper import FinalKeyScraper
from checker import Checker

sub = "maths"

s = ResponseScraper(scraper='mains_2021')
with open("files/Subjectwise/"+sub+".txt") as f:
    s.parse(f, parse_candidate_details=False, parse_test_details=False)
with open("files/Subjectwise/"+sub+".json", 'w') as f:
    s.dump_to(f)
    f.close()

'''
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
    cp = Checker(f)
'''
with open("files/final_answer.json") as f:
    cf = Checker(f)

with open("files/Subjectwise/"+sub+".json") as f:
    cf.check(f)
    cf.display_default()
    '''
    f.seek(0)
    print()
    print()
    cf.check(f)
    cf.display_default()
    '''
