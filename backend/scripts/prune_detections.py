#!/usr/bin/env python
"""Retire detections that should not be in the corridor log.

Goes through the API (DELETE /api/v1/detections/{id}) rather than the database,
so the same rules and logging apply as for any other client.

Dry run unless --delete is passed. Nothing is removed just by looking.

    # what would go, and why
    python scripts/prune_detections.py --off-corridor

    # actually remove them
    python scripts/prune_detections.py --off-corridor --delete

    # specific records
    python scripts/prune_detections.py --id 12557495-... --id d58cb5c1-... --delete

    # against a different deployment
    python scripts/prune_detections.py --api https://pipe-proctor.vercel.app --off-corridor
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import urllib.error
import urllib.request

# The corridor, as the frontend models it (see frontend/src/lib/corridor.js).
HEAD = (13.6, 13.1)    # Agadem oilfields
TAIL = (6.36, 2.65)    # Seme terminal
CORRIDOR_KM = 1950
SEGMENT_COUNT = 20
DEFAULT_MAX_OFFSET_KM = 150
KM_PER_DEGREE = 111.32

_REF_LAT = (HEAD[0] + TAIL[0]) / 2


def _plane(lat: float, lon: float) -> tuple[float, float]:
    """Equirectangular projection to kilometres."""
    return lon * KM_PER_DEGREE * math.cos(math.radians(_REF_LAT)), lat * KM_PER_DEGREE


_H = _plane(*HEAD)
_T = _plane(*TAIL)
_AX, _AY = _T[0] - _H[0], _T[1] - _H[1]
_LEN_SQ = _AX * _AX + _AY * _AY


def locate(lat: float, lon: float) -> tuple[int | None, float]:
    """Project a coordinate onto the corridor.

    Returns the 1-based segment (None when too far off) and the distance in
    kilometres from the corridor line.
    """
    px, py = _plane(lat, lon)
    raw = ((px - _H[0]) * _AX + (py - _H[1]) * _AY) / _LEN_SQ
    along = min(1.0, max(0.0, raw))
    perpendicular = math.hypot(px - (_H[0] + along * _AX), py - (_H[1] + along * _AY))
    overshoot = abs(raw - along) * math.sqrt(_LEN_SQ)
    offset = math.hypot(perpendicular, overshoot)
    segment = min(SEGMENT_COUNT, int(along * SEGMENT_COUNT) + 1)
    return segment, offset


def request(api: str, path: str, method: str = "GET"):
    req = urllib.request.Request(f"{api}{path}", method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status == 204:
                return None
            return json.load(response)
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"{method} {path} failed: {exc.code} {exc.read().decode()[:200]}")
    except urllib.error.URLError as exc:
        raise SystemExit(f"cannot reach {api}: {exc.reason}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--api", default="http://127.0.0.1:8000",
                        help="API base URL (default: %(default)s)")
    parser.add_argument("--off-corridor", action="store_true",
                        help="select every detection further than --max-offset from the line")
    parser.add_argument("--id", dest="ids", action="append", default=[],
                        help="select a specific detection id (repeatable)")
    parser.add_argument("--max-offset", type=float, default=DEFAULT_MAX_OFFSET_KM,
                        help="km from the corridor line before a detection counts as off "
                             "(default: %(default)s)")
    parser.add_argument("--delete", action="store_true",
                        help="actually delete. Without it this only reports.")
    args = parser.parse_args()

    if not args.off_corridor and not args.ids:
        parser.error("nothing selected: pass --off-corridor and/or --id")

    detections = request(f"{args.api}/api/v1", "/detections") or []
    print(f"{len(detections)} detections in the log")

    doomed, wanted = [], set(args.ids)
    for record in detections:
        segment, offset = locate(record["latitude"], record["longitude"])
        reason = None
        if record["id"] in wanted:
            reason = "id given"
            wanted.discard(record["id"])
        elif args.off_corridor and offset > args.max_offset:
            reason = f"{offset:,.0f} km off the corridor"
        if reason:
            doomed.append((record, segment, offset, reason))

    for missing in sorted(wanted):
        print(f"  ! {missing}  not in the log")

    if not doomed:
        print("nothing to remove.")
        return 0

    print(f"\n{len(doomed)} to remove:")
    for record, _segment, _offset, reason in doomed:
        print(f"  {record['id'][:8]}  {record['latitude']:>11.5f},{record['longitude']:<11.5f}"
              f"  {record['anomaly_type']:<16} {reason}")

    if not args.delete:
        print("\nDry run. Re-run with --delete to remove these.")
        return 0

    print()
    failures = 0
    for record, _segment, _offset, _reason in doomed:
        request(f"{args.api}/api/v1", f"/detections/{record['id']}", method="DELETE")
        still_there = True
        try:
            request(f"{args.api}/api/v1", f"/detections/{record['id']}")
        except SystemExit:
            still_there = False
        print(f"  {record['id'][:8]}  {'deleted' if not still_there else 'STILL PRESENT'}")
        failures += still_there

    print(f"\nremoved {len(doomed) - failures} of {len(doomed)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
