# JEEMainAnswerKeyChecker

An automated script to scrape and check JEE Main 2021 answer keys I made over the weekend. Runs fully offline.\
This is still very crude and can be improved and extended upon in many ways. Contributions welcome. :)

This software is not affiliated to or endorsed by [NTA](https://www.nta.ac.in). 

## Why?

JEE Main answer keys are given in a format which is extremely difficult and tedious to check by hand (Ctrl+F helps somewhat but its still hard). So I decided to automate this process.

This code correlates everything for you and emits the score with some barebones statistics. It can also be extended to list all mismatches for a person to check. Should be trivial though, might add it later.
## Usage

To use this project, you need some basic Python and [Okular](https://okular.kde.org/) (might work if other PDF readers have the same functionality, but untested).

I might add a CLI later.

1. Open your PDF (recorded response, final answer key PDF, or a Ctrl+P of the provisional answer key page) using Okular.
2. Export the PDF as text (File > Export As > Plain Text/Text File).
3. Use the file as demonstrated in main.py.

```python
# Scraper
s = Scraper() # choose what you need
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