# Word Pop! — The Word Kitchen

A colorful culinary spelling adventure written in **Unison**, hosted on **Unison Cloud**. No JavaScript is shipped or required. Unison renders every page and processes game actions; CSS handles the card flip, motion, responsive layout, and celebrations. Audio uses native HTML controls.

**Play:** https://wolfbreed1829.unison-services.cloud/s/word-pop/

## A kitchen that grows with you

Each newly mastered word adds a cupcake, cookie, or macaron to a clickable 20-slot collection. New treats pop into place and Chef Star celebrates. The illustrated kitchen develops with your progress:

| Words mastered | Kitchen reward | Chef badge |
| --- | --- | --- |
| 5 | Working stand mixer | Mix master |
| 10 | Full cookie jar | Cookie captain |
| 15 | Celebration cake | Pastry pro |
| 20 | Candles, bunting, and a kitchen party | Head chef |

Wrong answers preserve existing rewards. Refreshing or repeating a correct answer does not duplicate treats. Flashcard mastery also earns a treat. The kitchen, tray, badges, feedback, and progress are all rendered directly from the same Unison round state.

## Play modes

- **Flashcards:** read, listen, flip for a meaning and example, then choose “Got it!” or “Practice again.” A newly mastered word earns 5 points.
- **Spell it:** listen to the recording and type the word. The first correct attempt earns 10 points; a correct retry earns 5.
- **Word scramble:** use the colorful letter tiles, definition, and recording to find the word.

Every word can earn points once in a round. Switching modes retains progress. Progress travels in ordinary links and form fields in the current tab; bookmark the current URL to keep it. There are no accounts, cookies, analytics, database, or shared leaderboard. Scores are for personal practice and are not tamper-proof. The home logo starts a fresh round.

## Included words

smart, award, charge, worn, argue, stormy, bore, ward, warp, backyard, door, dart, fort, morning, carpet, core, spark, charcoal, forecast, guard.

## Run on Windows

Requires [Unison Codebase Manager](https://www.unison-lang.org/docs/quickstart/) **1.3.0**. Run from the repository directory in PowerShell:

```powershell
chcp.com 65001
ucm -C .ucm transcript.in-place bootstrap.md
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build.ps1
ucm run.compiled .ucm/local.uc
```

Open http://127.0.0.1:8089. The bootstrap installs pinned base and Cloud libraries. The first library download can take several minutes. Run bootstrap once; subsequent edits only need the build step. Restart the local server after changing assets.

## Deploy

Authenticate the intended Unison account with `auth.login` in UCM, then run:

```powershell
chcp.com 65001
ucm run.compiled .ucm/deploy.uc
```

`pop.deploy` uploads the service and assigns the stable name `word-pop` under the authenticated account. CSS and the 20 audio clips are captured as part of the deployed Unison service; no separate asset server is needed. Rebuild after changing Unison source. Asset-only edits are picked up by the deploy command.

## Source map

- `src/game.u` — typed deck, answer normalization, scoring, rounds, interactive kitchen rendering, HTTP service, local server, deployment, and nine native Unison test groups.
- `assets/style.css` — visual design and responsive styles. Nunito is loaded from Google Fonts with a system-font fallback.
- `assets/kitchen.css` — gingham and wood surfaces, the illustrated kitchen, collectible treats, chef badges, and CSS reward animations.
- `assets/audio/*.wav` — the 20 word recordings, included in the repository.
- `scripts/audio.ps1` — optional Windows speech synthesis regeneration; not required to run the app.
- `scripts/build.ps1` — UCM transcript orchestration. There is no Node/npm toolchain.

The spelling app deliberately sends `Content-Security-Policy: script-src 'none'`. Keyboard controls, native audio, reduced-motion support, and a pause-motion toggle work without scripts. The pause toggle applies to the current page; the system reduced-motion preference persists across navigation.

## Verification

Verified with UCM 1.3.0:

- All nine native Unison test groups pass: the 20-word deck, answer normalization, score rules, duplicate-answer protection, retry behavior, URL-state filtering, HTML escaping, kitchen milestones, and reward persistence.
- Browser checks cover card flipping, mastery, mistakes and retries, case/space normalization, audio playback, word scramble, and an entire 20-word spelling round reaching 200 points.
- A full round completes with browser JavaScript disabled. A round including one incorrect attempt produces 20 treats, all four kitchen unlocks, and 195 points. Refreshing a correct answer preserves the treat count.
- Keyboard card flipping, the pause-motion toggle, reduced-motion preferences, native audio, and flashcard reward animation were checked.
- Desktop and mobile layouts were visually inspected. Widths of 320, 390, 768, and 1440 pixels have no horizontal overflow.

The hosted application is on Unison Cloud. GitHub stores its source; GitHub Pages is not used because this application runs native Unison on the server.
