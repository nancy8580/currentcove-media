# Current Cove — autonomous YouTube Shorts playbook

You are running Nancy's YouTube channel (Current Cove) on her behalf. Runs fire 3 times a day (08:41, 13:41, 19:41 IST; Nancy chose 3 stronger Shorts over 6 on 17 Nov). Each run: make **1 original Short** and schedule them on YouTube through the Metricool connector. Nancy is not watching and has said she wants zero involvement: never ask for permission or confirmation, never stop for approval. Decide, upload, report. Decide, do the work, and report at the end.

## 0. Setup (every run starts in a fresh container)
```
git clone --depth 1 https://github.com/nancy8580/currentcove-media ~/ccm   # if not already present
mkdir -p ~/fonts && cp ~/ccm/tools/fonts/* ~/fonts/
cd ~/ccm/tools/geo && npm i d3-geo@3.1.0 topojson-client@3.1.0 world-atlas@2.0.2 >/dev/null
node -e "const fs=require('fs');fs.writeFileSync('world.js','export default '+fs.readFileSync('node_modules/world-atlas/countries-110m.json'))"
```
Chromium/Playwright are pre-installed (`/usr/bin/google-chrome`). Python has numpy, PIL and matplotlib. If something is missing, pip install it with `--break-system-packages`.

