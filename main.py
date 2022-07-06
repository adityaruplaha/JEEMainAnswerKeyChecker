from response_scraper import ResponseScraper
from answer_scraper import ProvisionalKeyScraper
from answer_scraper import FinalKeyScraper
from checker import Checker

folder = "files_2022/files_jun"
current_scraper = 'mains_2022'

s = ResponseScraper(scraper=current_scraper)
with open(f"{folder}/Recorded Response.txt") as f:
    s.parse(f)
with open(f"{folder}/response.json", 'w') as f:
    s.dump_to(f)
    f.close()

### ''' 
s = ProvisionalKeyScraper(scraper=current_scraper)
with open(f"{folder}/Provisional Answer Key.txt") as f:
    s.parse(f)
with open(f"{folder}/provisional_answer.json", 'w') as f:
    s.dump_to(f)
    f.close()

'''
s = FinalKeyScraper(scraper=current_scraper)
with open(f"{folder}/Final Answer Key.txt") as f:
    s.parse(f)
with open(f"{folder}/final_answer.json", 'w') as f:
    s.dump_to(f)
    f.close()
'''


with open(f"{folder}/provisional_answer.json") as f:
    c = Checker(f)
'''
with open(f"{folder}/final_answer.json") as f:
    c = Checker(f)
''' ###

with open(f"{folder}/response.json") as f:
    c.check(f)
    c.display_default()
