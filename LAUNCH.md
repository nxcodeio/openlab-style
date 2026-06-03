# Launch playbook — openlab-style

This is the operational doc for getting openlab-style in front of the people who'd find it useful. Use it after [PUBLISHING.md](PUBLISHING.md) lands the package on PyPI.

The whole strategy: **one image does the selling.** A clean openlab-style output. People who know MATLAB recognize the look instantly; people who don't know MATLAB aren't the target audience anyway. The text is supporting.

The hero asset: [`examples/demo.png`](examples/demo.png) — single 1100×770 image showing openlab-style output across 4 plot types (multi-line, histogram, heatmap with parula, log-scale). Use this everywhere.

We deliberately do NOT ship a side-by-side "vs matplotlib defaults" comparison. Reason: matplotlib 3.10's own defaults already look superficially MATLAB-ish (white background, full axes box, sans-serif font), so the side-by-side diff isn't dramatic enough to sell from a thumbnail. The right pitch is **"this IS MATLAB"** not **"this is different from matplotlib"** — the viewer's existing MATLAB intuition is the comparison.

---

## Pre-launch checklist

Before posting anything:

- [ ] `pip install openlab-style` works from a fresh machine (PUBLISHING.md step 6)
- [ ] PyPI page renders the README correctly: https://pypi.org/project/openlab-style/
- [ ] GitHub repo has at least one tagged release: https://github.com/nxcodeio/openlab-style/releases
- [ ] `examples/demo.png` exists and looks right (regenerate with `python examples/render_demo.py` if you tweak styles)
- [ ] You have a personal Twitter/X handle ready to post from (separate from any company account)
- [ ] You're available for the next 2-3 hours to respond to comments — half of the value of a launch is showing up in the replies

If any unchecked, fix first. A launch post linking to a broken `pip install` is worse than no launch.

---

## Channel-by-channel posts

Each channel has different culture. Same product, different angle, different lead.

Order of operations: **start with low-stakes channels** (your own Twitter, r/Python) to validate the pitch before hitting the high-traffic ones (HN, r/EngineeringStudents). If the first post falls flat, you can rewrite before burning bigger audiences.

### 1. Twitter/X (start here — easiest to iterate)

Single image post. The image does the work.

**Tweet text** (under 280 chars, but keep it tight):

> Tired of your AI's matplotlib plots looking nothing like MATLAB?
>
> `pip install openlab-style`
>
> Two lines. Your plots now look like they came out of MATLAB.
>
> Works in ChatGPT Code Interpreter, Claude, Cursor, Jupyter, Colab.
>
> https://github.com/nxcodeio/openlab-style

Attach `demo.png` as the single image. **Do not** add multiple images — single-image tweets get more engagement than carousels for this kind of dev tool.

**Follow-up reply** (post 30 sec after the main tweet, as a thread):

> Why this exists: AI assistants generate Python + matplotlib for technical work. But if you're a MATLAB user — student, researcher, engineer — matplotlib's blue-orange-green-tab10 + viridis colormap is an instant tell that the work wasn't done in MATLAB.
>
> openlab-style aligns matplotlib's rcParams to MATLAB R2014b+ defaults: lines palette, parula colormap, inward ticks, full axes box, Helvetica.
>
> One `apply()` call. No need to learn anything.

### 2. r/Python (validate with a technical audience)

Title: `openlab-style: 200-line matplotlib rcParams package to mimic MATLAB R2014b+ defaults`

Body:

> matplotlib's defaults haven't been the same as MATLAB's since forever — different line colors, viridis vs parula colormap, outward ticks vs inward, no top/right spines. For most people this is fine. For people who work alongside MATLAB users (students whose professor expects MATLAB-styled output, researchers in MATLAB-using labs), it's a constant friction.
>
> I packaged the rcParams patches + the parula colormap as a tiny library. `pip install openlab-style`, call `apply()`, done.
>
> Sample output: [link to demo.png on GitHub]
>
> Repo: https://github.com/nxcodeio/openlab-style
>
> 200 lines of Python, MIT, 8KB wheel, depends only on matplotlib. Tested on matplotlib 3.10. Sister project is openlab — an MCP server for running real Octave from Claude/Cursor — for when matching the look isn't enough.

