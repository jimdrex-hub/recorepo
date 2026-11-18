# Reco Social Daily Fraud Brief

**Window:** Tuesday 2026-11-17 00:00–24:00 America/Los_Angeles  
**UTC bounds used:** `2026-11-17 08:00:00` → `2026-11-18 08:00:00`  
**Sources:** `user_profiles`, `mobile_game_event_completions` (confirmed only), plus `ledger_entries`, `payouts`, `user_wallets`, `mobile_games`  
**Exclusions:** internal, admin, deleted (except linked-account shells), `admin_games_override`, `override_ip_for_testing`, Withdraw/Withdrawal events, non-confirmed completions  
**Admin links:** `https://admin.recosocial.com/users/{id}`

Confirmed policy violations are labeled **CONFIRMED**. Everything else is suspicious pending investigation.

---

## Part 1 — Executive morning brief

| Item | Value |
| --- | --- |
| Overall fraud risk | **Critical** |
| Members requiring review | **38** |
| 24h unique IAP on flagged members | **~$34,200** |
| 24h points on flagged / fabricated progression | **7,825 pts** impossible Lords Mobile dump; **12,500 pts** unverified MPL |
| Open payout / wallet book | **$667,325** (`pending_approval` $382,358 · `on_hold` $267,267 · `scheduled` $16,155 · `pending` $1,545) |
| Unheld critical/high liquid exposure | **~$98,000** pending + wallet on still-unheld watchlist |
| Case mix | **Critical 22 · High 10 · Medium 6 · Low 4** |
| Confirmed payouts resolved in window | 481 / **$79,762** |
| Flagged-control payouts confirmed | 27 / **$3,982** including **full_block 890126 paid $1,059.90** |
| Duplicate same-tx IAP | **0** |
| Failed/rejected completions | **0** |
| Reversals | not present in this window |
| Hold lifts in window | **1** (2130088) then **$3,695** paid 25 minutes later |

### Five most important findings

1. **CONFIRMED — 1710438 still unheld.** Tuesday unique IAP **$5,318** including **6× $500 Bruno in 6 minutes** (00:58–01:03 UTC) plus 3× $500 Jackpot Nights earlier. Pending **$16,378**. Paid **$374** in-window. Hits the 6×$500/20min and 4×$500/3min alerts. Engine bonus $2,625 at 30–50%. Hold + recover + IAP restrict **now**.
2. **CONFIRMED — control failures paid out.** `full_block` **890126** confirmed **$1,059.90** at 22:40 UTC. `restrict_games` **1648850** paid $71 with **$9,829** still pending. `payout_hold` did **not** stop IAP: **3008799 $1,500** (0 ledger bonus) and **3238228 $525** after hold. **2130088** lifted 19:28 UTC (`removal_reason` null) then paid **$3,695** at 19:53.
3. **CONFIRMED — day-0 IAP and a new Utah cluster.** **3275400** $2,720 Victory Blast, no ID/FM, wallet $1,390. **3279794** $2,020, ID yes / FM no, wallet $1,574 + $100 pending. **3284260** created 03:39 UTC, $463 Bruno, **shares IP `97.247.126.237` with unheld 2802466**. Distinct devices — hold both independently.
4. **CONFIRMED — impossible Lords Mobile dump.** **3273825** (created 13:52 UTC, no phone/ID/FM) went Install → Castle 5 through Castle 25 in **~4 seconds** (14:26:46–14:26:50). **7,825 pts**. Wallet $79. Fabricated or partner-callback injection, not play.
5. **Watchlist still unenforced.** **2847927** (C-JAX) $2,000 GFC + wallet $6,899 + pending $7,382. **2802466** another $3,045 IAP + pending $9,080. **3003760** (C-KATY) wallet **$11,172**. **3215995** still shares IDFA `7E776601-…` and now IP `65.59.179.38` with held **2715325**. **2723827 returned** to JAX `24.129.83.23`.

### Meaningful changes vs prior day and baseline

| Metric | Tue 11/17 | Mon 11/16 (queried) | vs Mon | 7d daily avg (11/10–16) | vs 7d | 30d Oct 1–30 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Members | 15,549 | 14,427 | **+8%** | 15,187 | **+2%** | 14,094 |
| Events | 35,567 | 32,686 | **+9%** | 34,492 | **+3%** | 29,454 |
| Points | 1,380,098 | 1,314,852 | **+5%** | 1,205,671 | **+14%** | 1,093,545 |
| Points excl. admin-award | 1,039,402 | — | — | — | **−14%** | — |
| Unique IAP | $95,766 | $76,840 | **+25%** | $118,913 | **−19%** | $77,390 |
| Engine bonus | $50,360 | $41,081 | **+23%** | — | — | — |
| Open book | $667,325 | $673,220 | **−1%** | — | — | — |
| Flagged-control paid | $3,982 | $4,299 | **−7%** | — | — | — |
| Promo CB ≥10k pts | 4 / 84,999 pts | 10 / 247,450 | cooled | — | — | — |
| IAP on currently-held | ~$10,007 event-sum | $4,563 | **worse leak** | — | — | — |

Admin-award callbacks (30 events / 340,696 pts, including Call of Dragons 70k–80k Power 20M awards to aged KYC VIPs **408197 / 322877 / 512810**) inflate headline points. Treat those as ops, not fraud.

