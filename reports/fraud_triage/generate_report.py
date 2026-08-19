#!/usr/bin/env python3
"""Daily fraud-triage report: low-bonus IAPs (>=$19.99, linked bonus <1.0x) over rolling 72h PT."""

from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

PT = ZoneInfo("America/Los_Angeles")
ROOT = Path(__file__).resolve().parent
DATA = Path("/tmp/report_data")
ART = Path("/opt/cursor/artifacts")
OUT = ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)
ART.mkdir(parents=True, exist_ok=True)

ALLOWLIST_CANONICAL = [
    "Pixel Flow",
    "Animals & Coins",
    "Merge Cooking",
    "Box Jam",
    "Yarn Loop",
    "Dice Dreams",
    "Candy Crush Saga",
    "Legend of Mushroom",
    "Palmon: Survival",
    "Zombie Waves",
    "Merge Meow Cafe",
    "Fable Town",
    "Merge Cruise",
    "Coin Master Board Adventure",
    "Call of Dragons",
    "Merge Islanders",
    "Tile Match Puzzle",
    "Drop the Cat",
    "Alice's Mergeland",
    "Goblins Wood",
    "Warhammer 40,000: Tacticus",
    "Eatventure",
    "Project Makeover",
    "Jewel Hunter",
    "EverMerge",
    "Word Search Sea",
    "Clash of Critters",
    "Screw Guru",
    "Merge Restaurant",
    "Doomsday: Last Survivors",
    "Cryptogram",
    "Domino Dreams",
    "Angry Bird 2",
    "Angry Birds 2",
    "Tetris Block Party",
    "Word Trip",
    "Crossword Go!",
    "Crossword Go",
    "Merge Cat Detective",
    "Beast Lord",
    "Unravel Master",
    "Merge Gardens",
    "We Are Warriors",
]

# Affirmative fraud-family payout-risk signals (not the low-bonus IAP pattern itself).
ADVERSE_SIGNAL_RES = [
    re.compile(r"verisoul_fake", re.I),
    re.compile(r"adverse_linked", re.I),
    re.compile(r"unverified_high_earner", re.I),
    re.compile(r"multiple_prior_denials", re.I),
    re.compile(r"device_.*bridge|network_bridge|mobile_id_bridge|linked_device", re.I),
    re.compile(r"verified_mule", re.I),
    re.compile(r"failed_idv|failed_identity|identity_verification_failed", re.I),
]