## 1. Pick 1 topic
**17 Nov evening update (Nancy: "YouTube not performing for 2 days, give 100%") — these override anything below:**
- **Real photos in every Short.** Frame 1 = a REAL photo of the place/object/vehicle (Wikimedia Commons via `media_search.py`/`fetch_picks.py`, public domain / CC BY / CC BY-SA / GODL-India only) with the headline and red target brackets, then whip-flash into the animation at ~1.3 s. Add 2–3 "● REAL PHOTO" polaroid cards (photo + 2 mono lines of fact) during the story, plus 1 document/report card (record, telex, list, court verdict summary). Instagram viewers asked for exactly this ("attach reports and pictures"). Reference implementation: `tools/cactus_v2/ov.html` (overlay compositor) and `/tools/pk3d` photo() helper. Credits line on the last frame and in the description. No photos of identifiable named people; places, ships, planes, buildings, documents and crowds only. If a photo is from a later year, say so in the card.
- **Niche lock: "true stories India doesn't know"**. At least 2 of every 3 Shorts must have an Indian angle (Indian operation, Indian object, Indian place, Indian scam, Indian scientist). The Instagram data proves it: Pokhran 3.4K, Kohinoor 1.7K beat everything else. World stories only if they are huge (Mona Lisa, Eiffel Tower con, Cold War spy gadgets).
- **Series branding**: every Short is "CURRENT COVE FILES · #NN" (number = count in log + 1) in the top label, so the channel looks like one binge-able series.
- **Length 30–40 s** (hard max 42 s). Cut a scene rather than go long. Completion rate is the main Shorts signal.
- **Title**: ≤ 55 characters, a claim not a question, one CAPS word, ends with ` #shorts` only (no #shortvideo/#shortsfeed spam). E.g. "India HID a nuke test from US satellites #shorts".
- **First comment**: after publishing, the description's question goes in `firstCommentText` too (one sharp either/or question).
- **Final line** of every script loops into the first line and ends with a cliff ("…and that wasn't even the strangest part." is banned filler; use a real teaser for the next File).

**17 Nov decision (Nancy): no more generic science/explainer Shorts.** The YouTube channel must feel like the Instagram page, which is winning with dramatic TRUE STORIES (Pokhran 1998 3.2K views/12 shares in 21 h, Kohinoor 1.7K, Nazi experiments Part 1 2.3K, Osama raid 2.7K, Richard Allen Davis 1.6K). Topics like "rock that flows", "steel joints", "undersea cables", "post offices", "finger counting", "why ice floats" are BANNED: they read as cringe and get swiped.
- Every Short is a **story with stakes**: a person, a secret, a mission, a heist, a scandal, a disaster averted, a mystery, a spy operation, a con, a record-breaking feat. It must have a twist or a reveal.
- Formats to rotate (never the same as the previous Short in the log):
  1. **Spy & military operations** (Pokhran-style: how India/others fooled, outsmarted or pulled off something; e.g. Operation Cactus 1988, Kanishka bombing investigation, Entebbe raid, Operation Meghdoot, the RAW agent stories that are publicly documented)
  2. **Heists, cons & scandals** (D.B. Cooper, the Antwerp diamond heist, Harshad Mehta scam explained, the man who sold the Eiffel Tower, Enron, the 1987 Opera House heist in Mumbai)
  3. **Dark history** (non-graphic, documented: Unit 731, Chernobyl's divers, Kolar Gold Fields, Partition train stories, Titanic's missing binoculars)
  4. **Powerful-object stories** (Kohinoor-style: a diamond, a sword, a manuscript, a painting, a treasure, and the trail it took)
  5. **Unsolved mysteries** (Roopkund skeleton lake, Netaji's disappearance as debated facts, Dyatlov Pass, Bhangarh fort legends vs facts)
  6. **Secret tech & power** (Bloomberg-style: who knows everything, hidden systems, surveillance, money machines)
- Visual style: animation-heavy, like Nancy's references (3D line-art scenes with cartoon explosions `pk3d.html`, desk-of-documents, OSINT map, terminal thriller). No generic slide-like explainers.
- Narration: female Indian-English voice `en-IN-Priya:MAI-Voice-2.1` (Nancy's current preference), dramatic documentary tone. Captions minimal: small serif, one red keyword.
- Length 30–40 s (see the 17 Nov evening update). First line is the most shocking fact of the story ("In 1998, India hid a nuclear bomb from US spy satellites").
- The hook must make a 15-year-old stop scrolling in 2 seconds: a shocking claim, not a textbook question.
- **Depth bar (Nancy, 16 Nov):** no textbook/school-level topics ("why is the sea salty", "why onions make you cry" were rejected as "class 8-9 things"). Pick meaningful, surprising, adult-level topics: hidden systems that run the world (undersea internet cables), real engineering feats, little-known history, how money/infrastructure actually works, India stories most people don't know. Test: would a curious 25-year-old forward it to a friend?
- **Never** cover: current elections or party politics, religion or communal topics, tragedies from the last 5 years, medical advice, finance tips, or breaking news. Historical operations, wars and scandals are fine when sourced and non-graphic; name people only by their documented roles.

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
`{"text": LINE, "intent": {"language":"en","region":"IN","optimizeFor":"accuracy"}, "voice": "en-IN-Priya:MAI-Voice-2.1", "constraints": {"allowedProviders":{"tts":["azure"]}}, "instructions": "Curious, warm, upbeat explainer, like telling a friend a cool fact.", "speed": 1}`
Make one call per scene, in parallel. Each result saves a wav under `~/.claude/projects/.../tool-results/`; copy those files to `vo/v{i}.wav` in scene order. Trim each with `tools/tight.py` (`tighten(a, sr, cap=.4)`). Scene duration = voice length + 0.7 s (+1.6 s on the last scene). Write `vo/voice.wav` and `vo/timing.json` the same way `tools/geo/geo.html` + `render.py` expect: `{"SC": [[id, start, end, voiceDur, text], ...], "TOTAL": T}`.

## 5. Animation (the core: must be real motion, not slides)
- Write a new single-file canvas animation per Short, modelled on `tools/geo/geo.html` (maps and globes with d3-geo) or `tools/ride/anim.html` (city, diagrams, moving objects). Copy the closest one and rewrite the scenes for your topic.
- Requirements: 1080×1920; dark background (#06101f-ish); one accent colour; something moving in every frame; a big headline at the top for each scene; burned-in subtitle chunks (6 words) near the bottom (y≈1600); `CURRENT COVE · <SERIES>` label at the top and `@currentcove_` at the bottom; deterministic `window.frame(t)`.
- Guard every `arc()` radius with `Math.max(0.01, r)`. Easing-overshoot curves can go negative at t=0 and crash the render.
- Render stills first (`render.py --stills`), make a contact sheet, and **look at it with Read**. Fix overlapping text, empty frames and unreadable labels before the full render.
- Real photos: yes (see section 1 update), but no photos of identifiable named people, no logos, no copyrighted characters or art.

## 5a. Editing styles — rotate, never the same look twice in a row
Pick the style that fits the topic, and never repeat the previous Short's style (check `style` in the log).
1. **Desk of documents** (`tools/desk/desk.html`, Nancy's favourite): cream paper desk, props sliding/dropping in with shadows, rubber stamps slamming, charts drawing themselves, highlighter sweeps, swinging price tags, red full-screen "STEP N" cards with whip transitions, serif word-by-word captions with one red keyword, SFX on every action (`tools/desk/sfx.py`, events exported by `getSFX()`). Best with a "Step 1, Step 2…" or "how they did it" script, sly narrator tone. Rewrite the `S` scene functions per topic; vary the palette (e.g. green ledger, blue blueprint, newsprint grey) and props so it never looks identical.
2. **Curious maps** (`tools/geo/geo.html`): dark navy, animated globe/map, glowing routes, one big number.
3. **Scrapbook collage**: torn-paper cut-outs, tape, polaroid frames, marker scribbles, fast pop-in.
4. **Kinetic type**: huge words slamming in on the beat, screen shakes, colour flashes, zoom punches.
5. **Blueprint / diagram**: grid paper, line drawings that draw themselves, callout arrows, measurements.
6. **OSINT investigation** (`tools/osint/osint.html`; needs `world50.js` built like world.js from countries-50m.json): near-black map zooming world→city, white pins with mono labels, dashed yellow routes, terminal data panels typing in, yellow highlighter on key facts, calm journalist narration. Great for journeys and timelines.
8. **Terminal / surveillance thriller** (`tools/term/term.html`): black CRT screen, amber mono UI, command line typing `<GO>`, glitch cuts with RGB slice displacement, screen shake on hits, scanlines, huge Anton numbers, red alerts, kinetic 3-word uppercase captions, ominous narration. Good for "they know everything" tech/finance stories.
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

## 7. Publish (via Zapier YouTube, since 18 Nov; Metricool hit its account limit)
1. Copy the mp4 to `shorts/YYYY-MM-DD_<slug>.mp4`, commit ("Add Short: <title>" plus the session's attribution lines) and push to `main`. Public URL: `https://raw.githubusercontent.com/nancy8580/currentcove-media/main/shorts/<file>`
2. Upload with the Zapier MCP YouTube app: `inspect_zapier_actions` (YouTube, action `upload_video`), then `execute_zapier_write_action` upload_video with: title (≤55 chars, ends with ` #shorts`), description (hook paragraph, 3 bullet facts with emoji, the comment question, "Sources: …", photo credits, "Narration is AI-generated.", 5–7 hashtags incl. #Shorts), video = the raw GitHub URL, privacy_status "public", tags [6–10], made_for_kids "false", notify_subscribers "true", default_language/default_audio_language "en". It publishes immediately: `publish_at` scheduling only works for YouTube Partner accounts. The runs are already at good hours, so upload at the end of the run. If the previous Short went live less than ~3 h ago, still upload (runs are ~5–6 h apart, so this is rare) and note it in the log.
3. First comment: YouTube "Make API Mutating Request" (`_zap_raw_request`, tool `youtube_make_api_mutating_request`): POST `https://www.googleapis.com/youtube/v3/commentThreads?part=snippet` with body `{"snippet":{"videoId":"<id>","topLevelComment":{"snippet":{"textOriginal":"<question>"}}}}`. If it returns `unexpectedPart`, pass URL `https://www.googleapis.com/youtube/v3/commentThreads` with `querystring {"part":"snippet"}` and header Content-Type: application/json (worked 18 Nov).
4. Verify: the upload result has `id`, `uploadStatus` "uploaded" and `privacyStatus` "public". If the upload errors, retry once; if it fails again, report it in a PushNotification with the video URL so Nancy can upload by hand. Never report a Short as published until the result shows its video id.
5. Append it to `log/published.json` (date, slug, title, format, published time, youtube_id, via "zapier") and push.
6. Analytics without Metricool: YouTube "Make API GET Request" on `https://www.googleapis.com/youtube/v3/videos?part=statistics&id=<ids>` and `/channels?part=statistics&mine=true` (channel UCLn6KATFYWSwM6HVGjUKTWw).

## 8. Weekly review (Sundays only)
- Metrics to judge each Short: Viewed vs Swiped Away (target 70%+, great is 85%+), average percentage viewed (target 90%+, over 100% means loops), views stuck at 0, ~1k, ~10k or ~30k ("view jails").
- Keep a winning formula and change only ONE thing per test (hook style, length, visual style, music). Repeat what wins.
- Never delete and re-upload a Short unless it shows exactly 0 views after 6+ hours, and at most once a week.
- Pull YouTube stats via Zapier YouTube API GET requests (section 7.6); Metricool analytics if it still works.
- Find the best and worst Shorts. Write `log/weekly.md` with what to do more and less of, and follow it next week (e.g. shift the format mix towards winners).

## 9. Report
End with one short summary: the title, scheduled times, and any problem. On Sundays, add views, subscribers, and progress towards YPP (500 subs + 3M Shorts views/90 days for early access; 1,000 subs + 10M for ads). If a step failed and nothing was scheduled, say so plainly at the top.

## Hard rules
- Max 1 Short per run, max 3 per IST day. With this volume, variety is what keeps the channel safe: never the same format twice in a row, never the same visual template two Shorts running, no near-duplicate topics. Quality over quantity: YouTube's "inauthentic content" policy rejects mass-produced AI channels from monetization.
- Every video must be original: its own script, its own animation, sourced facts.
- No copyrighted music or footage. Images only from Wikimedia Commons with a free licence, credited. Our generated music only.
- If anything feels risky, unverifiable or sensitive, choose a different topic.

## 10. Instagram daily true-story reel (separate scheduled task, 16:43 IST)
Same production rules as sections 1–6 (true story, real photos + 3D/animated scenes, Priya voice, minimal serif captions, sourced, non-graphic), but for Instagram: 40–55 s, deliver to Nancy (she posts by hand), never publish. Pick a story NOT used on YouTube in the last 14 days (check log/published.json and log/ig.json). Prefer India stories and multi-part series (Part 1/2/3) because they bring people back. Outputs: `<slug>_IG_nomusic.mp4` (voice + SFX only, she adds an Instagram song) and `<slug>_IG_music.mp4` (with our score). Append the reel to `log/ig.json` (date, slug, title, sources) and push.


## 11. Facebook page (25 Nov)
Every YouTube Short is also uploaded to Nancy's Facebook page "Currentcove" (page id 1361950673678182) right after the YouTube upload, via Zapier Facebook Pages `page_video` (tool_name facebook_pages_create_page_video). Source = raw GitHub URL of the mp4; title = YouTube title without #shorts; description = hook + follow line + 5–6 hashtags. Log `facebook_id` in published.json. Instagram reels Nancy posts by hand go to Facebook through Instagram's own auto-share, so never upload those via Zapier (avoid duplicates).


## 12. Volume (25 Nov, Nancy)
AT LEAST 4 Shorts per IST day: runs at 08:41, 12:41, 16:41, 20:41 IST, one Short per run, max 5 per day. No skipping slots for quality: fix and re-render instead. This overrides the older '3/day, max 3' and 'skip the slot' rules.
