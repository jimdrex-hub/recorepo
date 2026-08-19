-- Reference SQL used for the fraud-triage 72h report.
-- Every query includes LIMIT. Window timestamps are filled at run time (PT).

-- 1) Qualifying purchases (+24h buffer for consecutive-day detection)
-- Confirmed IAP USD from webhook_data->>'iapUsd'; exact linked bonus multiplier < 1.0
SELECT
  mgec.id AS event_id,
  mgec.user_profile_id,
  mgec.mobile_game_id,
  mgec.created_at AS event_at,
  (mgec.webhook_data->>'iapUsd')::numeric AS iap_usd,
  (mgec.meta->'bonus_consumption'->'iap_bonus'->>'bonusId')::bigint AS bonus_id,
  COALESCE(
    (ub.bonus_data->>'multiplier')::numeric,
    (ub.bonus_data->'dbaAction'->>'multiplier')::numeric
  ) AS multiplier
FROM mobile_game_event_completions mgec
JOIN user_bonuses ub
  ON ub.id = (mgec.meta->'bonus_consumption'->'iap_bonus'->>'bonusId')::bigint
WHERE mgec.created_at >= TIMESTAMP '2026-08-15 06:03:00'  -- buffer start (UTC)
  AND mgec.created_at <  TIMESTAMP '2026-08-19 06:04:00'  -- window end
  AND (mgec.webhook_data->>'iapUsd')::numeric >= 19.99
  AND COALESCE(
    (ub.bonus_data->>'multiplier')::numeric,
    (ub.bonus_data->'dbaAction'->>'multiplier')::numeric
  ) < 1.0
ORDER BY mgec.created_at DESC
LIMIT 5000;

-- 2) Profiles for cohort member IDs
SELECT id, status, COALESCE(payout_hold,false) AS payout_hold,
       game_blocked_reason, COALESCE(is_internal_user,false) AS is_internal_user,
       phone_verified, id_verified, registration_risk_score,
       registration_risk_action, phone_intelligence
FROM user_profiles
WHERE id = ANY(ARRAY[/* cohort ids */]::int[])
LIMIT 500;

-- 3) Latest Verisoul assessment
WITH latest AS (
  SELECT DISTINCT ON (user_profile_id)
    user_profile_id, decision, account_score, bot, multiple_accounts,
    risk_signals, accounts_linked, assessment_type, created_at
  FROM verisoul_assessments
  WHERE user_profile_id = ANY(ARRAY[/* cohort ids */]::int[])
  ORDER BY user_profile_id, created_at DESC
)
SELECT * FROM latest LIMIT 300;

-- 4) Latest payout-risk assessment
WITH latest AS (
  SELECT DISTINCT ON (user_profile_id)
    user_profile_id, risk_score, risk_action, signals, created_at
  FROM payout_risk_assessments
  WHERE user_profile_id = ANY(ARRAY[/* cohort ids */]::int[])
  ORDER BY user_profile_id, created_at DESC
)
SELECT * FROM latest LIMIT 300;

-- 5) Game earnings in the same 72h window (filter allowlist titles in application code)
SELECT
  l.user_profile_id AS user_id,
  COALESCE(NULLIF(TRIM(mg.name), ''), 'Unknown') AS game_name,
  DATE((l.created_at AT TIME ZONE 'UTC') AT TIME ZONE 'America/Los_Angeles') AS earn_date_pt,
  (SUM(l.points) * 0.01)::numeric(14,2) AS earnings_usd,
  COUNT(*)::int AS credit_events
FROM ledger_entries l
JOIN mobile_game_event_completions mgec ON mgec.id = l.game_event_completion_id
JOIN mobile_games mg ON mg.id = mgec.mobile_game_id
WHERE l.user_profile_id = ANY(ARRAY[/* cohort ids */]::int[])
  AND l.entry_kind = 'credit'
  AND l.earning_type = 'game'
  AND l.created_at >= TIMESTAMP '2026-08-16 06:03:00'
  AND l.created_at <  TIMESTAMP '2026-08-19 06:04:00'
GROUP BY 1, 2, 3
ORDER BY 4 DESC
LIMIT 5000;