Victory Blast unique IAP **recovered** $5,407 → $15,384 (near 7d $14,596). Jackpot Go **4574 spiked** $4,830 vs 7d avg $891 (**+442%**), concentrated in **2251716**. Bruno still **−50%** vs 7d. GFC 5749 cooled vs Monday ($7,998 → $4,002) but dual first+any-purchase fingerprint continues.

### Recommended actions this morning

1. Hold **1710438, 2847927, 2802466, 3275400, 3279794, 3284260, 3273825, 3215995, 3003760, 2744123, 3033023, 3197354, 2260308, 2310003, 2726598** if still unheld.
2. Deny / recover **890126 $1,059.90**. Hold remaining `full_block` pendings (**300466 $5,488**).
3. Keep held + IAP restrict: **3008799, 3238228, 3271386, 3260896, 3255293, 3249692, 3266164, 2766773, 2414145, 2715325**.
4. Hold shells **3094081, 3258863, 2762038, 3113035, 2478920, 2767755, 1184324, 1489513**.
5. Do **not** confirm any payout within 15 minutes of a hold lift. Require `removal_reason`. Stop IAP, promo CB, completions, and payout confirmation on `payout_hold` / `full_block` / `fraud_block` / `verisoul_block` / `restrict_games`.

---

## Part 2 — Member risk investigation

### 1. [1710438](https://admin.recosocial.com/users/1710438) — score **96** · Critical · High confidence · **HOLD NOW**

- Age ~99d. ID+FM+phone. Not VIP. Unheld. Nashville T-Mobile `172.58.148.120`. Device `10C31525-…`.
- Tue: 20 unique IAP **$5,318** (JN + Bruno). **6× $500 Bruno 00:58:31–01:03:46 UTC**. Also 3× $500 JN 17:41–17:48. Bonus $2,625 at <span style="color:#b91c1c">30%</span>/<span style="color:#b91c1c">40%</span>/<span style="color:#b91c1c">50%</span>.
- Pending **$16,378**. Paid $374 in-window. Wallet $3.60.
- **Strongest evidence:** direct velocity (6×$500/6 min) plus prior-day 6×$500/4 min leftover. **Reducing:** aged KYC. **Missing:** purchase receipts / partner tx match. **CONFIRMED** policy-velocity violation, not just suspicion.

### 2. [890126](https://admin.recosocial.com/users/890126) — score **95** · Critical · High · **RECOVER + DENY**

- `registration_risk_action=full_block`. ID+FM. El Paso.
- **CONFIRMED** payout 111065 **$1,059.90** resolved 22:40:57 UTC (requested Nov 1). Control did not stop confirmation.
- Wallet $0. No remaining pending in this pull.

### 3. [2847927](https://admin.recosocial.com/users/2847927) — score **94** · Critical · High · **HOLD + recover $1,912**

- C-JAX. Age 17d. ID+FM. Unheld (lifted Nov 12). IP **`24.129.83.23`** with **2692629** and **2723827** (2723827 **returned** to this IP). Distinct IDFAs — hold each independently, do not mass-hold the IP.
- Tue: 4× $500 GFC **$2,000** at <span style="color:#b91c1c">40%</span>/<span style="color:#b91c1c">50%</span>. Wallet **$6,899**. Pending **$7,382**.

### 4. [2802466](https://admin.recosocial.com/users/2802466) — score **93** · Critical · High · **HOLD + recover $3,119**

- Age 19d. ID+FM. Unheld. Utah IP **`97.247.126.237`** now shared with day-0 **3284260**. Distinct devices.
- Tue IAP **$3,045** (Cash Avalanche, GFC dual first+any within 1s — partner fingerprint, VB 3×$500). Bonus $1,167 including one <span style="color:#15803d">125%</span> $120. Pending **$9,080**. Wallet $1,272. Paid $3,119 Monday.

### 5. [3275400](https://admin.recosocial.com/users/3275400) — score **92** · Critical · High · **HOLD + KYC/FM-gate**

- **Day-0** created 16:19 UTC. Phone yes, **no ID, no FM**. Queens `99.56.175.31` (near held 3238228 on `99.56.175.73`, different device — do not cluster on /24).
- 8 VB purchases **$2,720**: $10@<span style="color:#b91c1c">10%</span>, $10@<span style="color:#b91c1c">20%</span>, $1,000@<span style="color:#b91c1c">40%</span>, $1,500@<span style="color:#b91c1c">50%</span>, $200@<span style="color:#ca8a04">100%</span>. Bonus $1,353. Wallet **$1,390**. No open payout yet.
- Direct evidence: day-0 high IAP + missing KYC. Circumstantial: Queens proximity to 3238228.

### 6. [3273825](https://admin.recosocial.com/users/3273825) — score **91** · Critical · High · **HOLD**

- **Day-0** 13:52 UTC. No phone/ID/FM. Dayton `166.199.7.54`. Device `d9adf1fd-…`.
- Lords Mobile 4800: Install 14:23 → Castle 5/8/10/14/18/22/25 all at **14:26:46–14:26:50** (out of order: 14 then 10 then 5 then 8). **7,825 pts**. Wallet $79.
- **CONFIRMED** impossible progression. Not peer-plausible even for a speedrun.

### 7. [3279794](https://admin.recosocial.com/users/3279794) — score **90** · Critical · High · **HOLD + FM-gate**

