#!/usr/bin/env python3
"""Random-afternoon publish gate for bottledmarbles.ipe.rest — stdlib only (Python 3.9+).

launchd calls this every 15 minutes between 12:00 and 18:45 KST. It publishes at most one journal post a day, at a random
time between 12:00 and 17:59 that never shares its hour with the previous day's time (Davy 2026-11-13: one post a day, random
afternoon, not the same time of day as yesterday).

State file (default ~/.ipe/queue/bottledmarbles/slot.json, same shape in every game room):
  {"date": "YYYY-MM-DD", "time": "HH:MM", "prev_date": "YYYY-MM-DD"|null, "prev_time": "HH:MM"|null, "published": bool}

Per tick: today's slot missing/old -> draw a new time (old date/time move to prev_*) · now >= time and not published -> run the publish
command (default: python3 <BM_PUBLISH_DIR>/scripts/publish_next.py); exit 0 -> published=true · otherwise do nothing.
  --status   print the state (and today's slot) without running anything
  --now ISO  test clock (needs a UTC offset)
"""
import argparse
import datetime as dt
import json
import os
import random
import subprocess
import sys
from pathlib import Path

KST = dt.timezone(dt.timedelta(hours=9))
FIRST_HOUR, LAST_HOUR = 12, 17            # draw window 12:00-17:59
HOME = Path(os.path.expanduser("~"))
DEFAULT_STATE = HOME / ".ipe" / "queue" / "bottledmarbles" / "slot.json"
DEFAULT_REPO = HOME / ".ipe" / "bottledmarbles-publish" / "repo"


def draw_time(date, prev_time):
    """Random HH:MM in [12:00, 17:59] whose hour differs from prev_time's hour. Seeded by the date -> reproducible and testable."""
    hours = [h for h in range(FIRST_HOUR, LAST_HOUR + 1) if prev_time is None or h != int(prev_time[:2])]
    rng = random.Random("bottledmarbles:%s" % date)
    return "%02d:%02d" % (rng.choice(hours), rng.randrange(60))


def roll(state, today):
    """State for `today`: keeps it when it is already today's, otherwise draws a new slot and moves the old one to prev_*."""
    if state and state.get("date") == today:
        return state
    prev_date = state.get("date") if state else None
    prev_time = state.get("time") if state else None
    return {"date": today, "time": draw_time(today, prev_time), "prev_date": prev_date, "prev_time": prev_time, "published": False}


def due(state, now):
    return (not state["published"]) and now.strftime("%H:%M") >= state["time"]


def load_state(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def save_state(path, state):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    os.replace(str(tmp), str(path))


def log(msg, now):
    print("[%s KST] gate: %s" % (now.strftime("%Y-%m-%d %H:%M:%S"), msg), flush=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--state", default=os.environ.get("BM_SLOT_FILE", str(DEFAULT_STATE)))
    ap.add_argument("--repo", default=os.environ.get("BM_PUBLISH_DIR", str(DEFAULT_REPO)))
    ap.add_argument("--publish-cmd", default=os.environ.get("BM_PUBLISH_CMD"), help="shell command; default python3 <repo>/scripts/publish_next.py")
    ap.add_argument("--now", help="ISO time with offset (tests)")
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args(argv)
    now = dt.datetime.fromisoformat(a.now).astimezone(KST) if a.now else dt.datetime.now(KST)
    today = now.strftime("%Y-%m-%d")

    state = roll(load_state(a.state), today)
    if a.status:
        print(json.dumps(state, ensure_ascii=False))
        return 0
    if state != load_state(a.state):
        save_state(a.state, state)
        log("new slot %s (prev %s)" % (state["time"], state["prev_time"]), now)
    if state["published"]:
        return 0
    if not due(state, now):
        return 0
    cmd = a.publish_cmd or "python3 %s" % os.path.join(a.repo, "scripts", "publish_next.py")
    log("slot %s reached — publishing: %s" % (state["time"], cmd), now)
    rc = subprocess.call(cmd, shell=True)
    if rc == 0:
        state["published"] = True
        save_state(a.state, state)
        log("published", now)
        return 0
    log("publish exited %d — slot stays open, next tick retries" % rc, now)
    return rc


if __name__ == "__main__":
    sys.exit(main())
