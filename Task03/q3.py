"""Q3 - Dictionaries: farmer helpline complaint analysis."""
import random
import re
import time
from collections import Counter

calls = [
    "seeds not received seeds delayed",
    "fertiliser price high",
    "seeds price high subsidy not received",
]
STOP = {"not", "high"}


def frequencies(texts, stop):
    # TODO 1: dictionary word -> count for every word not in stop, using dict.get()
    counts = {}
    for text in texts:
        for word in text.split():
            if word not in stop:
                counts[word] = counts.get(word, 0) + 1
    return counts


def top(counts, k):
    # TODO 2: k most frequent (word, count) pairs, highest first, alphabetical ties
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:k]


print(top(frequencies(calls, STOP), 3))


def frequencies_setdefault(texts, stop):
    """The same count with setdefault() instead of get()."""
    counts = {}
    for text in texts:
        for word in text.split():
            if word not in stop:
                counts.setdefault(word, 0)
                counts[word] += 1
    return counts


def group_by_district(rows):
    """(district, crop, text) rows -> district -> list of complaints."""
    by_district = {}
    for district, crop, text in rows:
        by_district.setdefault(district, []).append(text)
    return by_district


print("setdefault() agrees:", frequencies_setdefault(calls, STOP) == frequencies(calls, STOP))

# ---- experimental investigation ----------------------------------------------
WORDS = ["seeds", "price", "subsidy", "water", "pest", "loan", "crop", "rain",
         "fertiliser", "delay", "damage", "market", "soil", "pump", "insurance"]
random.seed(7)


def make_complaints(m):
    return [" ".join(random.choice(WORDS) for _ in range(8)) for _ in range(m)]


def count_dict(words):
    c = {}
    for w in words:
        c[w] = c.get(w, 0) + 1
    return c


def count_list(words):
    distinct = list(set(words))
    return {w: words.count(w) for w in distinct}


print("\ncomplaints  dict(s)   list.count(s)  Counter(s)")
for m in (1000, 10000, 100000):
    words = " ".join(make_complaints(m)).split()
    t0 = time.perf_counter(); count_dict(words); t1 = time.perf_counter()
    count_list(words); t2 = time.perf_counter()
    Counter(words); t3 = time.perf_counter()
    print(f"{m:>9}   {t1 - t0:.4f}    {t2 - t1:>8.4f}     {t3 - t2:.4f}")

# ---- robustness: empty text, case, punctuation ----------------------------------
messy = ["SEEDS, seeds! SEEDS?", "", "price... price"]
cleaned = [re.sub(r"[^a-z ]", "", t.lower()) for t in messy]
print("messy input ->", frequencies(cleaned, set()))
print("empty text  ->", frequencies([], STOP))