- **Day-0** 22:19 UTC. ID yes, **no FM**. Las Vegas T-Mobile `172.56.210.92`. Zero UUID device — do not cluster on it.
- 7 IAP **$2,020** (CA $10 + VB). $10@<span style="color:#b91c1c">10%</span>, $510@<span style="color:#b91c1c">40%</span>, $1,300@<span style="color:#b91c1c">50%</span>, $200@<span style="color:#ca8a04">100%</span>. Wallet **$1,574**. Pending **$100**.

### 8. [3284260](https://admin.recosocial.com/users/3284260) — score **88** · Critical · High · **HOLD + KYC-gate**

- **Day-0** 03:39 UTC Nov 18. Phone yes, no ID/FM. **Same IP as 2802466** `97.247.126.237`. Distinct IDFA.
- 9 Bruno IAP in 42 min **$463**: $148@<span style="color:#b91c1c">25%</span>, $200@<span style="color:#b91c1c">75%</span>, $100@<span style="color:#ca8a04">100%</span>. Wallet $305. Corroborating cluster evidence, not IP-only.

### 9. [3271386](https://admin.recosocial.com/users/3271386) — score **87** · Critical · High · **KEEP HELD + IAP restrict**

- Created 07:22 UTC (hours before window). No phone/ID/FM. Held 20:12 UTC by admin 49161. LA T-Mobile `172.58.213.151` — CGNAT, do not cluster with 1131612.
- 20 VB/CA IAP **$2,321** including **$500 after hold** (22:11). Mixed 10–100% CB. Wallet $1,158. Day-0/1 velocity.

### 10. [3260896](https://admin.recosocial.com/users/3260896) — score **86** · Critical · Medium-High · **KEEP HELD**

- Day-1. Phone yes, no ID/FM. Held 20:12. **Shares Huntsville IP `208.180.10.116` with lift-then-pay 2310003**. Distinct devices (3260896 zero UUID).
- $2,110 across **7 games** in ~11 hours, including $1,280@<span style="color:#ca8a04">100%</span>. $300 Bruno **after hold** (02:20 Nov 18). GFC dual first+any. Wallet $1,825.
- Do not treat the shared IP as conclusive alone; the day-1 7-game $2k + 100% CB + post-hold IAP is enough to keep held.

### 11. [2130088](https://admin.recosocial.com/users/2130088) — score **85** · Critical · High · **RE-HOLD + review lift process**

- Lifted 19:28:50 UTC by 49161, `removal_reason` null. Paid **$3,695.11** across 3 aged requests at 19:53:52–19:54:05 (**25 min**). Pending still **$2,606**. ID+FM Nashua. Zero UUID.
- **CONFIRMED** ops control failure (lift-then-pay). Aged KYC reduces member-fraud confidence; the process failure is the issue.

### 12. [3008799](https://admin.recosocial.com/users/3008799) — score **84** · Critical · High · **KEEP HELD + IAP restrict**

- Held since Mon 18:02. ID+FM. **All Tuesday IAP is after hold: $1,500** (Bruno/VB). **0 engine ledger bonus** — same 0-ledger pattern as 523124. On-hold payouts $768.

### 13. [3238228](https://admin.recosocial.com/users/3238228) — score **83** · Critical · High · **KEEP HELD + IAP restrict**

- Re-held Tue 05:45 UTC. ID+FM now. **$500 Bruno after hold** @ <span style="color:#b91c1c">40%</span> plus $25 GFC/Bruno. Wallet **$5,678**. On-hold $592. Recover Mon $280.

### 14. [1648850](https://admin.recosocial.com/users/1648850) — score **88** · Critical · High · **HOLD + deny pendings**

- `restrict_games`. Paid **$71.32** Tuesday. Pending **$9,829**. **CONFIRMED** control leak.

### 15. [3003760](https://admin.recosocial.com/users/3003760) — score **87** · Critical · High · **HOLD**

- C-KATY `170.203.122.23` with shells 2540180 / 2990252. Wallet **$11,172**. Pending $365. ID+FM. Do not hold aged KYC neighbors 2541251 / 2151768 / 2318930 on IP alone.

### 16. [3215995](https://admin.recosocial.com/users/3215995) — score **86** · Critical · High · **RE-HOLD + KYC-gate**

- Lifted Mon 20:58. No ID/FM. **Shares IDFA `7E776601-DDEC-4A31-8368-310B3316485D` and IP `65.59.179.38` with held 2715325**. Wallet $900. Direct shared-device evidence.

### 17. [2744123](https://admin.recosocial.com/users/2744123) — score **85** · Critical · High · **HOLD**

- McKinney `75.4.176.250` CONFIRMED dump. 14 pending **$2,666**. Wallet $476. VIP+ID+FM. Hold 2744123 only, not 1631143 / 1631163.

### 18. [3094081](https://admin.recosocial.com/users/3094081) — score **82** · Critical · High · **HOLD**

- C-HOU-D93 shell. Device **`D93FC6C3-…`** with held **2766773**, plus **1871470** and **2016791** (aged KYC — investigate recycled IDFA vs household, do not auto-hold them). No KYC. Unheld. Same IP `172.58.55.13` is T-Mobile CGNAT — device match is the signal.

