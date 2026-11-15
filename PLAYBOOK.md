# Current Cove — autonomous YouTube Shorts playbook

You are running Nancy's YouTube channel (Current Cove) on her behalf. Runs fire 6 times a day (~06:40, 09:40, 11:40, 14:40, 16:40, 19:40 IST). Each run: make **1 original Short** and schedule them on YouTube through the Metricool connector. Nancy is not watching and has said she wants zero involvement: never ask for permission or confirmation, never stop for approval. Decide, upload, report. Decide, do the work, and report at the end.

## 0. Setup (every run starts in a fresh container)
```
git clone --depth 1 https://github.com/nancy8580/currentcove-media ~/ccm   # if not already present
mkdir -p ~/fonts && cp ~/ccm/tools/fonts/* ~/fonts/
cd ~/ccm/tools/geo && npm i d3-geo@3.1.0 topojson-client@3.1.0 world-atlas@2.0.2 >/dev/null
node -e "const fs=require('fs');fs.writeFileSync('world.js','export default '+fs.readFileSync('node_modules/world-atlas/countries-110m.json'))"
```
Chromium/Playwright are pre-installed (`/usr/bin/google-chrome`). Python has numpy, PIL and matplotlib. If something is missing, pip install it with `--break-system-packages`.

## 1. Pick 1 topic
**Current winner (14 Nov data):** the Delhi→New York flight-route map Short got 1.3K views in its first ~80 minutes, the channel's fastest start. Until the Sunday review says otherwise, 2 of every 6 daily Shorts are "map that surprises you" topics in the same visual style (globe/map animation, glowing route or line, one big number). Ideas: why flights to the US go over the Arctic (done; don't repeat), why planes avoid the Pacific, why Tibet has no flights over it, why Russia has 11 time zones, why the equator line in maps lies, Africa vs Greenland sizes, why ships avoid the straight route around Somalia.
- Read `log/published.json`. Never repeat a topic.
- Rotate between these formats, and never use the same format as the previous Short in the log:
  1. **Curious maps / geography** (map projections, odd borders, time zones, flight routes, why X is where it is)
  2. **How it works** (everyday tech and systems: UPI, OTP, GPS, elevators, ATMs, train signalling)
  3. **Science "why" facts** (why the sky is blue, why ice floats, why planes don't fly over the Pacific)
  4. **History mysteries and true stories** (non-graphic, no recent tragedies)
  5. **India curiosities** (why Indian Railways…, why ₹ notes…, why IST is +5:30)
- The hook must be a question a 15-year-old would want answered within 2 seconds.
- **Never** cover: elections, politicians, religion, communal topics, recent deaths or tragedies, medical advice, finance tips, or anything needing breaking-news accuracy. Evergreen only.

## 2. Research and fact-check
- Use WebSearch/WebFetch. Every number on screen needs a source. Compute what you can yourself (distances, ratios), as `tools/geo/calc.mjs` does.
- If you can't verify a claim, cut it.

## 3. Script (25–45 s total; shorter beats longer if the story allows)
- 5–7 scenes. Each scene is one narration line of 1–2 sentences.
- Scene 1 is the hook: one sentence, under 2.5 s of voice, no warm-up ("Let's talk about…", "Did you know…" are banned). State the most surprising thing first.
- No separate outro scene. The last line pays off the hook and flows back into the first line so the Short loops. A small "Follow @currentcove_" text overlay on the last 1.5 s is enough.
- Tone: curious, warm, conversational, simple English, Indian audience.

## 4. Voiceover (Speko MCP)
`mcp__Speko__audio_synthesize` with body:
`{"text": LINE, "intent": {"language":"en","region":"IN","optimizeFor":"accuracy"}, "voice": "en-IN-Dhruv:MAI-Voice-2.1", "constraints": {"allowedProviders":{"tts":["azure"]}}, "instructions": "Curious, warm, upbeat explainer, like telling a friend a cool fact.", "speed": 1}`
Make one call per scene, in parallel. Each result saves a wav under `~/.claude/projects/.../tool-results/`; copy those files to `vo/v{i}.wav` in scene order. Trim each with `tools/tight.py` (`tighten(a, sr, cap=.4)`). Scene duration = voice length + 0.7 s (+1.6 s on the last scene). Write `vo/voice.wav` and `vo/timing.json` the same way `tools/geo/geo.html` + `render.py` expect: `{"SC": [[id, start, end, voiceDur, text], ...], "TOTAL": T}`.

## 5. Animation (the core: must be real motion, not slides)
- Write a new single-file canvas animation per Short, modelled on `tools/geo/geo.html` (maps and globes with d3-geo) or `tools/ride/anim.html` (city, diagrams, moving objects). Copy the closest one and rewrite the scenes for your topic.
- Requirements: 1080×1920; dark background (#06101f-ish); one accent colour; something moving in every frame; a big headline at the top for each scene; burned-in subtitle chunks (6 words) near the bottom (y≈1600); `CURRENT COVE · <SERIES>` label at the top and `@currentcove_` at the bottom; deterministic `window.frame(t)`.
- Guard every `arc()` radius with `Math.max(0.01, r)`. Easing-overshoot curves can go negative at t=0 and crash the render.
- Render stills first (`render.py --stills`), make a contact sheet, and **look at it with Read**. Fix overlapping text, empty frames and unreadable labels before the full render.
- No real people's photos, no logos, no copyrighted characters or art.

## 5a. Editing styles — rotate, never the same look twice in a row
Pick the style that fits the topic, and never repeat the previous Short's style (check `style` in the log).
1. **Desk of documents** (`tools/desk/desk.html`, Nancy's favourite): cream paper desk, props sliding/dropping in with shadows, rubber stamps slamming, charts drawing themselves, highlighter sweeps, swinging price tags, red full-screen "STEP N" cards with whip transitions, serif word-by-word captions with one red keyword, SFX on every action (`tools/desk/sfx.py`, events exported by `getSFX()`). Best with a "Step 1, Step 2…" or "how they did it" script, sly narrator tone. Rewrite the `S` scene functions per topic; vary the palette (e.g. green ledger, blue blueprint, newsprint grey) and props so it never looks identical.
2. **Curious maps** (`tools/geo/geo.html`): dark navy, animated globe/map, glowing routes, one big number.
3. **Scrapbook collage**: torn-paper cut-outs, tape, polaroid frames, marker scribbles, fast pop-in.
4. **Kinetic type**: huge words slamming in on the beat, screen shakes, colour flashes, zoom punches.
5. **Blueprint / diagram**: grid paper, line drawings that draw themselves, callout arrows, measurements.
6. **OSINT investigation** (`tools/osint/osint.html`; needs `world50.js` built like world.js from countries-50m.json): near-black map zooming world→city, white pins with mono labels, dashed yellow routes, terminal data panels typing in, yellow highlighter on key facts, calm journalist narration. Great for journeys and timelines.
7. **Night-lights cinematic map**: 3–5 s line-art/wireframe opening scene with glowing particles, then a dark map with orange city-light glow, cream paper data cards with big red serif numbers pinned by leader lines, dashed trade routes, serif captions with a red keyword. For economics, trade and energy chain-reaction stories (evergreen only, no live wars).
Every style: something changes every ~1 s, sudden cuts and whip-pans instead of fades, sound effect on each hit.

## 5b. Retention rules (from the YouTube growth skill)
- Frame 1 is the most dramatic visual of the video, fully drawn: no fade-in from black, no empty map. The viewer decides in the first second.
- Something changes on screen at least every 1.5–2 s: a zoom, a label popping in, an arrow, a counter, a highlight.
- Add 3–6 sound effects (whoosh on transitions, pop on labels, tick on counters, low hit on the reveal). Generate them with numpy; keep them under the voice.
- Captions: max 2 colours (white + the accent), thin dark backing, no emoji, 4–6 words per chunk, never covering the key visual.
- Quality gate: if the stills don't look clearly better than the previous Short, fix or pick another topic. A skipped slot is better than a weak upload, because weak uploads lower the channel's trust score.

## 6. Mix and encode
- Music: `python3 tools/music/gen_synth.py <secs> music.wav "<unique seed: date+topic>"`. Never reuse a seed.
- Mix the voice over the music with ducking (see the ffmpeg filter in the "Mix" section below) and loudnorm to -14 LUFS.
- **Encode the upload file to under 15 MB**: two-pass H.264 at ~1600 kbps, AAC 128k, yuv420p, faststart.

Mix filter:
```
[1:a]aresample=48000,highpass=f=80,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=90,asplit=2[vs][v1];
[2:a]aresample=48000,volume=0.2[m];[m][vs]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400[md];
[md][v1]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5[a]
```

## 7. Publish
1. Copy the mp4 to `shorts/YYYY-MM-DD_<slug>.mp4`, commit ("Add Short: <title>" plus the session's attribution lines) and push to `main`. Public URL: `https://raw.githubusercontent.com/nancy8580/currentcove-media/main/shorts/<file>`
2. `mcp__Metricool_Social_Media_Management__getBestTimeToPostByNetwork` (brandId 8101545, youtube, timezone Asia/Calcutta) for today, IST. Pick the best slot that is at least 1 hour from now, at least 2 hours after the last scheduled Short in the log, and between 08:00 and 23:00 IST. Avoid exactly :00/:30, using e.g. 17:07.
3. `createScheduledPost` with blogId "8101545": providers youtube; youtubeData `{title (≤90 chars, ends with #shorts), type:"short", privacy:"public", tags:[6–10], category: EDUCATION or SCIENCE_TECHNOLOGY, madeForKids:false, isAiGeneratedContent:false}`. Text = description: hook paragraph, 3 bullet facts with emoji, a question for comments, "Sources: …", "Narration is AI-generated.", 5–7 hashtags including #Shorts.
4. Append it to `log/published.json` (date, slug, title, format, scheduled time, Metricool post id) and push.

## 8. Weekly review (Sundays only)
- Metrics to judge each Short: Viewed vs Swiped Away (target 70%+, great is 85%+), average percentage viewed (target 90%+, over 100% means loops), views stuck at 0, ~1k, ~10k or ~30k ("view jails").
- Keep a winning formula and change only ONE thing per test (hook style, length, visual style, music). Repeat what wins.
- Never delete and re-upload a Short unless it shows exactly 0 views after 6+ hours, and at most once a week.
- Pull YouTube analytics via Metricool (`getAnalyticsAvailableMetrics` network=youtube, then `getAnalyticsDataByMetrics` for the last 7 days).
- Find the best and worst Shorts. Write `log/weekly.md` with what to do more and less of, and follow it next week (e.g. shift the format mix towards winners).

## 9. Report
End with one short summary: the title, scheduled times, and any problem. On Sundays, add views, subscribers, and progress towards YPP (500 subs + 3M Shorts views/90 days for early access; 1,000 subs + 10M for ads). If a step failed and nothing was scheduled, say so plainly at the top.

## Hard rules
- Max 1 Short per run, max 6 per IST day. With this volume, variety is what keeps the channel safe: never the same format twice in a row, never the same visual template two Shorts running, no near-duplicate topics. Quality over quantity: YouTube's "inauthentic content" policy rejects mass-produced AI channels from monetization.
- Every video must be original: its own script, its own animation, sourced facts.
- No copyrighted music, footage or images. Our generated music only.
- If anything feels risky, unverifiable or sensitive, choose a different topic.
