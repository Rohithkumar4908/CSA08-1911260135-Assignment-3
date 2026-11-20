"""Q1 - Lists and slicing: daily rainfall records."""
import random
import time


def weekly_totals(readings):
    """Totals of consecutive 7-day slices (the last slice can be short)."""
    return [sum(readings[i:i + 7]) for i in range(0, len(readings), 7)]


def wettest_driest(totals):
    wet = max(range(len(totals)), key=lambda i: totals[i])
    dry = min(range(len(totals)), key=lambda i: totals[i])
    return wet + 1, dry + 1  # 1-based week numbers


def moving_average_naive(readings, k=7):
    """Every window summed from scratch: about k additions per window."""
    return [sum(readings[i:i + k]) / k for i in range(len(readings) - k + 1)]


def moving_average_running(readings, k=7):
    """Running sum: subtract the day that leaves, add the day that enters."""
    if len(readings) < k:
        return []
    run = sum(readings[:k])
    out = [run / k]
    for i in range(k, len(readings)):
        run += readings[i] - readings[i - k]
        out.append(run / k)
    return out


def dry_days(readings):
    return [day for day, rain in enumerate(readings, start=1) if rain == 0]


# ---- one year of readings -----------------------------------------------
random.seed(42)
year = [random.randint(0, 40) for _ in range(365)]

totals = weekly_totals(year)
wet, dry = wettest_driest(totals)
print(f"days={len(year)}  weekly totals={len(totals)} (last week has {len(year) - 52 * 7} day)")
print(f"week 1 total: {totals[0]} mm   week 52 total: {totals[51]} mm")
print(f"wettest week: week {wet} ({totals[wet - 1]} mm)   driest week: week {dry} ({totals[dry - 1]} mm)")

ma = moving_average_running(year)
print(f"7-day moving average, first 3 days: {[round(x, 1) for x in ma[:3]]}")
dd = dry_days(year)
print(f"dry days (0 mm): {len(dd)} days, first five: {dd[:5]}")

# ---- slicing questions ----------------------------------------------------
print("readings[7:14] ->", year[7:14], " (week 2, 7 values)")
print("readings[-7:]  ->", year[-7:], " (last 7 days of the year)")
print("readings[::7]  ->", year[::7][:8], "... (every 7th day, 53 values)")

# ---- experimental investigation -------------------------------------------
print("\nn        naive(s)  running(s)   ratio")
for n in (365, 36500, 365000):
    data = [random.randint(0, 40) for _ in range(n)]
    t0 = time.perf_counter(); moving_average_naive(data); t1 = time.perf_counter()
    moving_average_running(data); t2 = time.perf_counter()
    print(f"{n:<8} {t1 - t0:>8.4f}  {t2 - t1:>10.4f}   {(t1 - t0) / (t2 - t1):5.1f}x")

print("empty list        ->", moving_average_running([], 7), moving_average_naive([], 7))
print("5 values (< 7)    ->", moving_average_running([3, 0, 5, 1, 2], 7), moving_average_naive([3, 0, 5, 1, 2], 7))