Mods are picky about self-promo. The technical content (rcParams, parula extraction, MCP sister project) signals "real contribution" not "spam ad."

### 3. r/EngineeringStudents (the actual target user)

Title: `Free tool: make ChatGPT's plots look like MATLAB for your homework`

Body:

> If you've ever asked ChatGPT to help with a signals/control/numerical methods assignment, you've seen it: ChatGPT writes Python + matplotlib, you screenshot the output, and the plot looks nothing like what your textbook examples or professor's slides show. Different colors, different colormap, different everything.
>
> I made a tiny Python package that fixes this: `openlab-style`. It styles matplotlib to match MATLAB R2014b+ defaults (the version most professors are using).
>
> In ChatGPT Code Interpreter:
>
> ```
> !pip install openlab-style
> import openlab_style; openlab_style.apply(grid=True)
> # ... now any plot you make looks like MATLAB
> ```
>
> Sample output: [demo.png]
>
> Free, MIT licensed, open source: https://github.com/nxcodeio/openlab-style
>
> Caveat: this only fixes the **look**. If your assignment specifically requires MATLAB code/syntax, you still need MATLAB or Octave. (I'm also working on that — sister project openlab.)

Honest framing: "for your homework" is exactly what undergrads search for. Don't pretend it isn't.

### 4. r/ChatGPT (huge audience, lower technical bar)

Title: `Made a one-liner that gives ChatGPT's Code Interpreter MATLAB-style plots`

Body: shorter, image-first.

> ChatGPT's matplotlib output looks like matplotlib. If you want it to look like MATLAB (for school, work, or just because it looks cleaner), there's now a pip package:
>
> [demo.png — single image]
>
> Two lines in Code Interpreter:
>
> ```
> !pip install openlab-style
> import openlab_style; openlab_style.apply(grid=True)
> ```
>
> Open source: https://github.com/nxcodeio/openlab-style

### 5. Hacker News (only after the other channels work)

Only post to HN after the other channels show signal that the pitch lands. HN is high-stakes — one shot per submission, harsh feedback, but huge upside.

Title: `Show HN: openlab-style – matplotlib styling to mimic MATLAB`

URL field: https://github.com/nxcodeio/openlab-style

First comment (post yourself, right after submitting):

> Background: I was watching how AI assistants (ChatGPT, Claude) handle technical computing requests and noticed a small friction — when the user is a MATLAB user (student, researcher, engineer collaborating with MATLAB-using labs), the AI-generated matplotlib output looks visually distinct from MATLAB in ways that matter (line color order, colormap, axes style, font). The work is "right" but doesn't fit the workflow.
>
> openlab-style is a ~200-line package that aligns matplotlib's rcParams to MATLAB R2014b+ defaults. One `apply()` call. The parula colormap is included (it's not in matplotlib by default; closest built-in is viridis).
>
> The bigger project (openlab) is an MCP server that lets AI tools run real Octave for cases where matching the look isn't enough — but openlab-style ships first because it's the smallest useful thing.
>
> Happy to answer questions about rcParams choices, the parula RGB extraction, or the broader "AI for MATLAB workflows" thesis.

**Time the HN post for Tuesday-Thursday morning Pacific** (~9-10am PT). That's empirically the best window for Show HN traction.

### 6. r/matlab (cautious — they might love it OR hate it)

This community has a complicated relationship with Octave / OSS alternatives. Some are happy to see the visual style of MATLAB respected; others are protective of the brand. Pitch carefully.

Title: `Open source: matplotlib styling that matches MATLAB R2014b+ visual defaults`

Body:

