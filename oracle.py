import math, json

def plural(n, one, many):
    return one if n == 1 else many

def tenths(x):
    return math.floor(x * 10 + 0.5) / 10

def fixed1(x):
    return f"{tenths(x):.1f}"

NEED = [8, 14, 20]  # labeled norm: DLI target, gentle / moderate / hungry
CROP = ["gentle", "moderate", "hungry"]

def watt_truth(claim, draw):
    if not (claim > 0):
        raise ValueError("the claimed watts must be above zero")
    if not (draw > 0):
        raise ValueError("the wall draw must be above zero")
    pct = tenths(draw / claim * 100)
    if pct < 12:
        band = "about a tenth"
    elif pct < 22:
        band = "about a fifth"
    elif pct < 38:
        band = "about a third"
    elif pct < 70:
        band = "about half"
    else:
        band = "most of the claim"
    return f"The box claims {claim} {plural(claim, 'watt', 'watts')} and the wall meter reads {draw} - {pct:.1f}% of the claim, {band} honestly."

def dli_truth(ppfd, ref_h, hang_h, hours):
    if not (ppfd > 0):
        raise ValueError("the chart PPFD must be above zero")
    if not (ref_h > 0):
        raise ValueError("the chart height must be above zero")
    if not (hang_h > 0):
        raise ValueError("the hanging height must be above zero")
    if not (hours > 0):
        raise ValueError("the daily hours must be above zero")
    if not (hours <= 24):
        raise ValueError("the daily hours must be 24 or fewer")
    at = ppfd * (ref_h / hang_h) ** 2
    dli = at * hours * 0.0036
    return f"The chart's {ppfd} µmol at {ref_h} {plural(ref_h, 'inch', 'inches')} hangs at {hang_h} {plural(hang_h, 'inch', 'inches')} as {fixed1(at)} µmol; {hours} {plural(hours, 'hour', 'hours')} a day grows a DLI of {fixed1(dli)} honestly."

def need_truth(dli, level):
    if not (dli > 0):
        raise ValueError("the delivered DLI must be above zero")
    need = NEED[level]
    dm = tenths(dli - need)
    if dm > 0:
        verdict = f"a margin of {fixed1(dm)} honestly"
    elif dm < 0:
        verdict = f"{fixed1(-dm)} short honestly"
    else:
        verdict = "exactly matched honestly"
    return f"A {CROP[level]} crop asks for a DLI of {fixed1(need)}; the lamp delivers {fixed1(dli)} - {verdict}."

FNS = {"wattTruth": watt_truth, "dliTruth": dli_truth, "needTruth": need_truth}

CASES = [
    ("wattTruth", [1000, 100]),
    ("wattTruth", [600, 150]),
    ("wattTruth", [100, 95]),
    ("wattTruth", [800, 160]),
    ("wattTruth", [400, 180]),
    ("wattTruth", [1, 1]),
    ("wattTruth", [0, 100]),
    ("wattTruth", [1000, 0]),
    ("wattTruth", [1000, -5]),
    ("dliTruth", [800, 12, 24, 16]),
    ("dliTruth", [600, 18, 12, 12]),
    ("dliTruth", [800, 12, 12, 16]),
    ("dliTruth", [500, 12, 30, 10]),
    ("dliTruth", [900, 6, 18, 18]),
    ("dliTruth", [1000, 24, 24, 1]),
    ("dliTruth", [0, 12, 24, 16]),
    ("dliTruth", [800, 0, 24, 16]),
    ("dliTruth", [800, 12, 0, 16]),
    ("dliTruth", [800, 12, 24, 0]),
    ("dliTruth", [800, 12, 24, 25]),
    ("needTruth", [11.5, 1]),
    ("needTruth", [46.1, 2]),
    ("needTruth", [11.5, 0]),
    ("needTruth", [8.0, 0]),
    ("needTruth", [7.9, 0]),
    ("needTruth", [20.04, 2]),
    ("needTruth", [0, 1]),
    ("needTruth", [-3, 2]),
]

out = []
for fn, args in CASES:
    rec = {"fn": fn, "args": args}
    try:
        rec["out"] = FNS[fn](*args)
    except ValueError as e:
        rec["err"] = str(e)
    out.append(rec)
    print(fn, args, "->", rec.get("out") or ("ERR: " + rec["err"]))

with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(f"{len(out)} cases written to expected.json")
