# Word Pop!

A colorful spelling playground written in **Unison**, hosted on **Unison Cloud**. No JavaScript is shipped or required. Unison renders every page and processes game actions; CSS handles the card flip, motion, responsive layout, and celebrations. Audio uses native HTML controls.

**Play:** https://wolfbreed1829.unison-services.cloud/s/word-pop/

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

- `src/game.u` — typed deck, answer normalization, scoring, rounds, page rendering, HTTP service, local server, deployment, and seven native Unison test groups.
- `assets/style.css` — visual design and responsive styles. Nunito is loaded from Google Fonts with a system-font fallback.
- `assets/audio/*.wav` — the 20 word recordings, included in the repository.
- `scripts/audio.ps1` — optional Windows speech synthesis regeneration; not required to run the app.
- `scripts/build.ps1` — UCM transcript orchestration. There is no Node/npm toolchain.

The spelling app deliberately sends `Content-Security-Policy: script-src 'none'`. Keyboard controls, native audio, reduced-motion support, and a pause-motion toggle work without scripts. The pause toggle applies to the current page; the system reduced-motion preference persists across navigation.

## Verification

Verified with UCM 1.3.0:

- All seven native Unison test groups pass: the 20-word deck, answer normalization, score rules, duplicate-answer protection, retry behavior, URL-state filtering, and HTML escaping.
- Browser checks cover card flipping, mastery, mistakes and retries, case/space normalization, audio playback, word scramble, and an entire 20-word spelling round reaching 200 points.
- A full round completes with browser JavaScript disabled.
- Desktop and 390px mobile layouts were visually inspected; no horizontal overflow was found.

The hosted application is on Unison Cloud. GitHub stores its source; GitHub Pages is not used because this application runs native Unison on the server.