### 19. [3258863](https://admin.recosocial.com/users/3258863) — score **80** · High · High · **HOLD**

- C-WESTMINSTER day-0 shell. `fraud_block`. Shared device `2ceee4fc-…` with held **2414145**. Unheld.

### 20. [3186084](https://admin.recosocial.com/users/3186084) — score **74** · High · Medium · **HOLD + KYC-gate**

- Age 6d. No phone/ID/FM. Zero UUID. Florida T-Mobile. MPL Bingo **12,500 pts** in 1 second (Win 50 cash games 16:30:39 + $25 deposit 16:30:40). MPL 16:30 batching is a known partner fingerprint, but 12.5k pts with zero KYC is still a hold. Wallet $210.

### 21. [3260675](https://admin.recosocial.com/users/3260675) — score **68** · Medium · Medium · **KYC-gate / monitor**

- Day-1. No phone/ID/FM. Indianapolis. POP Slots levels 180→500 plus $405 IAP (mostly <span style="color:#b91c1c">10–40%</span>). Fast but ordered. Wallet $157. Not impossible; missing KYC is the gap.

### 22. [3281109](https://admin.recosocial.com/users/3281109) — score **70** · High · Medium · **HOLD pendings + FM-gate**

- Day-0. ID yes, no FM. Fresno T-Mobile. Single VB **$300 @ <span style="color:#ca8a04">100%</span>**. Pending **$308**. Wallet $0.

### 23. [2251716](https://admin.recosocial.com/users/2251716) — score **72** · High · Medium · **Receipts today**

- Age 45d. ID+FM. Prior hold lifted Oct 29. Jackpot Go-heavy **$3,288** (4× ~$475 plus Backspin $500, Gleaming $482, Solitaire $200). Bonus includes <span style="color:#15803d">125%</span> on $392. Pending $2,164. Wallet $208. Concentrated in the Jackpot Go spike — partner-confirm before hold.

### 24. [3033023](https://admin.recosocial.com/users/3033023) — score **80** · Critical · High · **RE-HOLD**

- Lifted 07:37 UTC Nov 17 (before window). 4× Cider **$1,919** at 40/50%. Pending $1,009. Wallet $0. Prior 20k-pt promo CB while held. Lift-then-earn pattern continues.

### 25. [1878492](https://admin.recosocial.com/users/1878492) — score **78** · High · Medium · **Receipts + consider IAP restrict**

- VIP. ID+FM. Prior hold lifted Nov 5. Tue **$2,780** across VB/Frosty/GFC/Cider. Wallet $1,243. Pending $579. Direct high multi-game IAP; KYC reduces identity risk.

Carryover unheld (no material new Tuesday play beyond open book): **1662981** pending $7,302; **2692629** C-JAX pending $6,843; **2785102** $6,748; **2704216** $5,197; **300466** full_block pending $5,488 **DENY**; **1643885** C-ASHBURN wallet $4,746 + pending $1,400; **2723827** pending $2,837 (back on JAX IP); **2693800** wallet $506 recover leftover; **1555885** pending $2,671; **2990252** wallet $2,634 no FM; **3226358** wallet $1,147 no ID/FM; **3236809** wallet $1,557 no FM; **523124** wallet $894 0-ledger leftover; **1550037/3127296** C-OHIO shared device `212E4FA3-…`; farm shells **2478920 / 2767755 / 1184324 / 1489513**; **2762038 / 3113035** PH `fraud_block`.

Promo CB ≥10k (aged KYC, treat as monitor not hold): **1742769** 29,999 pts Call of Dragons 150% (VIP); **1645404** 20,000 VB 125% (VIP); **540547** 25,000; **2770061** 10,000 Drop the Cat 125%. **886370** 20,000 MPL bonus, ID yes / FM no.

Admin awards (clear): **408197** 80,000 / **322877** 70,000 / **512810** 70,000 Call of Dragons Power 20M. Aged, ID+FM, `admin-award-` tx ids.

---

## Part 3 — Peer and ecosystem analysis

- **Jackpot Go 4574** unique IAP $4,830 vs 7d daily $891 (**+442%**). 11 payers. **2251716** is $1,626 of that (4 large txs). Game-level spike, not a ring.
- **Victory Blast 5701** $15,384 vs 7d $14,596 (**+5%**) but **+184% vs Monday**. Day-0 **3275400 / 3279794 / 3271386 / 3281109** are outside peer (same-game, similar age) distribution. Aged VB payers (1878492, 2802466, 3008799) are high-value but KYC’d.
- **Bruno 3846** $17,429 vs 7d $35,001 (**−50%**). Cooled. 1710438’s 6×$500 is the outlier vs other Bruno payers.
- **GFC 5749** $4,002 vs 7d $3,170 (**+26%**), down from Monday $7,998. Dual first-purchase + any-purchase within 2s remains a **partner fingerprint** (2802466, 3260896, and several $3–$15 first purchases). Do not ring those accounts on the dual callback alone.
- **Call of Dragons 4520** 220,399 pts / 4 members is **admin-award**, not a fraud spike.
- **Lords Mobile 4800** 14,865 pts. The 3273825 dump is the anomaly; other members are ordinary.
- **MPL Bingo 1384** 42,700 pts / 14 members. 3186084’s same-second 12.5k is the exception; 16:30 UTC batching remains partner-side.
- Shared IP/device clusters requiring corroboration are in Part 5. T-Mobile `172.56/58/59` and Verizon `174.x` are CGNAT — not cluster keys. Zero UUID IDFA is not a cluster key.

