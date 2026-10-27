"""Session 4 - A tiny, explainable phishing classifier (Naive Bayes from scratch).

Email security gateways use machine learning to decide whether a message is phishing.
This script trains a very small Naive Bayes model on 16 fictional, harmless emails,
tests it on 6 unseen ones, and then applies an EMAIL POLICY:

  probability >= 0.90  -> QUARANTINE (user never sees it, admin can release)
  0.50 to 0.90         -> DELIVER WITH WARNING BANNER
  below 0.50           -> DELIVER

It also prints the words that pushed each decision, because a policy that cannot be
explained cannot be audited. No real brands, links or payloads are used.
Run:  python session-04_phishing_classifier.py
"""
import math
import re
from collections import Counter

TRAIN = [  # (label, text)  1 = phishing, 0 = legitimate
    (1, "urgent verify your account password now or it will be suspended"),
    (1, "your mailbox is full click here to verify login immediately"),
    (1, "congratulations you won a prize claim your reward by entering bank details"),
    (1, "security alert unusual sign in confirm your password at this link"),
    (1, "invoice overdue pay now using the attached link to avoid penalty"),
    (1, "hr update confirm your salary account details today urgent"),
    (1, "your parcel is held pay a small fee click the link now"),
    (1, "final warning account locked verify identity within 24 hours"),
    (0, "reminder the data structures lab moves to room 204 on monday"),
    (0, "please find the agenda for the faculty meeting on thursday"),
    (0, "the library will close early on friday for maintenance"),
    (0, "assignment two marks are uploaded to the course portal"),
    (0, "thank you for attending the workshop slides are attached"),
    (0, "the exam timetable for the midterm week has been published"),
    (0, "lunch for the department seminar will be served at one"),
    (0, "please review the draft syllabus and send comments by friday"),
]
TEST = [
    (1, "urgent your password expires today click here to verify"),
    (1, "claim your bonus reward enter your bank account details"),
    (0, "the programming lab quiz is on wednesday in room 204"),
    (0, "seminar slides and agenda are attached for review"),
    (1, "account suspended confirm login details at the link"),
    (0, "please verify the attendance sheet before friday"),  # tricky: has "verify"
]
STOP = {"the", "a", "to", "your", "is", "on", "for", "at", "by", "or", "it", "in", "and", "of", "be", "will", "has", "been", "are", "this", "using", "now"}


def words(text):
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP]


class NaiveBayes:
    def fit(self, data):
        self.counts = {0: Counter(), 1: Counter()}
        self.docs = Counter(label for label, _ in data)
        for label, text in data:
            self.counts[label].update(words(text))
        self.vocab = set(self.counts[0]) | set(self.counts[1])
        self.total = {c: sum(self.counts[c].values()) for c in (0, 1)}
        return self

    def word_logratio(self, w):  # > 0 means the word points to phishing
        p = [(self.counts[c][w] + 1) / (self.total[c] + len(self.vocab)) for c in (0, 1)]
        return math.log(p[1] / p[0])

    def predict_proba(self, text):
        log_odds = math.log(self.docs[1] / self.docs[0])
        log_odds += sum(self.word_logratio(w) for w in words(text) if w in self.vocab)
        return 1 / (1 + math.exp(-log_odds))


def policy(p):
    return "QUARANTINE" if p >= 0.90 else "WARN BANNER" if p >= 0.50 else "DELIVER"


model = NaiveBayes().fit(TRAIN)
print(f"[1] Trained on {len(TRAIN)} emails, vocabulary {len(model.vocab)} words")
top = sorted(model.vocab, key=lambda w: (-model.word_logratio(w), w))[:6]
print("    strongest phishing words:", ", ".join(top))

print("\n[2] Test emails -> probability -> policy action")
tp = fp = tn = fn = 0
for label, text in TEST:
    p = model.predict_proba(text)
    pred = 1 if p >= 0.50 else 0
    tp += pred == 1 and label == 1; fp += pred == 1 and label == 0
    tn += pred == 0 and label == 0; fn += pred == 0 and label == 1
    clues = sorted({w for w in words(text) if w in model.vocab},
                   key=lambda w: (-model.word_logratio(w), w))[:2]
    mark = "ok " if pred == label else "ERR"
    print(f"  {mark} p={p:.2f} {policy(p):<11} | {text[:46]:<46} | clues: {', '.join(clues)}")

acc = (tp + tn) / len(TEST)
prec = tp / (tp + fp) if tp + fp else 0
rec = tp / (tp + fn) if tp + fn else 0
print(f"\n[3] Confusion: TP={tp} FP={fp} TN={tn} FN={fn}")
print(f"    accuracy {acc:.2f} | precision {prec:.2f} | recall {rec:.2f}")
print("    A false positive delays real mail; a false negative lets phishing in.")
print("    Policy owners choose thresholds knowing which mistake costs more.")
