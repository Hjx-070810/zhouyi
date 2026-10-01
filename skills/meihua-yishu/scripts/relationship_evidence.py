"""Prepare cited relationship evidence, not an automatic psychological verdict."""
import argparse
import json
from cast import ROOT, cast_numbers, relation, GENERATES, CONTROLS

MARRIAGE = {
    "用生体": "婚易成，或因婚有得",
    "体生用": "婚难成，或因婚有失",
    "体克用": "可成但成迟",
    "用克体": "不可成，成亦有害",
    "比和": "婚姻吉利",
}
SEASONS = {"spring": "木", "summer": "火", "autumn": "金", "winter": "水", "earth": "土"}

def state(element, dominant):
    if element == dominant:
        return "旺"
    if GENERATES[dominant] == element:
        return "相"
    if GENERATES[element] == dominant:
        return "休"
    if CONTROLS[element] == dominant:
        return "囚"
    return "死"

def prepare(a, b, c, season=None):
    r = cast_numbers(a, b, c)
    classics = json.loads((ROOT / "references/zhouyi-classics.json").read_text(encoding="utf-8"))
    entry = next(x for x in classics if x["sequence"] == r["main"]["sequence"])
    original = json.loads((ROOT / "references/domain-originals.json").read_text(encoding="utf-8"))
    positions = [("本用", r["yong"]), ("下互", r["mutual"]["lower"]),
                 ("上互", r["mutual"]["upper"]), ("变用", r["changed_yong"])]
    phases = [{"position": pos, "trigram": t["name"], "element": t["element"],
               "relation_to_original_ti": relation(r["ti"]["element"], t["element"]),
               "marriage_rule": MARRIAGE[relation(r["ti"]["element"], t["element"])]}
              for pos, t in positions]
    chains = []
    for pos, t in positions:
        for other_pos, other in positions:
            if pos == other_pos:
                continue
            if GENERATES[t["element"]] == other["element"]:
                chains.append(f"{pos}{t['name']}{t['element']}生{other_pos}{other['name']}{other['element']}")
            elif CONTROLS[t["element"]] == other["element"]:
                chains.append(f"{pos}{t['name']}{t['element']}克{other_pos}{other['name']}{other['element']}")
    evidence = {"casting": r, "subject_mapping": "体=求测者，用=所问关系这一侧；不确认他人内心",
                "phases": phases, "interactions": chains,
                "judgment": entry["judgment"],
                "moving_line_text": next(x for x in entry["moving_lines"] if x["position"] == r["moving_line"]),
                "classics_source": entry["source"],
                "domain_source": original["source"],
                "domain_original": next(x["text"] for x in original["sections"] if x["id"] == "5"),
                "season": None}
    if season:
        if season not in SEASONS:
            raise ValueError("Unknown explicit season")
        dominant = SEASONS[season]
        evidence["season"] = {"convention": "explicit-seasonal-five-element",
                              "dominant": dominant, "ti": state(r["ti"]["element"], dominant),
                              "phases": {pos: state(t["element"], dominant) for pos, t in positions}}
    return evidence

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("numbers", nargs=3, type=int)
    p.add_argument("--season", choices=list(SEASONS))
    args = p.parse_args()
    try:
        print(json.dumps(prepare(*args.numbers, season=args.season), ensure_ascii=False, indent=2))
    except ValueError as error:
        p.error(str(error))
