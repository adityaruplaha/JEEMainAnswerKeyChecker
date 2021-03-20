import json

class Checker:
    def __init__(self, answer_key_file):
        questions = json.load(answer_key_file)["questions"]
        self.data = {}
        self.answers = {}
        for question in (questions["mcq"] + questions["numerical"]):
            self.answers[question["question_id"]] = question["answer"]

    def check(self, response_file):
        data = json.load(response_file)
        self.data = {
            "candidate" : data["candidate"],
            "test" : data["test"],
            "score" : {},
            "mismatched_questions": []
        }
        correct_mcq = 0
        correct_num = 0
        incorrect_mcq = 0
        incorrect_num = 0
        dropped_mcq = 0
        dropped_num = 0
        for question in data["questions"]["mcq"]:
            id = question["question_id"]
            if self.answers[id] is None:
                dropped_mcq += 1
                continue
            if (question["chosen"] is not None):
                if question["option_" + str(question["chosen"])] == self.answers[id]:
                    correct_mcq += 1
                else:
                    self.data["mismatched_questions"].append(
                        {
                            "question_id": id,
                            "candidate_answer": question["option_" + str(question["chosen"])],
                            "correct_answer": self.answers[id]
                        }
                    )
                    incorrect_mcq += 1
        for question in data["questions"]["numerical"]:
            id = question["question_id"]
            if self.answers[id] is None:
                dropped_num += 1
                continue
            if (question["given"] is not None):
                if question["given"] == self.answers[id]:
                    correct_num += 1
                else:
                    self.data["mismatched_questions"].append(
                        {
                            "question_id": id,
                            "candidate_answer": question["given"],
                            "correct_answer": self.answers[id]
                        }
                    )
                    incorrect_num += 1

        # Marking scheme hardcoded here.
        total = 4*(correct_mcq + correct_num + dropped_mcq + dropped_num) - incorrect_mcq
        fm = 300

        self.data["score"] = {
            "mcq" : {
                "correct" : correct_mcq,
                "incorrect" : incorrect_mcq,
                "dropped" : dropped_mcq
            },
            "numerical" : {
                "correct" : correct_num,
                "incorrect" : incorrect_num,
                "dropped" : dropped_num
            },
            "total" : total,
            "fm": fm 
        }

        return self.data

    def display_default(self,
        display_candidate_details=False,
        display_test_details=False,
        display_question_mismatches=True):

        if display_candidate_details:
            print(self.data["candidate"])
        if display_test_details:
            print(self.data["test"])
        total = self.data["score"]["total"]
        fm = self.data["score"]["fm"]
        print(f"Correct   (MCQ) : {self.data['score']['mcq']['correct']:3d}")
        print(f"Incorrect (MCQ) : {self.data['score']['mcq']['incorrect']:3d}")
        print(f"Dropped   (MCQ) : {self.data['score']['mcq']['dropped']:3d}")
        print(f"Correct   (NUM) : {self.data['score']['numerical']['correct']:3d}")
        print(f"Incorrect (NUM) : {self.data['score']['numerical']['incorrect']:3d}")
        print(f"Dropped   (NUM) : {self.data['score']['numerical']['dropped']:3d}")
        print(f"Got: {total}/{fm} ({round((total/fm)*100, 2)}%)")
        if display_question_mismatches:
            print("--------------------------")
            for q in self.data["mismatched_questions"]:
                print(f"Incorrect Question: {q['question_id']}")

    def dump_to(self, file):
            json.dump(self.data, file)