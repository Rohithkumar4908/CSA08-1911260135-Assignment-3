"""Q6 - Nested data: a railway timetable enquiry."""
import random
import sys
import time

# train number -> {name, stops: [(station, arrival, departure), ...], days: set}
timetable = {
    "12621": {"name": "Tamil Nadu Exp",
              "stops": [("Chennai Central", "-", "22:00"), ("Katpadi Jn", "23:55", "23:58"),
                        ("Jolarpettai", "01:43", "01:45"), ("Salem Jn", "03:07", "03:10")],
              "days": {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"}},
    "12675": {"name": "Kovai Express",
              "stops": [("Chennai Central", "-", "06:10"), ("Katpadi Jn", "08:03", "08:05"),
                        ("Salem Jn", "10:47", "10:50"), ("Coimbatore", "14:05", "-")],
              "days": {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"}},
    "12677": {"name": "Ernakulam Exp",
              "stops": [("Chennai Central", "-", "06:35"), ("Salem Jn", "11:10", "11:12"),
                        ("Coimbatore", "14:20", "14:22"), ("Ernakulam", "17:55", "-")],
              "days": {"Mon", "Wed", "Fri"}},
    "16127": {"name": "Chennai Egmore - Guruvayur",
              "stops": [("Chennai Egmore", "-", "09:00"), ("Villupuram", "11:20", "11:25"),
                        ("Salem Jn", "14:40", "14:45"), ("Coimbatore", "18:10", "18:12")],
              "days": {"Tue", "Thu", "Sat"}},
    "22671": {"name": "Tejas Express",
              "stops": [("Chennai Egmore", "-", "06:00"), ("Villupuram", "07:38", "07:40"),
                        ("Madurai Jn", "12:20", "-")],
              "days": {"Mon", "Tue", "Thu", "Sat"}},
}


def trains_at(tt, station, day):
    """All (train, departure) stopping at station on day, sorted by departure."""
    found = []
    for number, info in tt.items():
        if day not in info["days"]:
            continue
        for st, arr, dep in info["stops"]:
            if st == station and dep != "-":
                found.append((number, info["name"], dep))
    return sorted(found, key=lambda row: row[2])


print("Trains at Salem Jn on Monday:")
for number, name, dep in trains_at(timetable, "Salem Jn", "Mon"):
    print(f"  {number}  {name:28} dep {dep}")
print("departure of 12621's 3rd stop:", timetable["12621"]["stops"][2][2])


def build_index(tt):
    """station -> sorted list of (train, day-independent departure)."""
    index = {}
    for number, info in tt.items():
        for st, arr, dep in info["stops"]:
            index.setdefault(st, []).append((number, dep))
    return index


def query_no_index(tt, station):
    return [(num, dep) for num, info in tt.items()
            for st, arr, dep in info["stops"] if st == station]


# ---- generated timetables: 100, 1,000, 10,000 trains --------------------------------
random.seed(5)
STATIONS = [f"Station{i:03d}" for i in range(200)]


def make_tt(n_trains):
    tt = {}
    for t in range(n_trains):
        stops = random.sample(STATIONS, 12)
        tt[f"T{t:05d}"] = {"name": f"Exp {t}", "stops": [(s, "10:00", "10:02") for s in stops],
                           "days": {"Mon"}}
    return tt


print("\ntrains   no-index(s)   with-index(s)")
for size in (100, 1000, 10000):
    tt = make_tt(size)
    idx = build_index(tt)
    t0 = time.perf_counter()
    for _ in range(20):
        query_no_index(tt, "Station007")
    t1 = time.perf_counter()
    for _ in range(20):
        idx.get("Station007", [])
    t2 = time.perf_counter()
    print(f"{size:>6}   {t1 - t0:>10.5f}   {t2 - t1:>11.7f}")


def deep_size(obj, seen=None):
    seen = seen or set()
    if id(obj) in seen:
        return 0
    seen.add(id(obj))
    size = sys.getsizeof(obj)
    if isinstance(obj, dict):
        size += sum(deep_size(k, seen) + deep_size(v, seen) for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set)):
        size += sum(deep_size(x, seen) for x in obj)
    return size


tt = make_tt(1000)
idx = build_index(tt)
print(f"\n1,000 trains: timetable {deep_size(tt):,} bytes, station index {deep_size(idx):,} bytes extra")
print("unknown station:", trains_at(timetable, "Timbuktu", "Mon"))
print("right station, wrong day:", trains_at(timetable, "Madurai Jn", "Wed"))