def parse_ts(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def load_rows(name: str) -> list:
    raw = json.loads((DATA / name).read_text())
    if isinstance(raw, list):
        return raw
    return raw["rows"]


def norm_title(s: str) -> str:
    s = (s or "").strip().lower()
    s = s.replace("’", "'").replace("‘", "'")
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[!?.]+$", "", s)
    # punctuation-light key
    return re.sub(r"[^a-z0-9&: ]+", "", s)


ALLOW_NORM = {norm_title(t): t for t in ALLOWLIST_CANONICAL}
# Prefer display names without Angry Birds duplicate
DISPLAY_FOR = dict(ALLOW_NORM)
DISPLAY_FOR[norm_title("Angry Birds 2")] = "Angry Birds 2"
DISPLAY_FOR[norm_title("Angry Bird 2")] = "Angry Birds 2"
DISPLAY_FOR[norm_title("Crossword Go")] = "Crossword Go!"
DISPLAY_FOR[norm_title("Crossword Go!")] = "Crossword Go!"


def match_allowlist(game_name: str) -> str | None:
    key = norm_title(game_name)
    if key in DISPLAY_FOR:
        return DISPLAY_FOR[key]
    # soft punctuation variants already handled by norm
    return None


def is_blocked(profile: dict) -> bool:
    status = (profile.get("status") or "").lower()
    if status == "blocked":
        return True
    if profile.get("payout_hold") is True:
        return True
    return False


def phone_concern(profile: dict) -> list[str]:
    markers = []
    pi = profile.get("phone_intelligence") or {}
    if pi.get("is_voip") or str(pi.get("line_type") or "").lower() == "voip":
        markers.append("voip_phone")
    sms = pi.get("sms_risk") or {}
    level = str(sms.get("level") or "").lower()
    score = sms.get("score")
    try:
        score_n = float(score) if score is not None else 0.0
    except (TypeError, ValueError):
        score_n = 0.0
    if level in ("high", "very_high", "critical") or score_n >= 70:
        markers.append(f"high_phone_sms_risk:{level or score_n}")
    return markers


def concern_markers(uid: int, profile: dict, verisoul: dict | None, payout: dict | None) -> list[str]:
    markers: list[str] = []
    # Verisoul Fake / Suspicious
    if verisoul:
        decision = (verisoul.get("decision") or "").strip()
        if decision in ("Fake", "Suspicious"):
            markers.append(f"verisoul_{decision.lower()}")
        linked = int(verisoul.get("accounts_linked") or 0)
        try:
            multi = float(verisoul.get("multiple_accounts") or 0)
        except (TypeError, ValueError):
            multi = 0.0
        if linked >= 2:
            markers.append(f"accounts_linked:{linked}")
        elif multi >= 0.5:
            markers.append(f"high_multiple_accounts:{multi:.2f}")

    # Registration risk
    score = profile.get("registration_risk_score")
    action = (profile.get("registration_risk_action") or "").lower()
    try:
        score_n = float(score) if score is not None else None
    except (TypeError, ValueError):
        score_n = None
    if score_n is not None and score_n >= 70:
        markers.append(f"elevated_registration_risk:{score_n:g}")
    if action in ("block", "deny", "manual_review", "review"):
        markers.append(f"registration_risk_action:{action}")

    markers.extend(phone_concern(profile))

    # Affirmative payout-risk fraud signals (exclude low_iap_cashback — that's the cohort pattern)
    if payout:
        for sig in payout.get("signals") or []:
            if re.search(r"low[_ ]?iap[_ ]?cashback|low_matched_cashback", str(sig), re.I):
                continue
            if any(rx.search(str(sig)) for rx in ADVERSE_SIGNAL_RES):
                markers.append(f"payout_signal:{sig}")

    # de-dupe preserve order
    seen = set()
    out = []
    for m in markers:
        if m not in seen:
            seen.add(m)
            out.append(m)
    return out


def consecutive_days(dates: list) -> bool:
    """True if any two PT calendar dates are the same or differ by 1 day."""
    if len(dates) < 2:
        return False
    uniq = sorted(set(dates))
    if len(uniq) == 1:
        return True  # same-day multi purchase handled by count; still consecutive pattern
    for a, b in zip(uniq, uniq[1:]):
        if (b - a).days <= 1:
            return True
    return False


def severity_score(member: dict) -> float:
    """Higher = more urgent for priority alert list."""
    score = 0.0
    score += member["purchase_count"] * 3
    score += member["purchase_usd"] / 50.0
    score += len(member["concern_markers"]) * 8
    score += member["allowlist_earnings_usd"] / 20.0
    if member["days_span"] >= 2:
        score += 5
    if member["min_multiplier"] <= 0.25:
        score += 4
    elif member["min_multiplier"] <= 0.5:
        score += 2
    return score


def main() -> None:
    now_utc = datetime.now(tz=timezone.utc)
    now_pt = now_utc.astimezone(PT)
    window_end = now_utc
    window_start = window_end - timedelta(hours=72)
    buffer_start = window_start - timedelta(hours=24)

    query_log = {}
    if (DATA / "query_log.json").exists():
        query_log = json.loads((DATA / "query_log.json").read_text())

    purchases_all = load_rows("purchases.json")
    profiles = {r["id"]: r for r in load_rows("profiles_0.json") + load_rows("profiles_1.json")}
    verisoul = {r["user_profile_id"]: r for r in load_rows("verisoul.json")}
    payout_risk = {r["user_profile_id"]: r for r in load_rows("payout_risk.json")}
    earnings_all = load_rows("earnings.json")

    # Filter purchases: buffer for consecutive detection; report window for totals
    buf_purchases = []
    win_purchases = []
    for r in purchases_all:
        t = parse_ts(r["event_at"])
        iap = float(r["iap_usd"])
        mult = float(r["multiplier"])
        if iap < 19.99 or mult >= 1.0:
            continue
        if buffer_start <= t < window_end:
            buf_purchases.append({**r, "_ts": t, "_iap": iap, "_mult": mult})
        if window_start <= t < window_end:
            win_purchases.append({**r, "_ts": t, "_iap": iap, "_mult": mult})

    # Exclude internal users
    def keep_user(uid: int) -> bool:
        p = profiles.get(uid) or {}
        return not p.get("is_internal_user")

    win_purchases = [r for r in win_purchases if keep_user(r["user_profile_id"])]
    buf_purchases = [r for r in buf_purchases if keep_user(r["user_profile_id"])]

    # Group by member
    by_user_win: dict[int, list] = defaultdict(list)
    by_user_buf: dict[int, list] = defaultdict(list)
    for r in win_purchases:
        by_user_win[r["user_profile_id"]].append(r)
    for r in buf_purchases:
        by_user_buf[r["user_profile_id"]].append(r)

    members = []
    for uid, rows in by_user_win.items():
        profile = profiles.get(uid) or {"id": uid, "status": None, "payout_hold": False}
        v = verisoul.get(uid)
        pr = payout_risk.get(uid)
        markers = concern_markers(uid, profile, v, pr)
        blocked = is_blocked(profile)

        win_dates = [r["_ts"].astimezone(PT).date() for r in rows]
        buf_rows = by_user_buf.get(uid, rows)
        buf_dates = [r["_ts"].astimezone(PT).date() for r in buf_rows]
        same_day = len(rows) >= 2 and len(set(win_dates)) == 1
        consec = consecutive_days(sorted(set(buf_dates))) if len(buf_rows) >= 2 else False
        # Prompt definition: same-day or consecutive-day multi-purchase pattern.
        if same_day or (len(rows) >= 2 and consecutive_days(sorted(set(win_dates)))):
            is_repeat = True
            pattern = "same_day" if same_day else "consecutive_days"
        elif len(rows) == 1 and consec:
            # Single in-window purchase linked to buffer-day neighbor
            is_repeat = True
            pattern = "consecutive_across_boundary"
        elif len(rows) >= 2:
            # Multiple purchases with calendar gaps — not "one-time"; triage with alerts
            is_repeat = True
            pattern = "multi_nonconsecutive"
        else:
            is_repeat = False
            pattern = "one_time"

        purchase_detail = [
            {
                "at_pt": r["_ts"].astimezone(PT).strftime("%Y-%m-%d %H:%M %Z"),
                "date_pt": r["_ts"].astimezone(PT).date().isoformat(),
                "amount_usd": r["_iap"],
                "multiplier": r["_mult"],
                "mobile_game_id": r["mobile_game_id"],
                "bonus_id": r["bonus_id"],
            }
            for r in sorted(rows, key=lambda x: x["_ts"])
        ]

        members.append(
            {
                "user_id": uid,
                "cohort": "repeat" if is_repeat else "one_time",
                "pattern": pattern,
                "purchase_count": len(rows),
                "purchase_usd": round(sum(r["_iap"] for r in rows), 2),
                "min_multiplier": min(r["_mult"] for r in rows),
                "avg_multiplier": round(sum(r["_mult"] for r in rows) / len(rows), 4),
                "purchase_dates": sorted(set(win_dates)),
                "days_span": (max(win_dates) - min(win_dates)).days + 1,
                "purchases": purchase_detail,
                "concern_markers": markers,
                "has_concern": bool(markers),
                "blocked": blocked,
                "status": profile.get("status"),
                "payout_hold": bool(profile.get("payout_hold")),
                "admin_url": f"https://admin.recosocial.com/users/{uid}",
                "allowlist_earnings_usd": 0.0,
                "allowlist_by_game": {},
            }
        )

    # Allowlist earnings (same 72h window; filter in Python — do not infer allowlist from revenue)
    earn_rows_allow = []
    for r in earnings_all:
        # exclude buffer bleed if any
        d = str(r.get("earn_date_pt") or "")[:10]
        matched = match_allowlist(r["game_name"])
        if not matched:
            continue
        uid = int(r["user_id"])
        if uid not in by_user_win:
            continue
        usd = float(r["earnings_usd"])
        earn_rows_allow.append(
            {
                "user_id": uid,
                "game": matched,
                "earn_date_pt": d,
                "earnings_usd": usd,
                "credit_events": int(r.get("credit_events") or 0),
            }
        )

    earn_by_user_game = defaultdict(float)
    earn_by_user = defaultdict(float)
    for e in earn_rows_allow:
        earn_by_user_game[(e["user_id"], e["game"])] += e["earnings_usd"]
        earn_by_user[e["user_id"]] += e["earnings_usd"]

    for m in members:
        m["allowlist_earnings_usd"] = round(earn_by_user.get(m["user_id"], 0.0), 2)
        games = {
            g: round(v, 2)
            for (uid, g), v in earn_by_user_game.items()
            if uid == m["user_id"]
        }
        m["allowlist_by_game"] = dict(sorted(games.items(), key=lambda x: -x[1]))
        m["severity"] = severity_score(m)

    # Cohorts
    repeaters = [m for m in members if m["cohort"] == "repeat"]
    one_timers = [m for m in members if m["cohort"] == "one_time"]
    concerning = [m for m in members if m["has_concern"]]
    blocked_members = [m for m in members if m["blocked"]]

    def rate(group):
        if not group:
            return 0.0
        return sum(1 for m in group if m["has_concern"]) / len(group)

    rep_rate = rate(repeaters)
    one_rate = rate(one_timers)
    if one_rate > 0:
        rr = rep_rate / one_rate
    elif rep_rate > 0:
        rr = float("inf")
    else:
        rr = None

    # Actionable lists exclude already blocked
    priority_alerts = sorted(
        [m for m in repeaters if not m["blocked"]],
        key=lambda m: (-m["severity"], -m["purchase_usd"], -m["purchase_count"]),
    )
    watchlist = sorted(
        [m for m in one_timers if not m["blocked"]],
        key=lambda m: (-m["purchase_usd"], m["min_multiplier"], m["user_id"]),
    )

    # High allowlist earners among repeaters (triage signal)
    earn_vals = [m["allowlist_earnings_usd"] for m in members if m["allowlist_earnings_usd"] > 0]
    if earn_vals:
        threshold = max(
            25.0,
            sorted(earn_vals)[max(0, int(math.ceil(len(earn_vals) * 0.9)) - 1)],
        )
    else:
        threshold = 25.0
    high_earn_repeaters = [
        m
        for m in repeaters
        if m["allowlist_earnings_usd"] >= threshold and not m["blocked"]
    ]

    # Summary metrics for allowlist earnings
    total_allow_earn = sum(m["allowlist_earnings_usd"] for m in members)
    members_with_earn = sum(1 for m in members if m["allowlist_earnings_usd"] > 0)
    repeat_allow_earn = sum(m["allowlist_earnings_usd"] for m in repeaters)
    earn_per_member = total_allow_earn / len(members) if members else 0.0
    repeat_share = (repeat_allow_earn / total_allow_earn) if total_allow_earn else 0.0

    # ---------- Charts ----------
    # 1) Stacked daily bar: earnings by game title and cohort
    daily = defaultdict(lambda: defaultdict(float))  # date -> game -> usd (all cohorts combined stacked by game)
    daily_cohort = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    member_cohort = {m["user_id"]: m["cohort"] for m in members}
    for e in earn_rows_allow:
        cohort = member_cohort.get(e["user_id"], "one_time")
        daily[e["earn_date_pt"]][e["game"]] += e["earnings_usd"]
        daily_cohort[e["earn_date_pt"]][cohort][e["game"]] += e["earnings_usd"]

    # Stacked by game per day (total across cohorts), color by game; facet note in title about cohort
    fig, ax = plt.subplots(figsize=(12, 6))
    dates = sorted(daily.keys())
    # top games by total
    game_totals = Counter()
    for d in dates:
        for g, v in daily[d].items():
            game_totals[g] += v
    top_games = [g for g, _ in game_totals.most_common(12)]
    other_label = "Other allowlist"
    bottoms = [0.0] * len(dates)
    colors = plt.cm.tab20.colors
    for i, g in enumerate(top_games + ([other_label] if game_totals else [])):
        vals = []
        for d in dates:
            if g == other_label:
                vals.append(sum(v for gg, v in daily[d].items() if gg not in top_games))
            else:
                vals.append(daily[d].get(g, 0.0))
        ax.bar(dates, vals, bottom=bottoms, label=g, color=colors[i % len(colors)])
        bottoms = [b + v for b, v in zip(bottoms, vals)]
    ax.set_title("Allowlist game earnings by PT day (qualifying IAP members)")
    ax.set_ylabel("Earnings (USD)")
    ax.set_xlabel("Date (America/Los_Angeles)")
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), fontsize=8)
    fig.tight_layout()
    chart1 = OUT / "chart_stacked_daily_earnings.png"
    fig.savefig(chart1, dpi=140, bbox_inches="tight")
    fig.savefig(ART / "chart_stacked_daily_earnings.png", dpi=140, bbox_inches="tight")
    plt.close(fig)

    # Cohort-split stacked daily (repeat vs one-time totals)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
    for ax, cohort, title in zip(
        axes,
        ["repeat", "one_time"],
        ["Repeat/consecutive", "One-time"],
    ):
        bottoms = [0.0] * len(dates)
        for i, g in enumerate(top_games[:8]):
            vals = [daily_cohort[d][cohort].get(g, 0.0) for d in dates]
            ax.bar(dates, vals, bottom=bottoms, label=g, color=colors[i % len(colors)])
            bottoms = [b + v for b, v in zip(bottoms, vals)]
        ax.set_title(f"{title} cohort")
        ax.set_xlabel("Date (PT)")
        ax.tick_params(axis="x", rotation=30)
    axes[0].set_ylabel("Earnings (USD)")
    axes[1].legend(loc="upper left", bbox_to_anchor=(1.02, 1), fontsize=8)
    fig.suptitle("Allowlist earnings by day × cohort (top games)")
    fig.tight_layout()
    chart1b = OUT / "chart_stacked_daily_by_cohort.png"
    fig.savefig(chart1b, dpi=140, bbox_inches="tight")
    fig.savefig(ART / "chart_stacked_daily_by_cohort.png", dpi=140, bbox_inches="tight")
    plt.close(fig)

    # 2) Ranked bar: total earnings by game title
    fig, ax = plt.subplots(figsize=(10, 7))
    ranked = game_totals.most_common(20)
    if ranked:
        names = [g for g, _ in ranked][::-1]
        vals = [v for _, v in ranked][::-1]
        ax.barh(names, vals, color="#2c6e49")
    ax.set_xlabel("Total earnings (USD)")
    ax.set_title("Allowlist earnings by game (72h window, qualifying members)")
    fig.tight_layout()
    chart2 = OUT / "chart_ranked_game_earnings.png"
    fig.savefig(chart2, dpi=140, bbox_inches="tight")
    fig.savefig(ART / "chart_ranked_game_earnings.png", dpi=140, bbox_inches="tight")
    plt.close(fig)

    # 3) Member-level: allowlist earnings vs qualifying purchase count
    fig, ax = plt.subplots(figsize=(10, 6))
    for cohort, color, label in [
        ("repeat", "#c1121f", "Repeat/consecutive"),
        ("one_time", "#457b9d", "One-time"),
    ]:
        xs = [m["purchase_count"] for m in members if m["cohort"] == cohort]
        ys = [m["allowlist_earnings_usd"] for m in members if m["cohort"] == cohort]
        sizes = [40 + (20 if m["has_concern"] else 0) for m in members if m["cohort"] == cohort]
        ax.scatter(xs, ys, c=color, alpha=0.7, s=sizes, label=label, edgecolors="k", linewidths=0.3)
    ax.axhline(threshold, color="#666", linestyle="--", linewidth=1, label=f"High-earn triage ≥ ${threshold:.0f}")
    ax.set_xlabel("Qualifying purchases (72h)")
    ax.set_ylabel("Allowlist game earnings (USD)")
    ax.set_title("Member allowlist earnings vs qualifying purchase count")
    ax.legend()
    fig.tight_layout()
    chart3 = OUT / "chart_member_earnings_vs_purchases.png"
    fig.savefig(chart3, dpi=140, bbox_inches="tight")
    fig.savefig(ART / "chart_member_earnings_vs_purchases.png", dpi=140, bbox_inches="tight")
    plt.close(fig)

    # ---------- Tables / HTML ----------
    def purchases_cell(m):
        parts = [
            f"{p['date_pt']} ${p['amount_usd']:.2f} @ {p['multiplier']:.2f}x"
            for p in m["purchases"]
        ]
        return "<br>".join(parts)

    def markers_cell(m):
        if not m["concern_markers"]:
            return "—"
        return "<br>".join(m["concern_markers"])

    def block_cell(m):
        if (m.get("status") or "").lower() == "blocked":
            return "Account Blocked/Deactivated by Compliance"
        if m.get("payout_hold"):
            return "Rewards/Payouts on Hold"
        return "No Compliance Action"

    def member_link(m):
        return f'<a href="{m["admin_url"]}">{m["user_id"]}</a>'

    # Member detail table (all)
    detail_rows = []
    for m in sorted(members, key=lambda x: (x["cohort"] != "repeat", -x["severity"])):
        detail_rows.append(
            f"<tr class='{'blocked' if m['blocked'] else ''}'>"
            f"<td>{member_link(m)}</td>"
            f"<td>{m['cohort']}</td>"
            f"<td>{m['purchase_count']}</td>"
            f"<td>${m['purchase_usd']:.2f}</td>"
            f"<td>{purchases_cell(m)}</td>"
            f"<td>{m['min_multiplier']:.2f}x</td>"
            f"<td>{markers_cell(m)}</td>"
            f"<td>{block_cell(m)}</td>"
            f"<td>${m['allowlist_earnings_usd']:.2f}</td>"
            f"</tr>"
        )

    # Earnings table member×game
    earn_table_rows = []
    for (uid, game), usd in sorted(earn_by_user_game.items(), key=lambda x: -x[1]):
        m = next(mm for mm in members if mm["user_id"] == uid)
        earn_table_rows.append(
            f"<tr class='{'blocked' if m['blocked'] else ''}'>"
            f"<td>{member_link(m)}</td>"
            f"<td>{game}</td>"
            f"<td>${usd:.2f}</td>"
            f"<td>{m['purchase_count']}</td>"
            f"<td>{markers_cell(m)}</td>"
            f"<td>{block_cell(m)}</td>"
            f"</tr>"
        )

    def alert_rows(group, limit=50):
        rows = []
        for i, m in enumerate(group[:limit], 1):
            rows.append(
                f"<tr>"
                f"<td>{i}</td>"
                f"<td>{member_link(m)}</td>"
                f"<td>{m['purchase_count']}</td>"
                f"<td>${m['purchase_usd']:.2f}</td>"
                f"<td>{purchases_cell(m)}</td>"
                f"<td>{m['min_multiplier']:.2f}x</td>"
                f"<td>{markers_cell(m)}</td>"
                f"<td>${m['allowlist_earnings_usd']:.2f}</td>"
                f"<td>{m['severity']:.1f}</td>"
                f"</tr>"
            )
        return rows

    rr_display = "n/a (no one-time concerns)" if rr is None else ("∞" if math.isinf(rr) else f"{rr:.2f}×")

    methodology = f"""
    <h2>Methodology</h2>
    <ul>
      <li><b>Run time:</b> {now_pt.strftime('%Y-%m-%d %H:%M:%S %Z')} ({now_utc.isoformat()})</li>
      <li><b>Window:</b> rolling 72 hours ending at run time —
        {window_start.astimezone(PT).strftime('%Y-%m-%d %H:%M %Z')} → {window_end.astimezone(PT).strftime('%Y-%m-%d %H:%M %Z')}</li>
      <li><b>Consecutive-day buffer:</b> +24h pre-window
        ({buffer_start.astimezone(PT).strftime('%Y-%m-%d %H:%M %Z')} → window start) used only to detect
        consecutive-day patterns crossing the boundary; buffer purchases are excluded from reported totals.</li>
      <li><b>Qualifying purchase:</b> confirmed IAP with <code>webhook_data.iapUsd</code> ≥ $19.99 USD and exact linked
        bonus multiplier &lt; 1.0× via <code>meta.bonus_consumption.iap_bonus.bonusId</code> → <code>user_bonuses</code>
        (<code>bonus_data.multiplier</code>).</li>
      <li><b>Repeat/consecutive:</b> ≥2 qualifying purchases on the same PT calendar day, or across consecutive PT days
        (buffer-aware). <b>One-time:</b> exactly one qualifying purchase in the 72h window without a consecutive-day link.</li>
      <li><b>Already blocked:</b> <code>user_profiles.status = 'blocked'</code> and/or <code>payout_hold = true</code>
        (BitLabs partner ban is not treated as a Compliance Action). Blocked members are labeled and excluded from
        suggested new actions (priority alerts / watchlist).</li>
      <li><b>Independent concern markers</b> (separate from the low-bonus pattern): Verisoul Fake/Suspicious;
        multi-account (<code>accounts_linked ≥ 2</code> or <code>multiple_accounts ≥ 0.5</code>); VoIP / high phone SMS risk;
        elevated registration risk; affirmative payout-risk fraud-family signals
        (<code>verisoul_fake_*</code>, <code>adverse_linked_*</code>, <code>unverified_high_earner</code>, device/network bridges,
        mule probes, failed IDV, multiple prior denials). Low-IAP-cashback signals are excluded as circular.</li>
      <li><b>Relative risk:</b> concern-marker rate(repeaters) / rate(one-time).</li>
      <li><b>Allowlist earnings:</b> ledger credits (<code>entry_kind='credit'</code>, <code>earning_type='game'</code>),
        USD = points × 0.01, same 72h window. Titles matched case-insensitively to the fixed non-cash allowlist
        (Pixel Flow, Animals &amp; Coins, and every other listed title). Membership is never inferred from in-window revenue.</li>
      <li><b>Internal users:</b> excluded. All currency USD. Every SQL query used LIMIT.</li>
      <li><b>Query log:</b> <pre>{json.dumps(query_log, indent=2)}</pre></li>
    </ul>
    """

    allowlist_html = "; ".join(
        sorted(
            {
                "Angry Birds 2" if "Angry Bird" in t else t
                for t in ALLOWLIST_CANONICAL
                if t not in ("Angry Bird 2", "Crossword Go")
            }
        )
    )

    high_callout = ""
    if high_earn_repeaters:
        items = "".join(
            f"<li>{member_link(m)} — {m['purchase_count']} qualifying purchases, "
            f"${m['allowlist_earnings_usd']:.2f} allowlist earnings, markers: {', '.join(m['concern_markers']) or 'none'}"
            f"{' (BLOCKED)' if m['blocked'] else ''}</li>"
            for m in sorted(high_earn_repeaters, key=lambda x: -x["allowlist_earnings_usd"])[:25]
        )
        high_callout = f"""
        <div class="callout">
          <h3>Triage callout — repeat/consecutive + elevated allowlist earnings (≥ ${threshold:.0f})</h3>
          <p>Signal only — not proof of abuse. Review manually.</p>
          <ul>{items}</ul>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Fraud Triage Report — Rolling 72h PT</title>
<style>
  body {{ font-family: "IBM Plex Sans", "Source Sans 3", system-ui, sans-serif; margin: 24px; color: #1a1a1a; background: #f7f5f1; }}
  h1,h2,h3 {{ font-family: "IBM Plex Serif", Georgia, serif; }}
  .meta {{ color: #444; margin-bottom: 16px; }}
  .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin: 16px 0 24px; }}
  .card {{ background: #fff; border: 1px solid #ddd; padding: 12px 14px; border-radius: 4px; }}
  .card .n {{ font-size: 1.6rem; font-weight: 700; }}
  .card .l {{ font-size: 0.85rem; color: #555; }}
  table {{ border-collapse: collapse; width: 100%; background: #fff; font-size: 0.85rem; margin: 12px 0 28px; }}
  th, td {{ border: 1px solid #ddd; padding: 6px 8px; vertical-align: top; text-align: left; }}
  th {{ background: #e8e4dc; position: sticky; top: 0; }}
  tr.blocked {{ background: #f0e6e6; }}
  img.chart {{ max-width: 100%; height: auto; background: #fff; border: 1px solid #ddd; margin: 8px 0 20px; }}
  .callout {{ background: #fff8e7; border-left: 4px solid #c9a227; padding: 12px 16px; margin: 16px 0; }}
  .warn {{ color: #8b1e1e; }}
  code, pre {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.8rem; }}
  pre {{ background: #fff; padding: 8px; overflow: auto; border: 1px solid #ddd; }}
</style>
</head>
<body>
<h1>Daily fraud-triage report</h1>
<p class="meta">Rolling 72-hour window ending {now_pt.strftime('%Y-%m-%d %H:%M %Z')} · Currency USD · Read-only Postgres</p>

<div class="cards">
  <div class="card"><div class="n">{len(members)}</div><div class="l">Qualifying members</div></div>
  <div class="card"><div class="n">{len(win_purchases)}</div><div class="l">Qualifying purchases</div></div>
  <div class="card"><div class="n">{len(repeaters)}</div><div class="l">Repeat/consecutive members</div></div>
  <div class="card"><div class="n">{sum(m['purchase_count'] for m in repeaters)}</div><div class="l">Repeat cohort purchases</div></div>
  <div class="card"><div class="n">{len(one_timers)}</div><div class="l">One-time members</div></div>
  <div class="card"><div class="n">{sum(m['purchase_count'] for m in one_timers)}</div><div class="l">One-time purchases</div></div>
  <div class="card"><div class="n">{len(concerning)}</div><div class="l">Independently concerning</div></div>
  <div class="card"><div class="n">{len(blocked_members)}</div><div class="l">Already blocked / on hold</div></div>
</div>

<h2>Concern-marker rates &amp; relative risk</h2>
<table>
<tr><th>Cohort</th><th>Members</th><th>With independent concerns</th><th>Rate</th></tr>
<tr><td>Repeat/consecutive</td><td>{len(repeaters)}</td>
<td>{sum(1 for m in repeaters if m['has_concern'])}</td><td>{rep_rate*100:.1f}%</td></tr>
<tr><td>One-time</td><td>{len(one_timers)}</td>
<td>{sum(1 for m in one_timers if m['has_concern'])}</td><td>{one_rate*100:.1f}%</td></tr>
<tr><td colspan="3"><b>Relative risk (repeat ÷ one-time)</b></td><td><b>{rr_display}</b></td></tr>
</table>
<p>Already blocked members are included in rates for visibility but <b>excluded</b> from priority alerts and the one-time watchlist.</p>

{high_callout}

<h2>Priority alerts — repeat/consecutive (ranked by severity)</h2>
<p>Excludes already blocked. Severity combines purchase count/amount, concern markers, allowlist earnings, day span, and low multipliers.</p>
<table>
<tr><th>#</th><th>Member</th><th>Purchases</th><th>Total USD</th><th>Dates / amounts / mult</th><th>Min mult</th><th>Concern markers</th><th>Allowlist $</th><th>Severity</th></tr>
{''.join(alert_rows(priority_alerts, 75))}
</table>

<h2>Watchlist — one-time behavior</h2>
<p>Exactly one qualifying purchase in-window; excludes already blocked. Sorted by purchase amount then lowest multiplier.</p>
<table>
<tr><th>#</th><th>Member</th><th>Purchases</th><th>Total USD</th><th>Dates / amounts / mult</th><th>Min mult</th><th>Concern markers</th><th>Allowlist $</th><th>Severity</th></tr>
{''.join(alert_rows(watchlist, 75))}
</table>

<h2>Independently concerning members</h2>
<table>
<tr><th>Member</th><th>Cohort</th><th>Purchases</th><th>USD</th><th>Markers</th><th>Block status</th></tr>
{''.join(
  f"<tr class='{'blocked' if m['blocked'] else ''}'><td>{member_link(m)}</td><td>{m['cohort']}</td>"
  f"<td>{m['purchase_count']}</td><td>${m['purchase_usd']:.2f}</td><td>{markers_cell(m)}</td><td>{block_cell(m)}</td></tr>"
  for m in sorted(concerning, key=lambda x: (-len(x['concern_markers']), -x['purchase_usd']))
)}
</table>

<h2>Already blocked / payout hold</h2>
<table>
<tr><th>Member</th><th>Cohort</th><th>Purchases</th><th>USD</th><th>Status</th><th>Suggested action</th></tr>
{''.join(
  f"<tr class='blocked'><td>{member_link(m)}</td><td>{m['cohort']}</td><td>{m['purchase_count']}</td>"
  f"<td>${m['purchase_usd']:.2f}</td><td>{block_cell(m)}</td><td class='warn'>No new action — already restricted</td></tr>"
  for m in blocked_members
) or '<tr><td colspan="6">None in this window</td></tr>'}
</table>

<h2>Allowlist (non-cash) game earnings</h2>
<div class="cards">
  <div class="card"><div class="n">${total_allow_earn:,.2f}</div><div class="l">Total allowlist earnings</div></div>
  <div class="card"><div class="n">${earn_per_member:,.2f}</div><div class="l">Earnings / qualifying member</div></div>
  <div class="card"><div class="n">{members_with_earn}</div><div class="l">Members with allowlist earnings</div></div>
  <div class="card"><div class="n">{repeat_share*100:.1f}%</div><div class="l">Share from repeat/consecutive</div></div>
  <div class="card"><div class="n">${repeat_allow_earn:,.2f}</div><div class="l">Repeat cohort allowlist $</div></div>
</div>
<p><b>Fixed allowlist</b> (do not infer from revenue): {allowlist_html}</p>

<img class="chart" src="chart_stacked_daily_by_cohort.png" alt="Stacked daily earnings by cohort"/>
<img class="chart" src="chart_stacked_daily_earnings.png" alt="Stacked daily earnings by game"/>
<img class="chart" src="chart_ranked_game_earnings.png" alt="Ranked game earnings"/>
<img class="chart" src="chart_member_earnings_vs_purchases.png" alt="Member earnings vs purchases"/>

<h3>Member × game allowlist earnings</h3>
<table>
<tr><th>Member</th><th>Game</th><th>Earnings USD</th><th>Qualifying purchases</th><th>Concern markers</th><th>Block status</th></tr>
{''.join(earn_table_rows) or '<tr><td colspan="6">No allowlist earnings in window</td></tr>'}
</table>

<h2>Full member detail</h2>
<table>
<tr><th>Member</th><th>Cohort</th><th>#</th><th>USD</th><th>Purchase detail</th><th>Min mult</th><th>Markers</th><th>Block</th><th>Allowlist $</th></tr>
{''.join(detail_rows)}
</table>

{methodology}
</body>
</html>
"""

    report_path = OUT / "fraud_triage_72h.html"
    report_path.write_text(html)
    (ART / "fraud_triage_72h.html").write_text(html)
    # also copy charts next to artifact html references — rewrite artifact html to use absolute-friendly names
    for name in [
        "chart_stacked_daily_earnings.png",
        "chart_stacked_daily_by_cohort.png",
        "chart_ranked_game_earnings.png",
        "chart_member_earnings_vs_purchases.png",
    ]:
        src = OUT / name
        if src.exists():
            (ART / name).write_bytes(src.read_bytes())

    summary = {
        "run_pt": now_pt.isoformat(),
        "window_start_utc": window_start.isoformat(),
        "window_end_utc": window_end.isoformat(),
        "members": len(members),
        "purchases": len(win_purchases),
        "repeat_members": len(repeaters),
        "repeat_purchases": sum(m["purchase_count"] for m in repeaters),
        "one_time_members": len(one_timers),
        "one_time_purchases": sum(m["purchase_count"] for m in one_timers),
        "independently_concerning": len(concerning),
        "already_blocked": len(blocked_members),
        "repeat_concern_rate": round(rep_rate, 4),
        "one_time_concern_rate": round(one_rate, 4),
        "relative_risk": None if rr is None or math.isinf(rr) else round(rr, 3),
        "relative_risk_display": rr_display,
        "allowlist_earnings_total_usd": round(total_allow_earn, 2),
        "allowlist_earnings_per_member_usd": round(earn_per_member, 2),
        "allowlist_repeat_share": round(repeat_share, 4),
        "high_earn_threshold_usd": threshold,
        "high_earn_repeaters": [m["user_id"] for m in high_earn_repeaters],
        "priority_alert_count": len(priority_alerts),
        "watchlist_count": len(watchlist),
        "report_html": str(report_path),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2))
    (ART / "fraud_triage_summary.json").write_text(json.dumps(summary, indent=2))
    (OUT / "members.json").write_text(json.dumps(members, indent=2, default=str))

    # Markdown snapshot for PR
    md = f"""# Fraud triage — rolling 72h PT

**Run:** {now_pt.strftime('%Y-%m-%d %H:%M %Z')}

| Metric | Value |
|--------|------:|
| Qualifying members | {len(members)} |
| Qualifying purchases | {len(win_purchases)} |
| Repeat/consecutive members (purchases) | {len(repeaters)} ({sum(m['purchase_count'] for m in repeaters)}) |
| One-time members (purchases) | {len(one_timers)} ({sum(m['purchase_count'] for m in one_timers)}) |
| Independently concerning | {len(concerning)} |
| Already blocked / hold | {len(blocked_members)} |
| Repeat concern rate | {rep_rate*100:.1f}% |
| One-time concern rate | {one_rate*100:.1f}% |
| Relative risk | {rr_display} |
| Allowlist earnings (USD) | ${total_allow_earn:,.2f} |
| Earnings / member | ${earn_per_member:,.2f} |
| Share from repeaters | {repeat_share*100:.1f}% |

Full interactive tables and charts: `reports/fraud_triage/output/fraud_triage_72h.html`
"""
    (ROOT / "REPORT.md").write_text(md)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
