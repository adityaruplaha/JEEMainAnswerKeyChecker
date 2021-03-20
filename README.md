# JEEMainAnswerKeyChecker

An automated script to scrape and check JEE Main 2021 answer keys I made over the weekend. Runs fully offline.
This is still very crude and can be improved and extended upon in many ways. Contributions welcome. :)

This software is not affiliated to or endorsed by [NTA](https://www.nta.ac.in). 

## Why?

JEE Main answer keys are given in a format which is extremely difficult and tedious to check by hand (Ctrl+F helps somewhat but its still hard). So I decided to automate this process.

This code correlates everything for you and emits the score with some barebones statistics. It can also be extended to list all mismatches for a person to check. ~~Should be trivial though, might add it later.~~ Working on it.
## Usage

To use this project, you need some basic Python and [Okular](https://okular.kde.org/) (might work if other PDF readers have the same functionality, but untested).

I might add a CLI later.

1. Open your PDF (recorded response, final answer key PDF, or a Ctrl+P of the provisional answer key page) using Okular.
2. Export the PDF as text (File > Export As > Plain Text/Text File).
3. Use the file as demonstrated in main.py. A short example is shown below.

```python
# Scraper
s = Scraper(scraper='mains_2021') # choose what you need
file = open(...) # or any file-like object
s.parse(file)
out_json_file = open(..., 'w') # or any file-like object
s.dump(out_json_file)

# Checker
answer_key_json_file = open(...)
checker = Checker(answer_key_json_file)
response_json_file = open(...)
checker.check(response_json_file) # prints your score and stats

# Please note that open() doesn't create folders.
# You need to have them in your filesystem already.
```

## Scrapers

As of Beta 0.2, the project support plugin-like scrapers in the form of JSON files.
These JSON files define regexes and a null list.
These define the rules by which the program extracts and interprets the various parts of the files.

Please note, I have no inside information upon the format NTA uses, this is all by trial and error.
So, writing scrapers takes a while and they can break easily if NTA decides to change the format of their PDFs.

If you find that this broke in the future, please open an issue describing what went wrong, the intended output, and attach files so that I can write a new scraper.

Currently the following scrapers are supported:
- `mains_2021` --> for JEE Mains 2021. Tested for February, March attempt.

### Implementing New Scrapers

If you are interested in writing a scraper, you need to keep their basic structure in mind.

- Folder name should be same as scraper name.
- `null_list.json` is a list containing all strings that correspond to "no answer"/"not attempted"/"question dropped".
- `final_answer.json` is used by `FinalKeyScraper`. It contains regexes for `mcq`,`numerical` with named capture groups:
    - `qid`: question ID
    - `ans`: answer
- `provisional_answer.json` is used by `ProvisionalKeyScraper`. It behaves the same way as `final_answer.json`.
- `response.json` is used by `ResponseScraper`.

    It contains regexes for different candidate and test details with a single capture group.
    The keys are self explanatory.

    It contains regexes for `mcq` with named capture groups:
    - `qid`: question ID
    - `o1id`: option 1 ID
    - `o2id`: option 2 ID
    - `o3id`: option 3 ID
    - `o4id`: option 4 ID
    - `chosen`: chosen (1,2,3, or 4)

    It contains regexes for `numerical` with named capture groups:
    - `qid`: question ID
    - `given`: given answer (float)

Keeping this structure in mind, you need to write regexes so that the match objects are able to capture details.