Non-US ≥500 pts: **1** (2169597 GB, 2,000-pt hero upgrade). Immaterial.

---

## Part 4 — Risk scoring notes

Scores weight **direct IAP velocity, post-hold activity, fabricated progression, and control bypass** over VOIP/CGNAT/Verisoul. Missing KYC raises investigation priority only when paired with day-0 high value or shared device. Missing data was not used to inflate scores.

---

## Part 5 — Required tables

### Member investigation queue

Cashback color: <span style="color:#b91c1c">below 100% red</span> · <span style="color:#ca8a04">exactly 100% yellow</span> · <span style="color:#15803d">above 100% green</span>.

| Rank | User | Score | Conf | Age | 24h earn | 24h IAP | #tx | Purchase detail | Games | Evt | Signals | Cluster | Exposure | Action | Evidence needed |
| ---: | --- | ---: | --- | --- | ---: | ---: | ---: | --- | --- | ---: | --- | --- | ---: | --- | --- |
| 1 | [1710438](https://admin.recosocial.com/users/1710438) | 96 | High | 99d | — | $5,318 | 20 | $5,000@<span style="color:#b91c1c">50%</span>; $300@<span style="color:#b91c1c">40%</span>; $18@<span style="color:#b91c1c">30%</span> | JN, Bruno | 20 | **CONFIRMED** 6×$500/6min; unheld | — | $16,378 pend | Hold + recover + IAP restrict | Receipts; partner tx |
| 2 | [890126](https://admin.recosocial.com/users/890126) | 95 | High | 157d | — | $0 | 0 | — | — | 0 | **CONFIRMED** full_block paid $1,060 | — | $1,060 paid | Recover / deny future | Payment ops audit |
| 3 | [2847927](https://admin.recosocial.com/users/2847927) | 94 | High | 17d | — | $2,000 | 4 | $1,500@<span style="color:#b91c1c">50%</span>; $500@<span style="color:#b91c1c">40%</span> | GFC 5749 | 4 | C-JAX unheld; 4×$500 | C-JAX | $14,281 w+pend | Hold independently | Distinct IDFA vs 2692629/2723827 |
| 4 | [2802466](https://admin.recosocial.com/users/2802466) | 93 | High | 19d | 10,316 pts | $3,045 | 10 | $2,300@<span style="color:#b91c1c">40%</span>; $120@<span style="color:#15803d">125%</span> | CA, GFC, VB | 31 | Unheld; new Utah shell | C-UTAH | $10,352 | Hold + recover Mon $3,119 | Link review vs 3284260 |
| 5 | [3275400](https://admin.recosocial.com/users/3275400) | 92 | High | **0d** | 8,482 pts | $2,720 | 8 | $1,500@<span style="color:#b91c1c">50%</span>; $1,000@<span style="color:#b91c1c">40%</span>; $200@<span style="color:#ca8a04">100%</span> | VB | 32 | Day-0 no ID/FM | Queens-adj | $1,390 w | Hold + KYC | ID/FM; card receipts |
| 6 | [3273825](https://admin.recosocial.com/users/3273825) | 91 | High | **0d** | 7,825 pts | $0 | 0 | — | Lords 4800 | 9 | **CONFIRMED** castle 5–25 in 4s | — | $79 w | Hold | Partner callback audit |
| 7 | [3279794](https://admin.recosocial.com/users/3279794) | 90 | High | **0d** | 8,482 pts | $2,020 | 7 | $1,300@<span style="color:#b91c1c">50%</span>; $510@<span style="color:#b91c1c">40%</span>; $200@<span style="color:#ca8a04">100%</span> | VB, CA | 32 | Day-0 no FM; $100 pending | — | $1,674 | Hold + FM-gate | FaceMatch |
| 8 | [3284260](https://admin.recosocial.com/users/3284260) | 88 | High | **0d** | — | $463 | 9 | $200@<span style="color:#b91c1c">75%</span>; $148@<span style="color:#b91c1c">25%</span>; $100@<span style="color:#ca8a04">100%</span> | Bruno | 9 | Day-0 same IP as 2802466 | C-UTAH | $305 w | Hold + KYC | ID/FM |
| 9 | [1648850](https://admin.recosocial.com/users/1648850) | 88 | High | 104d | — | $0 | 0 | — | — | 0 | restrict_games paid $71 | — | $9,829 pend | Hold + deny | Control fix |
| 10 | [3003760](https://admin.recosocial.com/users/3003760) | 87 | High | 13d | — | $0 | 0 | — | — | 0 | C-KATY wallet $11,172 | C-KATY | $11,537 | Hold | Shell vs household |
| 11 | [3271386](https://admin.recosocial.com/users/3271386) | 87 | High | 0–1d | — | $2,321 | 20 | $1,000@<span style="color:#b91c1c">40%</span>; $500@<span style="color:#b91c1c">50%</span>; $350@<span style="color:#ca8a04">100%</span> | VB, CA | 20 | Held; IAP after hold | — | $1,158 w | Keep held + IAP restrict | Receipts |
| 12 | [3260896](https://admin.recosocial.com/users/3260896) | 86 | Med | 1d | — | $2,110 | 10 | $1,280@<span style="color:#ca8a04">100%</span>; $500@<span style="color:#b91c1c">60%</span> | 7 games | 10 | Held; Huntsville IP w/ 2310003 | C-HUNTS | $1,825 w | Keep held | Device vs 2310003 |
| 13 | [3215995](https://admin.recosocial.com/users/3215995) | 86 | High | 5d | — | $0 | 0 | — | — | 0 | Shared IDFA+IP with 2715325 | C-PHX | $900 w | Re-hold + KYC | ID/FM |
| 14 | [2130088](https://admin.recosocial.com/users/2130088) | 85 | High | 56d | — | $0 | 0 | — | — | 0 | Lift-then-pay $3,695 / 25 min | — | $2,606 pend | Re-hold; ops review | removal_reason policy |
| 15 | [2744123](https://admin.recosocial.com/users/2744123) | 85 | High | 24d | — | $0 | 0 | — | — | 0 | McKinney dump unheld | C-MCK | $2,666 pend | Hold 2744123 only | — |
| 16 | [3008799](https://admin.recosocial.com/users/3008799) | 84 | High | 13d | — | $1,500 | 8 | **$1,500 / 0 ledger** | Bruno, VB | 8 | IAP after hold; 0 bonus | — | $768 on_hold | Keep held + IAP restrict | Why 0 ledger |
| 17 | [3238228](https://admin.recosocial.com/users/3238228) | 83 | High | 2d | 6,763 pts | $525 | 3 | $500@<span style="color:#b91c1c">40%</span> | Bruno, GFC | 7 | $500 after hold; wallet $5,678 | — | $5,678 w | Keep held + IAP restrict | Recover Mon $280 |
| 18 | [3094081](https://admin.recosocial.com/users/3094081) | 82 | High | 11d | — | $0 | 0 | — | — | 0 | D93 shell unheld | C-HOU-D93 | $0 | Hold | vs 1871470/2016791 |
| 19 | [3033023](https://admin.recosocial.com/users/3033023) | 80 | High | 13d | 9,744 pts | $1,919 | 4 | $1,439@<span style="color:#b91c1c">50%</span>; $480@<span style="color:#b91c1c">40%</span> | Cider | 9 | Lifted then $1.9k IAP | — | $1,009 pend | Re-hold | Receipts |
| 20 | [3258863](https://admin.recosocial.com/users/3258863) | 80 | High | 1d | — | $0 | 0 | — | — | 0 | fraud_block shell; device w/ 2414145 | C-WEST | $0 | Hold | — |
| 21 | [3255293](https://admin.recosocial.com/users/3255293) | 80 | High | 1d | — | $1,502 | 16 | $1,500@<span style="color:#ca8a04">100%</span> | Bruno | 16 | Held; 15×$100@100% | — | $1,840 w | Keep held + KYC | FM |
| 22 | [1878492](https://admin.recosocial.com/users/1878492) | 78 | Med | 85d | — | $2,780 | 5 | $980@<span style="color:#b91c1c">50%</span>; $500@<span style="color:#b91c1c">30%</span> | VB, Frosty, GFC, Cider | 5 | VIP multi-game IAP | — | $1,822 | Receipts | Partner confirm |
| 23 | [3186084](https://admin.recosocial.com/users/3186084) | 74 | Med | 6d | 12,500 pts | $0 | 0 | — | MPL Bingo | 2 | 12.5k pts 1s, no KYC | — | $210 w | Hold + KYC | MPL partner |
| 24 | [2251716](https://admin.recosocial.com/users/2251716) | 72 | Med | 45d | — | $3,288 | 8 | $1,462@<span style="color:#b91c1c">40%</span>; $1,434@<span style="color:#b91c1c">50%</span>; $392@<span style="color:#15803d">125%</span> | JG, Backspin, Gleaming | 8 | Jackpot Go spike driver | — | $2,372 | Receipts today | Partner JG |
| 25 | [3281109](https://admin.recosocial.com/users/3281109) | 70 | Med | **0d** | — | $300 | 1 | $300@<span style="color:#ca8a04">100%</span> | VB | 1 | Day-0 100% CB | — | $308 pend | Hold pending + FM | FaceMatch |

### Game and ecosystem anomaly

| Game | 24h members | Events | Points | IAP amt / count | vs 7d IAP | Flagged | Main anomaly | Exposure | Action |
| --- | ---: | ---: | ---: | --- | --- | ---: | --- | ---: | --- |
| Victory Blast 5701 | 1,647 | 2,118 | 81,023 | $15,384 / 187 | **+5%** (vs Mon **+184%**) | 6 | Day-0 $2.7k/$2.0k; recovered vs Mon | ~$8k flagged IAP | Watch; hold day-0 no-KYC |
| Jackpot Go 4574 | — | — | — | $4,830 / 43 | **+442%** | 1 | 2251716 concentration | $3,288 | Partner confirm; do not pause |
| Bruno 3846 | 2,255 | 4,840 | 95,195 | $17,429 / 283 | **−50%** | 5 | 1710438 6×$500; 3284260 day-0 | $5.3k+$0.5k | Watch 1710438; do not pause |
| GFC 5749 | — | — | — | $4,002 / 66 | **+26%** (vs Mon −50%) | 3 | Dual first+any fingerprint; 2847927 4×$500 | $2,000 | Watch; partner fingerprint |
| Jackpot Nights 4767 | 358 | 509 | 50,172 | $4,643 / 63 | **−46%** | 1 | 1710438 3×$500 | $1,800 | Cooled vs Mon |
| Jackpot Nights 2916 | — | — | — | $5,216 / 211 | **−52%** | 2 | 3266164 $500 while later held | $500 | Cooled |
| Cider 5714 | 161 | 218 | 28,616 | $2,947 / 27 | **+35%** | 1 | 3033023 4×$480 after lift | $1,919 | Watch 3033023 |
| Call of Dragons 4520 | 4 | 4 | 220,399 | $0 | n/a | 0 | Admin-award Power 20M | $2,200 pts $ | Ops, not fraud |
| Lords Mobile 4800 | 166 | 329 | 14,865 | — | n/a | 1 | 3273825 4-second castle dump | 7,825 pts | Partner audit |
| MPL Bingo 1384 | 14 | 16 | 42,700 | — | n/a | 1 | 3186084 12.5k same-second | 12,500 pts | KYC-gate; partner batch |
| Gleaming 4701 | 741 | 837 | 16,679 | $3,401 / 52 | **−10%** | 1 | Promo CB cooled (4 ≥10k vs 10) | — | No pause |
| Tang 4815 | 284 | 691 | 18,417 | $2,951 / 44 | **+7%** | 1 | 2905497 $1,390 leftover | $1,390 | Receipts |
| Frogs 5724/5726 | 941+1,154 | 1,105+1,343 | 53k+29k | $1,758+$1,222 | n/a | 0 | Loc 99/106/113 did not fire | — | Monitor |
| Spin Arena 2565 | not in top IAP | — | — | cooled | n/a | 0 | 523124 leftover idle | — | No pause |

Do **not** pause Bruno, JN, VB, GFC, Tang, Cider, Frogs, Gleaming, or Spin Arena. Temporarily **watch** Jackpot Go 4574 and day-0 VB.

### Linked-account clusters

| Cluster | Members | Shared IDs | Game/event | Purchases | Timeline | Exposure | Related? | Alt explanation | Action |
| --- | --- | --- | --- | --- | --- | ---: | --- | --- | --- |
| C-UTAH **NEW** | 2802466, 3284260 | IP `97.247.126.237` | Bruno/VB/GFC | Day-0 $463 + aged $3,045 | 3284260 created 03:39 UTC during 2802466 session | ~$10.7k | **High** (IP + timing; distinct devices) | Household / NAT | Hold both independently |
| C-JAX | 2847927, 2692629, 2723827 | IP `24.129.83.23` | GFC | 2847927 $2,000 | 2723827 **returned** to IP | ~$24k | Med-High per account | Shared ISP | Hold each; do not mass-hold IP |
| C-HUNTS **NEW** | 2310003, 3260896 | IP `208.180.10.116` | multi-game | 3260896 $2,110 | 2310003 lift-then-pay Mon; 3260896 day-1 | $1.8k + paid $3,914 | Med | Household | Keep 3260896 held; receipts 2310003 |
| C-PHX | 3215995, 2715325 | IDFA `7E776601-…` + IP `65.59.179.38` | — | leftover | 3215995 still lifted | $900+$7,167 on_hold | **High** | Recycled IDFA unlikely (same IP) | Re-hold 3215995 |
| C-HOU-D93 | 2766773 held, 3094081, 1871470, 2016791 | IDFA `D93FC6C3-…` | — | leftover | 4 accounts on device | $16,438 on_hold | High for shells | Recycled IDFA for 1871470/2016791 (aged KYC) | Hold 3094081; investigate KYC pair |
| C-KATY | 3003760, 2990252, 2540180 | IP `170.203.122.23` | leftover | leftover | 3236809 left | $14k+ | Med | Household + CGNAT | Hold 3003760 + KYC-gate shells; not 2541251/2318930 |
| C-MCK | 2744123, 1631143, 1631163 | IP `75.4.176.250` | leftover | leftover | dump | $2,666 | High for 2744123 | Aged KYC 1631143 | Hold 2744123 only |
| C-WEST | 2414145 held, 3258863, 2762038, 3113035 | device `2ceee4fc` / PH IP | leftover | leftover | fraud_block | low $ | High for shells | — | Hold unheld shells |
| C-OHIO | 1550037, 3127296 | IDFA `212E4FA3-…` | leftover | leftover | still unheld | $331 pend | High | Household | Hold both |
| Farm 9E0B6081 | 2311904 held, 2393325 held, shells 2478920/2767755/1184324/1489513 | IDFA `9E0B6081-…` | idle | idle | idle | $2,028 w on 2393325 | High | — | Hold remaining shells |
| GFC duals | several | callback fingerprint | first+any <2s | small $ | partner | n/a | **Not a member ring** | Partner batch | Do not hold on fingerprint alone |

---

## Part 6 — Operational action plan

### Immediately hold or restrict

**1710438** (6×$500/6min, $16.4k pending) · **2847927** · **2802466** · **3275400** · **3279794** · **3284260** · **3273825** · **3215995** · **3003760** · **2744123** · **3033023** · **3197354** · **2260308** · **2310003** · **2726598** · **1662981** · **2692629** · **2785102** · **2704216** · **1643885** · **2723827** · **1648850** · **300466** (deny) · **890126** (recover) · shells **3094081, 3258863, 2762038, 3113035, 2478920, 2767755, 1184324, 1489513, 2540180, 2990252**.

Cite: direct IAP velocity, shared device/IDFA, day-0 high IAP without KYC, control-status payouts, or previously confirmed dump/cluster membership. No hold is based on CGNAT or VOIP alone.

### Keep held / IAP restrict

**3008799** ($1,500 after hold, 0 ledger) · **3238228** · **3271386** · **3260896** · **3255293** · **3249692** · **3266164** · **2766773** · **2414145** · **2715325** · **2810500** · **2933198** · **3107354** · **3134345** · **3184070** · **3107598** · **3152065** · **2976221, 2861750, 2846635, 2952917, 2878241, 2763049, 2311904, 2393325**.

### Manually investigate today

**2251716** Jackpot Go spike · **1878492** VIP $2,780 · **3186084** MPL 12.5k · **3260675** POP day-1 · **1871470 / 2016791** on D93 IDFA · **2130088** lift process · **2905497** Tang receipts · **1550037/3127296** C-OHIO.

### Request receipts / IDFA / ID / partner confirmation

VIP **415661, 1183307, 1577219**. **2251716** Jackpot Go. **3281109** FaceMatch. Partner: Jackpot Go 4574 spike, Lords Mobile 3273825 callback, MPL 3186084, GFC dual fingerprint (not a ring).

### Monitor without action

Promo CB VIPs 1742769 / 1645404 / 2770061. Admin-award CoD 408197 / 322877 / 512810. GFC dual $3–$15 first purchases. Non-US 2169597. Bruno/JN cooling.

### Clear as likely legitimate

Admin-award Power 20M to aged KYC VIPs. Do not hold **2541251 / 2151768 / 2318930** on Katy IP. Do not hold **2035175** on stale Ashburn IDFA. Do not mass-hold T-Mobile CGNAT neighbors on `172.58.55.13`.

### Queries / checks next

1. Confirm holds actually persist (prior lifts by 49161 with null `removal_reason`).
2. After-hold IAP job: completions with `iapUsd>0` where `completion_timestamp` > `payout_hold_metadata.held_at`.
3. Partner pull for Lords Mobile 3273825 and Jackpot Go 2251716.
4. Device history for 3284260 vs 2802466 (current IP match only).
5. Why 3008799 / 523124 IAP have 0 `iap_marketing_engine_multiplier` ledger rows.
6. Open `full_block` / `restrict_games` / `fraud_block` pendings still confirmable.

### Missing data

Purchase receipts; IDFA/GAID time series (only `most_recent_device_id`); FaceMatch for day-0; partner settlement vs callback; SIM-swap (key exists but `recent_swap` historically false); wallet vs pending double-count risk.

### Rule / alert changes

1. Never confirm a payout within 15 minutes of a hold lift; require `removal_reason`.
2. `full_block` + `payout_hold` + `fraud_block` + `verisoul_block` + `restrict_games` must stop **IAP, promo CB, completions, and payout confirmation**.
3. Alert: ≥6 unique IAP ≥$500 in 20 min (hit: 1710438).
4. Alert: day-0 IAP ≥$300 and day-0 75%+ / 100% engine CB (hit: 3275400, 3279794, 3281109, 3284260).
5. Alert: IAP ≥$500 on currently held accounts (hit: 3008799, 3238228, 3271386).
6. Alert: same-second multi-milestone dump (Lords 3273825).
7. Alert: new account on watched IPs (Utah `97.247.126.237`, JAX `24.129.83.23`, Katy `170.203.122.23`, Hou `172.58.55.13`, Huntsville `208.180.10.116`, PHX `65.59.179.38`, Westminster device `2ceee4fc`).
8. Alert: 0 ledger bonus on ≥$500 unique IAP (3008799, 523124).

### Games / campaigns to watch (do not pause)

Watch **Jackpot Go 4574** and **day-0 Victory Blast**. Continue watching GFC 5749 dual callbacks. Do not pause Bruno/JN/VB/Gleaming/GFC/Tang/Cider/Frogs/Spin Arena.

### What changed since yesterday (Mon 11/16)

- Members +8%, events +9%, unique IAP +25% ($76.8k → $95.8k). Points +5% but **−14%** excluding 340,696 admin-award pts.
- **Worse:** 1710438 still unheld and re-hit 6×$500; 890126 full_block **paid**; 2130088 lift-then-pay $3.7k; day-0 VB whales 3275400/3279794; new C-UTAH shell 3284260; Lords dump 3273825; 2723827 back on JAX IP; hold-now IAP leak $4.6k → ~$10k event-sum; 3008799 $1,500/0-ledger after hold.
- **Better:** 3266164 / 3271386 / 3260896 / 3255293 / 3249692 / 1720260 now held; Bruno still −50% vs 7d; promo CB ≥10k 10→4; duplicate tx 0; reversals 0; no loc 113; GFC cooled vs Monday; 300466 did not pay; only 1 hold lift vs 7.
- Open book $673k → $667k. Confirmed payouts $105k Mon → $80k Tue.

---

*Generated 2026-11-18 15:00 UTC from read-only Postgres. Session TZ is UTC; PT midnight after DST is 08:00 UTC.*
