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
   - Checks the leading signals: overnight global XAU/USD move since the Thai close, USD/THB direction, and today's macro calendar.
   - Pulls views from 3 well-known gold sources (mix of global and Thai).
   - Checks whether each source's predictions over the past 3 days were correct.
3. **SYNTHESIZE** — Concludes whether gold today is likely to go UP or DOWN, weighting the overnight global move highest and each source by its recent accuracy.
4. **DELIVER**
   - Writes a dated Markdown report to `reports/YYYY-MM-DD.md` and commits it.
   - Sends a LINE push notification with four sections (Prediction, Agent Performance, Source Views, Key Reasons); Source Views and Key Reasons are written in Thai.

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

**Leading-signal check (strongest predictors — check these BEFORE reading opinions)**
Thailand's GTA price is largely a mechanical function of two inputs. Check both:
1. **Overnight global move** — what has XAU/USD done since yesterday's Thai close
   (~17:30 Bangkok time)? The Thai open almost always gaps in the direction of the
   overnight global move. Record the current live spot level and % change vs the
   level at yesterday's Thai close.
2. **USD/THB direction** — a strengthening baht offsets global gains (and vice
   versa). Record today's USD/THB level and direction vs yesterday.

Also check **today's macro calendar** (Bangkok time): FOMC decision/minutes, NFP,
CPI, major Fed speakers, or significant geopolitical events scheduled today. A
high-impact event landing during or after Thai trading hours can invalidate a
morning call — if one is scheduled, note it and lower confidence one notch.

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

Combine the signals in this priority order:
1. **Overnight global XAU/USD move since yesterday's Thai close** — the single
   strongest predictor of the Thai session's direction. Weight it highest.
2. **USD/THB direction** — adjust the global signal for baht strength/weakness.
3. **Source consensus, weighted by trailing accuracy** — weight each source's view
   by its own 3-day accuracy record from Phase 2. A source that has been wrong
   3 days running should barely move the needle; a source that has been right
   3 days running deserves real weight. Ignore week-ahead views when making a
   today-only call unless nothing fresher exists.
4. **Macro calendar risk** — if a high-impact event lands during/after Thai hours
   today, cap confidence at Medium.

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

Build the `<summary>` text (≤ 4,500 characters — LINE's hard limit per text
message is 5,000) using this template. It mirrors the report's four main
sections. **The 🔍 Source Views and 💡 Key Reasons sections must be written in
Thai**; the rest stays in English:
```
🪙 Thailand Gold — Today's Prediction YYYY-MM-DD

📌 Today's Prediction
Direction: ▲ UP / ▼ DOWN / ➡ SIDEWAYS
Confidence: High/Medium/Low

<2-3 sentence reason focused on what gold will do TODAY>

📊 Agent Performance (Past 3 Days)
Day-3 YYYY-MM-DD: Predicted <UP/DOWN/SIDEWAYS> → Actual <▲ UP / ▼ DOWN / ➡ SIDEWAYS / 🏖> (<change detail>) <✅/❌/🏖>
Day-2 YYYY-MM-DD: Predicted <UP/DOWN/SIDEWAYS> → Actual <▲ UP / ▼ DOWN / ➡ SIDEWAYS / 🏖> (<change detail>) <✅/❌/🏖>
Day-1 YYYY-MM-DD: Predicted <UP/DOWN/SIDEWAYS> → Actual <▲ UP / ▼ DOWN / ➡ SIDEWAYS / 🏖> (<change detail>) <✅/❌/🏖>

🔍 มุมมองจากแหล่งข่าว
1) YLG Bullion: <สรุปคาดการณ์วันนี้ 1-2 บรรทัด เป็นภาษาไทย>
   ความแม่นยำ 3 วัน: <✅/❌/🏖/❓> <✅/❌/🏖/❓> <✅/❌/🏖/❓>
2) สมาคมค้าทองคำ: <สรุป 1-2 บรรทัด เป็นภาษาไทย>
   ความแม่นยำ 3 วัน: <✅/❌/🏖/❓> <✅/❌/🏖/❓> <✅/❌/🏖/❓>
3) <ชื่อแหล่งข่าวต่างประเทศ>: <สรุป 1-2 บรรทัด เป็นภาษาไทย>
   ความแม่นยำ 3 วัน: <✅/❌/🏖/❓> <✅/❌/🏖/❓> <✅/❌/🏖/❓>

💡 เหตุผลสำคัญ
• <เหตุผลข้อ 1 เป็นภาษาไทย>
• <เหตุผลข้อ 2 เป็นภาษาไทย>
• <เหตุผลข้อ 3 เป็นภาษาไทย>
(3-5 ข้อ แปลจาก Key Reasons ในรายงาน — เขียนให้กระชับ อ่านง่ายบนมือถือ)

Sources: YLG · GTA · <global>
```

Where `<change detail>` is a short note like `+850 baht to 63,900` or `−1,300 baht to 63,050` or `Market Closed`.

Keep technical terms that are clearer in English (XAU/USD, DXY, FOMC, NFP,
Fed) as-is inside the Thai text — translate the explanation, not the jargon.

In the LINE message, write Thai gold prices as e.g. `65,400 บาท` — use the
word `บาท` only, never `บาทละ`. (The full unit `บาทละ` is fine in the Markdown
report, just not in the LINE message.)

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
