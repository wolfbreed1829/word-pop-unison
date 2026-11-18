# Word Pop! — Junior Chef Challenge

A culinary spelling adventure for a nine-year-old, written in **Unison** and hosted on **Unison Cloud**. A realistic kitchen, recipe cards, and collectible treats turn practice into a junior-chef challenge. No JavaScript is shipped or required. Unison renders every page and processes game actions; CSS handles the card flip, motion, responsive layout, and celebrations. Audio uses native HTML controls.

**Play:** https://wolfbreed1829.unison-services.cloud/s/word-pop/

**Crossword:** https://wolfbreed1829.unison-services.cloud/s/word-pop/?m=cross

## A kitchen that grows with you

Each newly mastered word adds a cupcake, cookie, or macaron to a clickable 20-slot collection. New treats pop into place, and the realistic kitchen photograph changes at each milestone:

| Words mastered | Kitchen reward | Chef badge |
| --- | --- | --- |
| 5 | Red stand mixer | Mixer Master |
| 10 | Full cookie jar | Baker |
| 15 | Celebration cake | Pastry Chef |
| 20 | Candles, bunting, and a kitchen party | Head chef |

Wrong answers preserve existing rewards. Refreshing or repeating a correct answer does not duplicate treats. Flashcard mastery also earns a treat. The kitchen, tray, badges, feedback, and progress are all rendered directly from the same Unison round state.

## iPad play

Open the play link in Safari. Portrait mode places the game above the score and collection panels; landscape mode puts progress alongside the game. Touch controls are at least 44 CSS pixels, with larger answer buttons and 22-pixel spelling inputs. Autocorrect, automatic capitalization, and spellchecking are disabled for answers. Audio starts only after tapping its native play control. Safe-area padding, Safari card-flip styles, browser zoom, and reduced-motion preferences are supported. The game requires an internet connection.

## Play modes

- **Flashcards:** read, listen, flip for a meaning and example, then choose “Got it!” or “Practice again.” A newly mastered word earns 5 points.
- **Spell it:** listen to the recording and type the word. The first correct attempt earns 10 points; a correct retry earns 5.
- **Word scramble:** use the colorful letter tiles, definition, and recording to find the word.
- **Chef's crossword:** a harder, connected 15-by-14 puzzle containing all 20 words. Definition clues and shared letters replace the visible word bank. Select a numbered square or clue, type a whole answer, and choose **Place word**. Previous/Next clue buttons avoid repeated scrolling. **Check puzzle** marks correct and incorrect filled words without revealing answers; optional hints give a second clue and first letter. Completing all 20 unlocks the celebration kitchen.

Every word can earn points once in a round. Switching modes retains progress. Progress travels in ordinary links and form fields in the current tab; bookmark the current URL to keep it. There are no accounts, cookies, analytics, database, or shared leaderboard. Scores are for personal practice and are not tamper-proof. The home logo starts a fresh round.

The crossword keeps its own letter grid alongside the original game scores. Switching modes preserves its letters; editing an intersection updates both words. Crossword completion is its own challenge and does not change spelling scores. **Start a fresh crossword** clears only that grid. On smaller screens the grid scrolls horizontally; clue buttons and whole-word entry remain available without interacting with individual letter cells.

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

`pop.deploy` uploads the service and assigns the stable name `word-pop` under the authenticated account. The pure handler is deployed with `Cloud.deploy.remote` and `Cloud.exposeHttp`, without a pooled ability wrapper. CSS is captured by the service. Audio and kitchen artwork load from immutable public GitHub commits, keeping those files out of the game request closure. Rebuild after changing Unison source. CSS-only edits are picked up by the deploy command. If replacing recordings or artwork, commit them and update the pinned URLs in `pop.audio` or `assets/studio.css`.

## Source map

- `src/game.u` — typed deck, answer normalization, scoring, rounds, interactive kitchen rendering, HTTP service, local server, deployment, and the original nine native Unison test groups.
- `src/crossword.u` — connected crossword layout, shared-letter board, answer entry, checking, clues, page rendering, and six native Unison test groups.
- `assets/style.css` — base layout and responsive styles. Manrope is loaded from Google Fonts with a system-font fallback.
- `assets/kitchen.css` — kitchen layout, collectible treats, chef badges, and CSS reward animations.
- `assets/studio.css` — realistic junior-chef styling, photographic stages, and iPad/touch layouts.
- `assets/crossword.css` — crossword grid, recipe-style clue editor, checking states, and responsive touch layout.
- `assets/chef-kitchen-v2.png` — generated artwork containing five kitchen stages, selected with CSS background positioning.
- `assets/kitchen-artwork.txt` — artwork source and generation prompt.
- `assets/audio/*.wav` — the 20 word recordings, included in the repository.
- `scripts/audio.ps1` — optional Windows speech synthesis regeneration; not required to run the app.
- `scripts/build.ps1` — UCM transcript orchestration. There is no Node/npm toolchain.
- `scripts/check-crossword.py` — optional independent geometry audit; Python is used only for development checks.

The spelling app deliberately sends `Content-Security-Policy: script-src 'none'`. Keyboard controls, native audio, reduced-motion support, and a pause-motion toggle work without scripts. The pause toggle applies to the current page; the system reduced-motion preference persists across navigation.

## Verification

Verified with UCM 1.3.0:

- All fifteen native Unison test groups pass: the original nine plus crossword bounds, input sanitization, entry validation, crossing edits, full solution, and progress preservation.
- `python scripts/check-crossword.py` independently verifies all 20 words appear exactly once, crossing letters agree, clue numbers follow reading order, every word connects to the same grid, and there are no unintended adjacent words.
- Browser checks cover card flipping, mastery, mistakes and retries, case/space normalization, audio playback, word scramble, and an entire 20-word spelling round reaching 200 points.
- A full round completes with browser JavaScript disabled. A round including one incorrect attempt produces 20 treats, all four kitchen unlocks, and 195 points. Refreshing a correct answer preserves the treat count.
- Keyboard card flipping, the pause-motion toggle, reduced-motion preferences, native audio, and flashcard reward animation were checked.
- Desktop and mobile layouts were visually inspected. Widths of 320, 390, 768, and 1440 pixels have no horizontal overflow.
- WebKit 26 touch emulation with JavaScript disabled passed at 768, 820, 1024, 1180, and 1366 CSS pixels: no horizontal overflow, primary tap targets at least 44 pixels, card flipping, native WAV playback, spelling mistakes/retries, Enter-key submission, refresh protection, scramble mode, and all five kitchen photographs. This is browser-engine testing on Windows, not a physical iPad test. Test media was served from the committed local assets; public asset responses were checked separately.
- The crossword passed a complete 20-word WebKit touch playthrough with JavaScript disabled: invalid-length rejection, wrong/correct manual checks, shared-letter updates, hint disclosure, shared-number Across/Down toggling, previous/next navigation, mode switching, completion, refresh, and reset without losing spelling scores. Layouts at 390, 768, 820, 1024, 1180, and 1366 pixels have no page overflow and primary targets are at least 44 pixels. The original game checks were rerun successfully after adding the fourth mode.
- The November 18, 2026 Unison Cloud deployment passed live browser checks for opening the crossword, placing a word, and checking the puzzle.

Public Unison Cloud requests intermittently timed out or returned HTTP 500 during checks on November 16, 2026. Those errors were not reproduced in the November 18 crossword smoke check; this does not establish long-term hosting reliability.

The hosted application is on Unison Cloud. GitHub stores its source; GitHub Pages is not used because this application runs native Unison on the server.