> Built this because AI tools (ChatGPT, Claude) generate matplotlib for technical computing, and the visual style is jarringly different from MATLAB output. openlab-style is a tiny Python package that styles matplotlib to match MATLAB defaults — lines palette, parula colormap, inward ticks, full axes box.
>
> Not a MATLAB replacement, not a MATLAB clone — just visual styling for Python plots so they fit MATLAB-shaped workflows.
>
> https://github.com/nxcodeio/openlab-style
>
> Curious if anyone here has run into the same visual-mismatch friction when reviewing AI-assisted work.

Last line invites discussion rather than pitches. Better engagement.

---

## Showing up in replies

Half the value of a launch is the replies. Reserve 2-3 hours after each post.

**Common questions you should pre-write answers for**:

1. "Why not just use matplotlib's `style.use('classic')` or similar?"
   - Answer: classic doesn't ship parula, doesn't match MATLAB's lines palette, doesn't set the axes box / tick direction. openlab-style is opinionated specifically for MATLAB fidelity.

2. "Why not just use Octave?"
   - Answer: openlab-style is for the case where you're already using Python + matplotlib (e.g. ChatGPT Code Interpreter) and just want it to LOOK like MATLAB. For actually running MATLAB code, see the sister project `openlab` (MCP server with real Octave).

3. "Is this a MATLAB clone? Does it run MATLAB code?"
   - Answer: no, just visual styling. Different problem.

4. "Why parula specifically? viridis is perceptually uniform too."
   - Answer: they're both perceptually uniform, but parula has a distinct look (yellower top, more blue-saturated bottom). For people who think in MATLAB visual idioms, parula matters.

5. "MATLAB is closed source though?"
   - Answer: yes — we're not redistributing MATLAB code. The parula RGB values are a widely-republished open-source approximation, and MATLAB's "lines" palette is published reference data, not code. The library is pure Python + matplotlib.

6. "Does this work in Jupyter/Colab/Spyder/PyCharm?"
   - Answer: yes anywhere matplotlib runs. `apply()` mutates global rcParams, persistent for the session.

**Bad-faith comment strategy**: respond once politely with the technical answer. If they come back hostile, don't engage twice. The audience is reading the thread, not the troll.

---

## After the launch

**Track these metrics for the first week** (manually OK, no analytics needed yet):

- GitHub stars (refresh daily, screenshot the count at +24h, +48h, +1wk)
- PyPI download stats: https://pypistats.org/packages/openlab-style (lag ~1 day)
- GitHub issues opened (any signal — questions, bug reports, requests)
- r/* upvotes + comment count for each post

**Definition of success for v0.1 launch**:

- ≥ 50 GitHub stars in week 1
- ≥ 500 PyPI downloads in week 1
- ≥ 3 GitHub issues from non-Vivian users (this is the real proof: someone cared enough to file)
- ≥ 1 quote-tweet / repost from someone in the EE / AI / Python community

If all 4 hit → you have product-market fit signal. Proceed with openlab v0.2 (MCP) launch in 2 weeks.
If 0-1 hit → pitch is wrong or audience is wrong. Iterate (rewrite README, try different channels, find real users to talk to).
If 2-3 hit → it's working but not viral. Keep posting, find the right channel.

**Don't pivot the product on day 7.** Software product-market signal takes 2-4 weeks to read clearly through noise. But do read the issues + comments for what people actually ask for — they'll tell you v0.2 features.

---

## What NOT to do

- **Don't post to all 6 channels in one day.** Spread over 3-4 days. Each post deserves your attention.
- **Don't link to the GitHub from inside ChatGPT screenshots.** The post should be a self-contained image + text.
- **Don't pretend this is bigger than it is.** It's a 200-line styling library. "Tiny but useful" plays better than "revolutionary."
- **Don't reply to every comment with a sales pitch.** Some comments deserve "good question, opened an issue to track." Showing process is better than showing eagerness.
- **Don't post about Product 2 (openlab MCP) yet** — that has its own launch when v0.2 is ready. Keep narratives separate.
