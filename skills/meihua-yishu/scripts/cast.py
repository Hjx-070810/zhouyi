"""Deterministic Meihua casting. Python 3.10+, standard library only."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRIGRAMS = {
    1: ("乾", "金", [1, 1, 1]), 2: ("兑", "金", [1, 1, 0]),
    3: ("离", "火", [1, 0, 1]), 4: ("震", "木", [1, 0, 0]),
    5: ("巽", "木", [0, 1, 1]), 6: ("坎", "水", [0, 1, 0]),
    7: ("艮", "土", [0, 0, 1]), 8: ("坤", "土", [0, 0, 0]),
}
GENERATES = dict(zip("木火土金水", "火土金水木"))
CONTROLS = dict(zip("木土水火金", "土水火金木"))
HEXAGRAMS = json.loads((ROOT / "references/hexagrams.json").read_text(encoding="utf-8"))
LOOKUP = {(h["upper"], h["lower"]): h for h in HEXAGRAMS}

def valid(value, low, high=None):
    if isinstance(value, bool) or not isinstance(value, int) or value < low or (high is not None and value > high):
        raise ValueError(f"Expected integer {low}..{high or 'infinity'}, got {value!r}")
    return value

def rem(n, modulus):
    return n % modulus or modulus

def trigram(n):
    name, element, lines = TRIGRAMS[n]
    return {"id": n, "name": name, "element": element, "lines": lines[:]}

def from_lines(lines):
    return next(n for n, (_, _, pattern) in TRIGRAMS.items() if pattern == lines)

def hexagram(upper, lower):
    entry = LOOKUP[(upper, lower)]
    return {**entry, "upper": trigram(upper), "lower": trigram(lower),
            "lines": TRIGRAMS[lower][2] + TRIGRAMS[upper][2]}

def relation(ti, yong):
    if ti == yong:
        return "比和"
    if GENERATES[yong] == ti:
        return "用生体"
    if CONTROLS[ti] == yong:
        return "体克用"
    if GENERATES[ti] == yong:
        return "体生用"
    return "用克体"

def mutual(h):
    lines = h["lines"]
    return hexagram(from_lines(lines[2:5]), from_lines(lines[1:4]))

def calculate(upper, lower, moving, mutual_rule="book"):
    valid(upper, 1, 8); valid(lower, 1, 8); valid(moving, 1, 6)
    if mutual_rule not in ("book", "website"):
        raise ValueError("Unknown mutual rule")
    main = hexagram(upper, lower)
    lines = main["lines"][:]
    lines[moving - 1] = 1 - lines[moving - 1]
    changed = hexagram(from_lines(lines[3:]), from_lines(lines[:3]))
    special = upper == lower and upper in (1, 8) and mutual_rule == "book"
    ti = main["upper"] if moving <= 3 else main["lower"]
    yong = main["lower"] if moving <= 3 else main["upper"]
    changed_yong = changed["lower"] if moving <= 3 else changed["upper"]
    inter = mutual(changed if special else main)
    return {"main": main, "mutual": inter, "changed": changed,
            "moving_line": moving, "line_order": "bottom-to-top",
            "mutual_rule": mutual_rule, "mutual_basis": "changed" if special else "main",
            "ti": ti, "yong": yong, "relation": relation(ti["element"], yong["element"]),
            "mutual_relations": {"lower": relation(ti["element"], inter["lower"]["element"]),
                                 "upper": relation(ti["element"], inter["upper"]["element"])},
            "changed_yong": changed_yong,
            "changed_relation": relation(ti["element"], changed_yong["element"])}

def cast_numbers(a, b, c, mutual_rule="book"):
    for n in (a, b, c):
        valid(n, 1)
    return {**calculate(rem(a, 8), rem(b, 8), rem(a + b + c, 6), mutual_rule),
            "method": "website-three-numbers", "inputs": [a, b, c]}

def cast_lunar(year_branch, month, day, hour_branch, mutual_rule="book", leap=False):
    valid(year_branch, 1, 12); valid(month, 1, 12); valid(day, 1, 30); valid(hour_branch, 1, 12)
    if leap:
        raise ValueError("Leap-month convention must be settled before casting; this mode does not resolve it.")
    upper_sum = year_branch + month + day
    total = upper_sum + hour_branch
    return {**calculate(rem(upper_sum, 8), rem(total, 8), rem(total, 6), mutual_rule),
            "method": "verified-lunar-time",
            "inputs": {"year_branch": year_branch, "month": month, "day": day, "hour_branch": hour_branch},
            "sums": {"upper": upper_sum, "lower_and_moving": total}}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutual-rule", choices=["book", "website"], default="book")
    sub = parser.add_subparsers(dest="mode", required=True)
    numbers = sub.add_parser("numbers")
    numbers.add_argument("values", nargs=3, type=int)
    manual = sub.add_parser("manual")
    manual.add_argument("values", nargs=3, type=int, metavar="UPPER_LOWER_MOVING")
    lunar = sub.add_parser("lunar")
    lunar.add_argument("values", nargs=4, type=int, metavar="YEAR_MONTH_DAY_HOUR")
    lunar.add_argument("--leap", action="store_true")
    args = parser.parse_args()
    try:
        if args.mode == "numbers":
            result = cast_numbers(*args.values, mutual_rule=args.mutual_rule)
        elif args.mode == "manual":
            result = calculate(*args.values, mutual_rule=args.mutual_rule)
            result["method"] = "provided-hexagram"
        else:
            result = cast_lunar(*args.values, mutual_rule=args.mutual_rule, leap=args.leap)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
