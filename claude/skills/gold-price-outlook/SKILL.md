# gold-price-outlook

Daily Thailand gold-price research, analysis, and LINE notification skill.

## Trigger

Invoke with `/gold-price-outlook` or when asked to run the daily gold price routine.

## Required Environment Variables

| Variable | Description |
|---|---|
| `LINE_ACCESS_TOKEN` | LINE Messaging API channel access token |
| `LINE_USER_ID` | LINE user ID to receive the push notification (`Uxxxxxxxxx…`) |

Never hardcode these values. Never write them to a `.env` file.

## What the skill does

1. **RESEARCH** — Searches the web for today's Thailand gold price prediction/outlook (YLG, Gold Traders Association, major Thai financial news).
2. **ANALYZE**
   - Compares yesterday's Thailand gold price vs yesterday's global (spot XAU/USD) price and states whether they moved in alignment.
   - Pulls views from 3 well-known gold sources (mix of global and Thai).
   - Checks whether each source's predictions over the past 3 days were correct.
3. **SYNTHESIZE** — Concludes whether gold today is likely to go UP or DOWN with concise reasons and reference links.
4. **DELIVER**
   - Writes a dated Markdown report to `reports/YYYY-MM-DD.md` and commits it.
   - Sends a LINE push notification via a direct HTTPS POST (no shell script).

## Skill instructions

<instructions>
You are running the daily Thailand gold-price outlook workflow. Follow each phase strictly.

### Phase 1 — RESEARCH

Search the web for:
- Today's Thailand gold price forecast / outlook (use Thai and English queries).
- Gold Traders Association of Thailand (สมาคมค้าทองคำ) latest price announcement.
- YLG Bullion & Futures daily gold outlook for **today** specifically.
- Any major Thai financial news gold articles published today.

Record every source URL you find.

### Phase 2 — ANALYZE

