"""Independently validate both spelling-list crossword geometries (development only)."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
game = (root / 'src/game.u').read_text(encoding='utf-8')
source = (root / 'src/crossword.u').read_text(encoding='utf-8')
deck = re.findall(r'Card "([a-z]+)"', game.split('pop.word :')[0])
assert len(deck) == len(set(deck)) == 40
assert deck[20:] == ('unborn unlock resell imperfect subway supersize unchain rewash '
                    'indirect overact premix unblock unload relearn rewind incorrect '
                    'overheat illegal transmit interact').split()

def validate(name, start, rows, columns):
    definition = source.split(f'cross.{name} =', 1)[1].split('  ]', 1)[0]
    entries = [(int(i), int(n), int(r), int(c), direction == 'true')
               for i, n, r, c, direction in re.findall(
                   r'CrossEntry (\d+) (\d+) (\d+) (\d+) (true|false)', definition)]
    assert len(entries) == 20
    assert sorted(e[0] for e in entries) == list(range(start, start + 20)), 'Every word must appear once'
    board, owners, graph = {}, {}, {i: set() for i in range(start, start + 20)}
    starts = sorted({(r, c) for _, _, r, c, _ in entries})
    expected_runs = set()
    for i, number, row, col, across in entries:
        assert number == starts.index((row, col)) + 1, 'Incorrect clue numbering'
        cells = tuple((row + (0 if across else offset), col + (offset if across else 0))
                      for offset in range(len(deck[i])))
        expected_runs.add((across, cells))
        for point, letter in zip(cells, deck[i]):
            assert 0 <= point[0] < rows and 0 <= point[1] < columns, 'Out of bounds'
            assert point not in board or board[point] == letter, 'Crossing letters disagree'
            for old_index, old_across in owners.get(point, []):
                assert across != old_across, 'Parallel words overlap'
                graph[i].add(old_index)
                graph[old_index].add(i)
            board[point] = letter
            owners.setdefault(point, []).append((i, across))
    assert all(graph.values()), 'Every word must cross another word'
    reached, pending = set(), [start]
    while pending:
        current = pending.pop()
        if current in reached:
            continue
        reached.add(current)
        pending.extend(graph[current] - reached)
    assert len(reached) == 20, 'The puzzle must form one connected grid'
    actual_runs = set()
    for row, col in board:
        for across, dr, dc in [(True, 0, 1), (False, 1, 0)]:
            if (row - dr, col - dc) in board:
                continue
            run, r, c = [], row, col
            while (r, c) in board:
                run.append((r, c))
                r, c = r + dr, c + dc
            if len(run) > 1:
                actual_runs.add((across, tuple(run)))
    assert actual_runs == expected_runs, 'Unclued runs or accidentally joined words'
    print(f'PASS {name}: all 20 spelling words, {len(board)} letter cells, valid crossings, clue numbers, '
          'one connected grid, no unintended words.')

widths = re.search(r'cross.width n = if n < 20 then (\d+) else (\d+)', source).groups()
heights = re.search(r'cross.height n = if n < 20 then (\d+) else (\d+)', source).groups()
for i, name in enumerate(['original', 'prefixes']):
    validate(name, i * 20, int(heights[i]), int(widths[i]))
