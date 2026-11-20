"""Q2 - Tuples, mutability and copying: city bus-stop map."""
import copy
import sys
import time

rows, cols = 3, 4

bad = [[0] * cols] * rows  # every row is the SAME list object
bad[0][1] = 7

# TODO 1: Create a rows x cols grid of zeros using a list comprehension so that every
# row is a separate list
good = [[0] * cols for _ in range(rows)]
good[0][1] = 7

print("bad :", bad)
print("good:", good)
print(bad[0] is bad[1], good[0] is good[1])

# Tuples are immutable, so they can be used as dictionary keys
stops = {(13.0827, 80.2707): "Chennai Central", (13.0418, 80.2341): "T. Nagar"}
print(stops[(13.0418, 80.2341)])

# ---- the bug shown with is and id() ---------------------------------------
print("\nid of bad rows :", [id(r) for r in bad])
print("id of good rows:", [id(r) for r in good])

# ---- aliasing, shallow copy, deep copy --------------------------------------
grid = [[1, 2], [3, 4]]
alias = grid                 # same object
shallow = copy.copy(grid)    # new outer list, same inner lists
deep = copy.deepcopy(grid)   # fully independent
grid[0][0] = 99
print("\nalias  :", alias[0], " <- changed (same object)")
print("shallow:", shallow[0], " <- changed (shared inner list)")
print("deep   :", deep[0], " <- unchanged")

# ---- unpacking tuples in a loop ----------------------------------------------
for (lat, lon), name in stops.items():
    print(f"{name:16} lat={lat} lon={lon}")

# ---- list as a dictionary key --------------------------------------------------
try:
    stops[[13.0418, 80.2341]] = "T. Nagar"
except TypeError as e:
    print("\nlist as key -> TypeError:", e)

# ---- a list stored inside a tuple can still change -----------------------------
pair = ([1, 2], "zone A")
pair[0].append(3)
print("list inside tuple:", pair, " (the tuple is unchanged, its list is not)")

# ---- memory and speed: list vs tuple of 1,000,000 values -------------------------
n = 1_000_000
lst = list(range(n))
tup = tuple(range(n))
print(f"\n1,000,000 values: list {sys.getsizeof(lst):,} bytes, tuple {sys.getsizeof(tup):,} bytes")

t0 = time.perf_counter(); lst2 = [i for i in range(n)]; t1 = time.perf_counter()
tup2 = tuple(range(n)); t2 = time.perf_counter()
print(f"create: list {t1 - t0:.4f}s   tuple {t2 - t1:.4f}s")

t0 = time.perf_counter(); s = sum(lst[i] for i in range(0, n, 97)); t1 = time.perf_counter()
s = sum(tup[i] for i in range(0, n, 97)); t2 = time.perf_counter()
print(f"index : list {t1 - t0:.4f}s   tuple {t2 - t1:.4f}s")
