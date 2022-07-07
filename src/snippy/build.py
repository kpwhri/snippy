from collections import defaultdict

from snippy.regex import load_regexes
from snippy.writer import prepare_writers


def build(doc_iter, regexes, csv_dict, context=180, rowlimit=2000):
    counters = defaultdict(int)
    duplicates = defaultdict(set)
    for doc in doc_iter:
        for label, rx in regexes:
            if counters[label] > rowlimit:
                continue
            for m in rx.finditer(doc.text):
                precontext = ' '.join(doc.text[max(0, m.start() - context): m.start()].strip().split())
                if len(precontext) > 20:
                    if precontext in duplicates[label]:
                        continue
                    else:
                        duplicates[label].add(precontext)
                csv_dict[label].write(doc.meta | {
                    'id': counters[label],
                    'precontext': precontext,
                    'keyword': ' '.join(m.group().split()),
                    'postcontext': ' '.join(doc.text[m.end():m.end() + context].strip().split()),
                })
                counters[label] += 1
        if counters and min(counters.values()) >= rowlimit:  # stop when found enough of everything
            break


def run_build(context, doc_iter, metalabels, outpath, regex_file, rowlimit):
    metalabels = list(metalabels)
    outpath.mkdir(exist_ok=True, parents=True)
    regexes = load_regexes(regex_file)
    labels = [label for label, _ in regexes]
    if len(labels) == 0:
        raise ValueError('No labels found in regular expression file.')
    csv_dict = prepare_writers(labels, outpath, metalabels)
    build(doc_iter, regexes, csv_dict, context=context, rowlimit=rowlimit)