**Price alignment check (yesterday's facts)**
- Find yesterday's closing Thailand gold price (baht/baht-weight, i.e. บาทละ).
- Find yesterday's closing global spot gold price (XAU/USD).
- State explicitly: did they move in the same direction vs the day before?
- If yesterday was a market holiday or weekend, note "Market Closed" instead of a price.

**Three-source view collection**
Collect each source's prediction for **today** (not the coming week) — at least one Thai, at least one global:
1. YLG Bullion (Thai) — https://ylg.co.th
2. Gold Traders Association of Thailand — https://goldtraders.or.th
3. One global source: World Gold Council, Kitco, Reuters Gold, or Bloomberg Commodities.

For each source, also check what they predicted for the previous 3 days and whether the actual price movement that day confirmed or contradicted the prediction. Summarise each as ✅ Correct, ❌ Wrong, ❓ Unclear, or 🏖 Market Closed.

**Agent self-performance check**
Read the last 3 daily report files from the `reports/` folder (e.g. `reports/YYYY-MM-DD.md` for Day-3, Day-2, Day-1 relative to today). For each:
- Extract the **Direction** this skill predicted on that day (UP / DOWN / SIDEWAYS).
- Find the **actual Thailand gold price movement** for that day (vs the prior trading day).
- Score as ✅ Correct, ❌ Incorrect, 🏖 Market Closed, or ❓ Unclear.

If a report file does not exist for a given day (e.g. weekend or missed run), mark as 🏖 Market Closed or ❓ No report.

### Phase 3 — SYNTHESIZE

The direction call must answer: **"What will Thailand gold do TODAY (YYYY-MM-DD)?"**
Write a SHORT conclusion (≤ 5 bullet points):
- Overall direction call for today: **UP** or **DOWN** (or SIDEWAYS if truly unclear).
- Key supporting reasons (price level, trend, macro drivers relevant to today).
- Confidence level: High / Medium / Low.
- List source links used.

### Phase 4 — DELIVER

**4a — Write the report**

Create the file `reports/YYYY-MM-DD.md` (use today's actual date).

Report structure:
```
# Thailand Gold Price Outlook — YYYY-MM-DD

## Today's Prediction
**Direction: ▲ UP / ▼ DOWN / ➡ SIDEWAYS** | Confidence: High/Medium/Low

<one-paragraph summary of what gold is expected to do TODAY and why>

## Agent Performance (Past 3 Days)
| Day | Date | My Prediction | Actual Move | Result |
|---|---|---|---|---|
| Day-3 | YYYY-MM-DD | UP/DOWN/SIDEWAYS | ▲ UP / ▼ DOWN / ➡ SIDEWAYS / 🏖 Market Closed | ✅/❌/🏖/❓ |
| Day-2 | YYYY-MM-DD | UP/DOWN/SIDEWAYS | ▲ UP / ▼ DOWN / ➡ SIDEWAYS / 🏖 Market Closed | ✅/❌/🏖/❓ |
| Day-1 | YYYY-MM-DD | UP/DOWN/SIDEWAYS | ▲ UP / ▼ DOWN / ➡ SIDEWAYS / 🏖 Market Closed | ✅/❌/🏖/❓ |

## Price Alignment (Yesterday)
| Metric | Value | Change |
|---|---|---|
| Thailand gold (บาทละ) | … | ▲/▼ … or 🏖 Market Closed |
| Global spot XAU/USD | … | ▲/▼ … or 🏖 Market Closed |
| Alignment | Yes / No / N/A | |

## Source Views
### 1. YLG Bullion
- Today's prediction: …
- 3-day accuracy: Day-3 ✅/❌/🏖/❓ · Day-2 ✅/❌/🏖/❓ · Day-1 ✅/❌/🏖/❓

### 2. Gold Traders Association of Thailand
- Today's prediction: …
- 3-day accuracy: …

### 3. <Global source name>
- Today's prediction: …
- 3-day accuracy: …

## Key Reasons
- …

## References
- [Source name](URL)
```

**4b — Write the report file to disk**

Write the completed report content to `reports/YYYY-MM-DD.md` using the Write
tool (or equivalent file-write). Do NOT run any git commands manually — the
script in step 4c handles commit, push, and LINE in one call.

**4c — Commit, push, and send LINE notification**

Build the `<summary>` text (≤ 1000 characters) using this template:
```
🪙 Thailand Gold — Today's Prediction YYYY-MM-DD
Direction: ▲ UP / ▼ DOWN / ➡ SIDEWAYS
Confidence: High/Medium/Low

<2-3 sentence reason focused on what gold will do TODAY>

📊 Agent Performance (Past 3 Days)
Day-3 YYYY-MM-DD: Predicted <UP/DOWN/SIDEWAYS> → Actual <▲ UP / ▼ DOWN / ➡ SIDEWAYS / 🏖> (<change detail>) <✅/❌/🏖>
Day-2 YYYY-MM-DD: Predicted <UP/DOWN/SIDEWAYS> → Actual <▲ UP / ▼ DOWN / ➡ SIDEWAYS / 🏖> (<change detail>) <✅/❌/🏖>
Day-1 YYYY-MM-DD: Predicted <UP/DOWN/SIDEWAYS> → Actual <▲ UP / ▼ DOWN / ➡ SIDEWAYS / 🏖> (<change detail>) <✅/❌/🏖>

Sources: YLG · GTA · <global>
```

Where `<change detail>` is a short note like `+850 baht to 63,900` or `−1,300 baht to 63,050` or `Market Closed`.

Then run this single command — it commits and pushes the report file AND sends
the LINE notification in one step:
```
python3 claude/skills/gold-price-outlook/send_line.py "<summary>" --report-file reports/YYYY-MM-DD.md
```

The script will:
1. `git add` the report file, commit it, and push to `origin/main` (retries up to 3×).
2. POST the summary to LINE via `https://api.line.me/v2/bot/message/push`.

It reads `LINE_ACCESS_TOKEN` and `LINE_USER_ID` from environment variables.
If those are missing, the git commit+push still runs and an error is printed
for the LINE step — the report is never lost.
</instructions>
