"""Exercise rendered links/forms against a running server, without browser scripts.

Run: python scripts/check-game.py [http://127.0.0.1:8089/]
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlencode, urljoin, urlsplit, urlunsplit
from urllib.request import urlopen
import re
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8089/'
ROOT = Path(__file__).resolve().parents[1]
WORDS = re.findall(r'Card "([a-z]+)"', (ROOT / 'src/game.u').read_text(encoding='utf-8').split('pop.word :')[0])


class Page(HTMLParser):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.forms, self.links, self.inputs, self.audio = [], [], [], []
        self.form = None
        with urlopen(url, timeout=45) as response:
            assert response.status == 200
            self.html = response.read().decode('utf-8')
        self.feed(self.html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'form':
            self.form = {'attrs': attrs, 'fields': {}, 'buttons': []}
            self.forms.append(self.form)
        elif tag == 'input':
            self.inputs.append(attrs)
            if self.form is not None and 'name' in attrs:
                self.form['fields'][attrs['name']] = attrs.get('value', '')
        elif tag == 'button' and self.form is not None:
            self.form['buttons'].append(attrs)
        elif tag == 'a':
            self.links.append(attrs)
        elif tag == 'audio':
            self.audio.append(attrs)

    def handle_endtag(self, tag):
        if tag == 'form':
            self.form = None

    def form_with(self, field):
        return next(f for f in self.forms if field in f['fields'])

    def submit(self, form, fields=None, button=None):
        data = form['fields'] | (fields or {})
        if button and 'name' in button:
            data[button['name']] = button['value']
        parts = urlsplit(urljoin(self.url, form['attrs'].get('action', '')))
        return Page(urlunsplit(parts._replace(query=urlencode(data))))

    def follow(self, link):
        return Page(urljoin(self.url, link['href']))

    def link_class(self, name):
        return [link for link in self.links if name in link.get('class', '').split()]

    def action(self, action):
        form = next(f for f in self.forms if any(b.get('value') == action for b in f['buttons']))
        return self.submit(form, button=next(b for b in form['buttons'] if b.get('value') == action))


home = Page(BASE)
assert 'unborn' in home.html
assert len(home.link_class('word-chip')) == 20
assert all(int(re.search(r'&n=(\d+)', a['href']).group(1)) >= 20 for a in home.link_class('word-chip'))

for start, size, cells in [(0, 210, 87), (20, 270, 120)]:
    page = Page(urljoin(BASE, '?' + urlencode({'m':'cross', 'n':start, 'k':str(start+2), 's':10})))
    assert len(page.link_class('cw-clue')) == 20
    assert len(page.link_class('cw-cell')) == cells
    assert all(a['href'].endswith('#cross-editor') for a in page.link_class('cw-cell'))
    assert '<script' not in page.html.lower()
    form = page.form_with('entry')
    assert form['fields']['crossaction'] == 'place', 'Keyboard submission must include the action'
    assert len(form['fields']['cw']) == size
    for word in WORDS[start:start+20]:
        assert word in page.html, f'Missing spelling word: {word}'

    invalid = page.submit(form, {'entry':'x'})
    assert 'Use exactly' in invalid.html
    assert invalid.form_with('entry')['fields']['cw'] == form['fields']['cw']
    wrong = page.submit(form, {'entry':'x' * len(WORDS[start])}).action('check')
    assert '0 of 20 correct' in wrong.html
    assert len(wrong.link_class('retry')) >= 1

    # No button parameters: mirrors Enter/software-keyboard submission.
    page = page.submit(form, {'entry':' ' + WORDS[start].upper() + ' '})
    assert page.form_with('entry')['fields']['entry'] == WORDS[start]
    checked = page.action('check')
    assert '1 of 20 correct' in checked.html
    # Also accept an answer from an older form omitting crossaction entirely.
    old_form = page.form_with('entry')
    del old_form['fields']['crossaction']
    page = page.submit(old_form, {'entry':WORDS[start]})
    assert 'Word placed.' in page.html
    saved = page.form_with('entry')['fields']['cw']
    flash = page.follow(next(a for a in page.link_class('mode') if '?m=flash' in a['href']))
    assert "data-baked='1'" in flash.html
    page = flash.follow(next(a for a in flash.link_class('mode') if '?m=cross' in a['href']))
    assert page.form_with('entry')['fields']['cw'] == saved

    for i in range(start, start + 20):
        link = next(a for a in page.link_class('cw-clue') if f'&n={i}&' in a['href'])
        page = page.follow(link)
        page = page.submit(page.form_with('entry'), {'entry':WORDS[i]})
    page = page.action('check')
    assert "data-complete='true'" in page.html
    assert len([a for a in page.link_class('cw-clue') if 'correct' in a['class'].split()]) == 20
    assert "style='--scene:4'" in page.html
    assert "data-complete='true'" in Page(page.url).html
    page = page.action('reset')
    assert page.form_with('entry')['fields']['cw'] == '.' * size
    assert page.form_with('entry')['fields']['k'] == str(start + 2)
    assert page.form_with('entry')['fields']['s'] == '10'
    print(f'PASS crossword {start // 20 + 1}: all 20 answers, keyboard submission, validation, '
          'checks, every-cell selection, mode persistence, completion, refresh, reset.', flush=True)

# Complete the new spelling list, follow the actual Next links and keep scoring.
page = Page(urljoin(BASE, '?m=spell&n=20'))
for i in range(20, 40):
    assert f'/audio/{i}.wav' in page.audio[0]['src']
    page = page.submit(page.form_with('answer'), {'answer':WORDS[i]})
    assert "That's the word!" in page.html
    page = page.follow(next(a for a in page.link_class('btn') if 'step=' + str(i - 19) in a['href'] and '?m=spell' in a['href']))
assert 'Your batch is ready!' in page.html and "data-baked='20'" in page.html
assert "<div class='score-big'>200" in page.html
restart = next(a for a in page.link_class('btn') if '&s=0&' in a['href'])
page = page.follow(restart)
assert page.form_with('answer')['fields']['n'] == '20'
mix = page.follow(next(a for a in page.link_class('mode') if '?m=mix' in a['href']))
assert "class='scramble'" in mix.html and mix.form_with('answer')['fields']['n'] == '20'
print('PASS spelling List V: all 20 words, 200 points, 20 treats, restart, scramble, audio mapping.', flush=True)
