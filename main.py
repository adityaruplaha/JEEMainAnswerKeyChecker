from response_scraper import ResponseScraper
from answer_scraper import ProvisionalKeyScraper
from answer_scraper import FinalKeyScraper
from checker import Checker

s = ResponseScraper()
f = open("files/Recorded Response.txt")
s.parse(f)
f.close()
f = open("files/response.json", 'w')
s.dump(f)
f.close()

s = ProvisionalKeyScraper()
f = open("files/Provisional Answer Key.txt")
s.parse(f)
f.close()
f = open("files/provisional_answer.json", 'w')
s.dump(f)
f.close()

s = FinalKeyScraper()
f = open("files/Final Answer Key.txt")
s.parse(f)
f.close()
f = open("files/final_answer.json", 'w')
s.dump(f)
f.close()

f = open("files/provisional_answer.json")
cp = Checker(f)
f.close()
f = open("files/final_answer.json")
cf = Checker(f)
f.close()
f = open("files/response.json")
cp.check(f)
f.seek(0)
cf.check(f)
f.close()