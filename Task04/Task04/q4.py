"""Q4 - Sets: elective registration clash detection."""
import random
import time

ai_elective = {"192311001", "192311004", "192311007", "192311009"}
iot_elective = {"192311002", "192311004", "192311009", "192311010"}
all_students = {f"1923110{i:02d}" for i in range(1, 11)}

# TODO 1: set operators -> both electives, exactly one, neither
both = ai_elective & iot_elective
exactly_one = ai_elective ^ iot_elective
neither = all_students - (ai_elective | iot_elective)

print("clash :", sorted(both))
print("exactly one:", sorted(exactly_one))
print("neither :", sorted(neither))

# TODO 1 rewritten with set methods - same results
both_m = ai_elective.intersection(iot_elective)
one_m = ai_elective.symmetric_difference(iot_elective)
none_m = all_students.difference(ai_elective.union(iot_elective))
print("methods agree:", both_m == both and one_m == exactly_one and none_m == neither)

# duplicates are removed automatically
raw = ["192311001", "192311004", "192311001", "192311007", "192311004"]
print("duplicates in:", len(raw), "registrations -> set keeps", len(set(raw)))

# ---- membership test: list vs set ----------------------------------------------
print("\nsize        in list(s)   in set(s)")
for n in (10_000, 100_000, 1_000_000):
    nums = [f"R{i:07d}" for i in range(n)]
    lst = list(nums)
    st = set(nums)
    probes = [f"R{n - 1:07d}", "NOT_HERE"] * 50
    t0 = time.perf_counter()
    for p in probes:
        p in lst
    t1 = time.perf_counter()
    for p in probes:
        p in st
    t2 = time.perf_counter()
    print(f"{n:>9,}   {t1 - t0:>9.4f}   {t2 - t1:>8.6f}")

# ---- nested loops vs set intersection -------------------------------------------
random.seed(3)
A = {f"R{random.randrange(60000):05d}" for _ in range(5000)}
B = {f"R{random.randrange(60000):05d}" for _ in range(5000)}
la, lb = list(A), list(B)
t0 = time.perf_counter()
common = [a for a in la if a in lb]
t1 = time.perf_counter()
common2 = A & B
t2 = time.perf_counter()
print(f"\n5,000 x 5,000: nested loops {t1 - t0:.3f}s, & operator {t2 - t1:.6f}s, agree: {set(common) == common2}")

# ---- edge cases -------------------------------------------------------------------
empty = set()
print("empty elective :", sorted(A & empty), A ^ empty == A)
print("identical electives:", A & A == A, sorted(A ^ A), "<- no clash, nobody in exactly-one")

# hand-verified small case
x, y = {"s1", "s2", "s3"}, {"s3", "s4"}
print("hand case:", x & y == {"s3"}, x ^ y == {"s1", "s2", "s4"})
