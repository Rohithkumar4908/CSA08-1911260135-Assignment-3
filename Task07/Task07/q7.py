"""Q7 - Design from first principles: merging phone contacts."""
import random
import re
import time


def normalise_number(raw):
    """'+91 98400 12345' -> '9840012345'; keep the last 10 digits."""
    digits = re.sub(r"\D", "", raw or "")
    return digits[-10:] if len(digits) >= 10 else digits


def normalise_name(raw):
    """'Dr.  Ravi KUMAR ' -> 'ravi kumar' (titles and extra spaces removed)."""
    name = (raw or "").lower()
    name = re.sub(r"\b(dr|mr|mrs|ms)\.?\b", " ", name)
    return " ".join(name.split())


def merge_contacts(sources):
    """Merge contact lists into one record per person.

    Rule: contacts sharing a normalised phone number are the same person.
    A contact with no number merges into a same-named group (SIM name-only card).
    Two people who only share a name stay separate.
    """
    by_number = {}          # normalised number -> person record
    name_only = {}          # normalised name -> person record (no number yet)
    for source in sources:
        for raw_name, raw_number, email in source:
            name = normalise_name(raw_name)
            number = normalise_number(raw_number)
            if number:
                person = by_number.setdefault(number, {"names": set(), "numbers": set(), "emails": set()})
            else:
                person = name_only.setdefault(name, {"names": set(), "numbers": set(), "emails": set()})
            if name:
                person["names"].add(name)
            if number:
                person["numbers"].add(number)
            if email:
                person["emails"].add(email.strip().lower())
    people = list(by_number.values())
    for name, orphan in name_only.items():
        match = next((p for p in people if name in p["names"]), None)
        if match:
            match["emails"] |= orphan["emails"]
        else:
            people.append(orphan)
    return people


phone_a = [("Dr. Ravi", "+91 98400 12345", "ravi@gmail.com"),
           ("Meena S", "044-2345 6789", "meena@yahoo.com")]
phone_b = [("ravi kumar", "9840012345", "ravi.kumar@work.com"),
           ("Ravi Kumar", "9000011111", "other.ravi@gmail.com")]  # a DIFFERENT Ravi
sim = [("Ravi Kumar", "", "ravi-sim@mail.com"), ("Meena", "", "")]

people = merge_contacts([phone_a, phone_b, sim])
print(f"{sum(len(s) for s in (phone_a, phone_b, sim))} contacts -> {len(people)} people")
for p in people:
    print(" ", sorted(p["names"]), sorted(p["numbers"]), sorted(p["emails"]))

# missing fields and odd formats must not crash
edge = [("", "91 90000 22222", ""), ("No Number", "", ""), ("X", "123", "")]
print("edge cases ->", len(merge_contacts([edge])), "people, no crash")

# ---- verification on a hand-merged small list ---------------------------------------
by_hand = 3  # phone_a's Ravi + SIM Ravi merge; Meena x2 entries are one; other Ravi separate
print("hand-verified count matches:", len(people) == by_hand)

# no number appears under two people (requirement R1)
all_numbers = [n for p in people for n in p["numbers"]]
print("no number shared by two people:", len(all_numbers) == len(set(all_numbers)))

# ---- measurements: dictionary merge vs comparing every pair -----------------------------
random.seed(9)
FIRST = ["ravi", "meena", "arun", "divya", "karthik", "priya", "suresh", "anita"]


def make_contacts(n):
    return [[(f"{random.choice(FIRST)} {i}", f"9{i:09d}", f"user{i}@mail.com")
             for i in range(n)]]


def merge_pairs(source):
    people = []
    for name, number, email in source[0]:
        number = normalise_number(number)
        found = None
        for p in people:
            if number in p["numbers"]:
                found = p
                break
        if not found:
            found = {"names": set(), "numbers": set(), "emails": set()}
            people.append(found)
        found["numbers"].add(number)
        found["names"].add(normalise_name(name))
    return people


print("\ncontacts   dictionary(s)   pairwise(s)")
for n in (1000, 2000, 4000):
    src = make_contacts(n)
    t0 = time.perf_counter(); merge_contacts(src); t1 = time.perf_counter()
    merge_pairs(src); t2 = time.perf_counter()
    print(f"{n:>8}   {t1 - t0:>11.4f}   {t2 - t1:>10.4f}")

src = make_contacts(100000)
t0 = time.perf_counter()
people100k = merge_contacts(src)
t1 = time.perf_counter()
print(f"{100000:>8}   {t1 - t0:>11.4f}   (pairwise: skipped, ~O(n^2))")
print("all 100,000 numbers preserved:", sum(len(p['numbers']) for p in people100k) == 100000)
