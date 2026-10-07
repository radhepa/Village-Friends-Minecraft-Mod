"""Compiles the residents' handwritten dialogue into data/villagefriends/villagefriends/dialogue.json.

Sources are plain text, easy to write and review:

  tools/dialogue/lines/*.txt       pools of lines, under "## pool.key" headings
  tools/dialogue/questions/*.txt   questions residents ask (and offers they make), with your possible answers

Lines:
    ## work.farmer
    The carrots came up crooked this year. I like them better that way.
    # a comment

Questions ("?" asks once ever; "!" is an offer that can come up once a day when its conditions hold):
    ? sunrise | when: morning
    Q: Be honest. Are you a sunrise person or a sunset person?
    - Sunrise, always :: Me too! The whole village is pink for a minute. @likes:sunrise
    - Sunset :: Then you'd love the view from the bell tower around six.
    - Whichever has breakfast :: Ha! A practical answer. {points:1}

Answers are "Label :: reply". After the reply, "@flag" is remembered about you, "{effect}" does
something (see Talk.java), "{points:N}" adds friendship and "[MOOD]" picks the speech bubble.
"when:" lists context tags that must all hold ("!rain" means not raining, "level:4" means friendship
level 4 or more). Placeholders like {name}, {player}, {village}, {friend}, {item} are filled from the
world; a line whose placeholder can't be filled is skipped.

    python tools/dialogue/dialogue.py           # compile
    python tools/dialogue/dialogue.py --check   # validate and confirm the compiled file is current
    python tools/dialogue/dialogue.py --stats   # counts by pool family
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
OUT = PROJECT / 'src/main/resources/data/villagefriends/villagefriends/dialogue.json'
PLACEHOLDERS = {'name', 'player', 'village', 'job', 'hobby', 'love', 'friend', 'partner', 'rival', 'time', 'day', 'item', 'biome', 'moon', 'market', 'neighbor', 'weekday'}
MOODS = {'EXCLAIM', 'QUESTION', 'HEART', 'NOTE', 'ANGER', 'SWEAT', 'DOTS', 'SLEEP', 'SPARKLE', 'IDEA', 'GLOOM', 'BLUSH'}
EFFECTS = {'heal', 'meal', 'shelter', 'torch', 'cook_held', 'mend_held', 'directions', 'fish', 'study', 'flower', 'apple', 'bread', 'cookie', 'seeds', 'emerald_tip'}
MAX_LINE, MAX_LABEL = 300, 30


def fail(where, message):
    raise SystemExit(f'{where}: {message}')


def check_text(where, text, limit=MAX_LINE):
    if not text.strip():
        fail(where, 'empty text')
    if len(text) > limit:
        fail(where, f'too long ({len(text)} > {limit}): {text[:60]}...')
    for name in re.findall(r'\{([a-z_]+)\}', text):
        if name not in PLACEHOLDERS:
            fail(where, f'unknown placeholder {{{name}}}')
    if text.count('{') != text.count('}'):
        fail(where, 'unbalanced braces')


def read_lines():
    pools = {}
    for path in sorted((ROOT / 'lines').glob('*.txt')):
        key = None
        for n, raw in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
            line = raw.strip()
            where = f'{path.name}:{n}'
            if not line or line.startswith('# ') or line == '#':
                continue
            if line.startswith('## '):
                key = line[3:].strip()
                if not re.fullmatch(r'[a-z0-9_.]+', key):
                    fail(where, f'bad pool key {key!r}')
                pools.setdefault(key, [])
                continue
            if key is None:
                fail(where, 'line before any "## pool" heading')
            check_text(where, line)
            pools[key].append(line)
    return pools


ANSWER = re.compile(r'^-\s*(.+?)\s*::\s*(.+)$')


def parse_answer(where, text):
    m = ANSWER.match(text)
    if not m:
        fail(where, 'answers look like "- Label :: reply"')
    label, reply = m.group(1).strip(), m.group(2).strip()
    answer = {'label': label}
    for flag in re.findall(r'\s@([a-z0-9_:]+)', ' ' + reply):
        answer['flag'] = flag
    reply = re.sub(r'\s*@[a-z0-9_:]+', '', reply)
    for effect in re.findall(r'\{(?:effect:)?([a-z_]+)(?::(-?\d+))?\}', reply):
        name, value = effect
        if name == 'points':
            answer['points'] = int(value or 1)
        elif name in EFFECTS:
            answer['effect'] = name
        elif name in PLACEHOLDERS:
            continue
        else:
            fail(where, f'unknown effect {{{name}}}')
    reply = re.sub(r'\s*\{(?:effect:)?(?:points|' + '|'.join(EFFECTS) + r')(?::-?\d+)?\}', '', reply)
    mood = re.search(r'\s*\[([A-Z]+)\]\s*', reply)
    if mood:
        if mood.group(1) not in MOODS:
            fail(where, f'unknown mood [{mood.group(1)}]')
        answer['mood'] = mood.group(1)
        reply = (reply[:mood.start()] + ' ' + reply[mood.end():]).strip()
    check_text(where, label, MAX_LABEL)
    check_text(where, reply)
    answer['reply'] = reply.strip()
    return answer


def read_questions():
    questions, ids = [], set()
    for path in sorted((ROOT / 'questions').glob('*.txt')):
        current = None
        for n, raw in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
            line = raw.strip()
            where = f'{path.name}:{n}'
            if not line or line.startswith('# ') or line == '#':
                continue
            if line[0] in '?!' and (len(line) == 1 or line[1] == ' '):
                head = [part.strip() for part in line[1:].split('|')]
                qid = head[0]
                if not re.fullmatch(r'[a-z0-9_]{2,40}', qid):
                    fail(where, f'bad question id {qid!r}')
                if qid in ids:
                    fail(where, f'duplicate question id {qid}')
                ids.add(qid)
                when = []
                for part in head[1:]:
                    if part.startswith('when:'):
                        when += part[5:].split()
                    else:
                        fail(where, f'unknown question option {part!r}')
                current = {'id': qid, 'offer': line[0] == '!', 'when': when, 'ask': [], 'answers': []}
                questions.append(current)
                continue
            if current is None:
                fail(where, 'text before a "? id" heading')
            if line.startswith('Q:'):
                text = line[2:].strip(); check_text(where, text); current['ask'].append(text)
            elif line.startswith('-'):
                current['answers'].append(parse_answer(where, line))
            else:
                fail(where, f'expected "Q:" or "- answer": {line[:40]}')
    for q in questions:
        if not q['ask'] or not 2 <= len(q['answers']) <= 4:
            fail(q['id'], 'each question needs a "Q:" line and 2-4 answers')
    return questions


def compile_all():
    pools, questions = read_lines(), read_questions()
    seen = Counter(line for lines in pools.values() for line in lines)
    duplicates = [line for line, count in seen.items() if count > 1]
    if duplicates:
        fail('lines', f'{len(duplicates)} duplicate lines, e.g. {duplicates[0]!r}')
    return {'format': 1, 'pools': pools, 'questions': questions}


def count(data):
    lines = sum(len(v) for v in data['pools'].values())
    asks = sum(len(q['ask']) for q in data['questions'])
    answers = sum(len(q['answers']) for q in data['questions'])
    return lines, asks, answers


def render(data):
    return json.dumps(data, ensure_ascii=False, indent=0, separators=(',', ':')) + '\n'


def main():
    data = compile_all()
    lines, asks, answers = count(data)
    total = lines + asks + answers * 2
    if '--stats' in sys.argv:
        families = Counter()
        for key, values in data['pools'].items():
            families[key.split('.')[0]] += len(values)
        for family, n in families.most_common():
            print(f'{family:12} {n}')
        print(f'questions    {len(data["questions"])} ({asks} asks, {answers} answers)')
    if '--check' in sys.argv:
        if not OUT.exists() or OUT.read_text(encoding='utf-8') != render(data):
            raise SystemExit('dialogue.json is out of date: run python tools/dialogue/dialogue.py')
        print(f'Dialogue is up to date: {total} pieces of dialogue ({lines} lines, {len(data["questions"])} questions with {answers} answers).')
        return
    OUT.write_text(render(data), encoding='utf-8')
    print(f'Dialogue: {total} pieces of dialogue: {lines} lines in {len(data["pools"])} pools, {len(data["questions"])} questions with {answers} answers and replies.')


if __name__ == '__main__':
    main()
