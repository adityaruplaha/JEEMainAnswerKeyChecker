import json

class Checker:
    def __init__(self, answer_key_file):
        questions = json.load(answer_key_file)["questions"]
        self.answers = {}
        for question in (questions["mcq"] + questions["numerical"]):
            self.answers[question["question_id"]] = question["answer"]

    def check(self, response_file):
        data = json.load(response_file)
        self.data = {
            "candidate" : data["candidate"],
            "test" : data["test"]
        }
        correct_mcq = 0
        correct_num = 0
        incorrect_mcq = 0
        incorrect_num = 0
        dropped_mcq = 0
        dropped_num = 0
        for question in data["questions"]["mcq"]:
            id = question["question_id"]
            if self.answers[id] == 'D':
                dropped_mcq += 1
                continue
            if (question["chosen"] is not None) and (self.answers[id] is not None):
                if question["option_" + str(question["chosen"])] == self.answers[id]:
                    correct_mcq += 1
                else:
                    incorrect_mcq += 1
        for question in data["questions"]["numerical"]:
            id = question["question_id"]
            if self.answers[id] == 'D':
                dropped_num += 1
                continue
            if (question["given"] is not None) and (self.answers[id] is not None):
                if question["given"] == self.answers[id]:
                    correct_num += 1
                else:
                    incorrect_num += 1

        total = 4*(correct_mcq + correct_num + dropped_mcq + dropped_num) - incorrect_mcq

        print(data["candidate"])
        print(data["test"])
        print(f"Correct   (MCQ) : {correct_mcq:3d}")
        print(f"Incorrect (MCQ) : {incorrect_mcq:3d}")
        print(f"Dropped   (NUM) : {dropped_mcq:3d}")
        print(f"Correct   (NUM) : {correct_num:3d}")
        print(f"Incorrect (NUM) : {incorrect_num:3d}")
        print(f"Dropped   (NUM) : {dropped_num:3d}")
        print(f"Got: {total}/300")