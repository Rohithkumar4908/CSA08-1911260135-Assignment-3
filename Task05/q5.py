"""Q5 - List comprehension: cleaning cold-storage sensor readings."""
import random
import sys
import time


def clean_loop(readings):
    """For loop with append: keep readings inside [-50, 50]."""
    valid = []
    for c in readings:
        if -50 <= c <= 50:
            valid.append(c)
    return valid


def clean_comp(readings):
    """The same filter as a list comprehension with a condition."""
    return [c for c in readings if -50 <= c <= 50]


def clean_mapfilter(readings):
    """The same filter with map/filter and lambda."""
    return list(map(lambda c: c, filter(lambda c: -50 <= c <= 50, readings)))


def to_fahrenheit(celsius):
    return [c * 9 / 5 + 32 for c in celsius]


def alarm_minutes(readings, lo=2, hi=8):
    """Minutes whose (valid) temperature is outside 2-8 C, via enumerate."""
    return [m for m, c in enumerate(readings) if -50 <= c <= 50 and not (lo <= c <= hi)]


# ---- demo ----------------------------------------------------------------------
random.seed(11)
log = [round(random.uniform(-60, 60), 1) for _ in range(12)]
valid = clean_comp(log)
print("raw log   :", log)
print("valid     :", valid)
print("fahrenheit:", [round(f, 1) for f in to_fahrenheit(valid)])
print("alarm minutes (outside 2-8 C):", alarm_minutes(log))

# dictionary and set comprehensions for the same problem
by_minute = {m: c for m, c in enumerate(log) if -50 <= c <= 50}
unique_temps = {round(c) for c in log if -50 <= c <= 50}
print("dict comp (minute->temp):", dict(list(by_minute.items())[:4]), "...")
print("set comp (unique temps) :", sorted(unique_temps))

# ---- three versions agree --------------------------------------------------------
print("\nloop == comprehension == map/filter:",
      clean_loop(log) == clean_comp(log) == clean_mapfilter(log))
print("all-valid input  :", clean_comp([4.0, 5.5, 7.9]))
print("all-invalid input:", clean_comp([-80.0, 99.0]))

# ---- timing ----------------------------------------------------------------------
print("\nn           loop(s)   comp(s)   map/filter(s)")
for n in (10_000, 100_000, 1_000_000):
    data = [random.uniform(-60, 60) for _ in range(n)]
    t0 = time.perf_counter(); clean_loop(data); t1 = time.perf_counter()
    clean_comp(data); t2 = time.perf_counter()
    clean_mapfilter(data); t3 = time.perf_counter()
    print(f"{n:>9,}  {t1 - t0:>7.4f}  {t2 - t1:>7.4f}   {t3 - t2:>7.4f}")

# ---- memory: list comprehension vs generator expression ----------------------------
data = [random.uniform(-60, 60) for _ in range(1_000_000)]
lc = [c for c in data if -50 <= c <= 50]
ge = (c for c in data if -50 <= c <= 50)
print(f"\n1,000,000 readings: list comp {sys.getsizeof(lc):,} bytes, generator {sys.getsizeof(ge)} bytes")
