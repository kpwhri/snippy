import pathlib
from collections import defaultdict

import click

from snippy.reader import docs_from_db
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
        if min(counters.values()) >= rowlimit:  # stop when found enough of everything
            break


@click.command()
@click.argument('connection-string', type=str)
@click.argument('tablename', type=str)
@click.argument('regex-file', type=click.Path(exists=True, path_type=pathlib.Path, dir_okay=False))
@click.argument('metalabels', nargs=-1, type=str)
@click.option('--context', default=180, type=int)
@click.option('--rowlimit', default=2000, type=int)
@click.option('--outpath', type=click.Path(path_type=pathlib.Path, file_okay=False), default=pathlib.Path('.'))
def main(connection_string: str, regex_file: pathlib.Path, metalabels: list[str], tablename: str,
         *, outpath=pathlib.Path('.'), context=180, rowlimit=2000):
    outpath.mkdir(exist_ok=True, parents=True)
    metalabels = list(metalabels)
    doc_iter = docs_from_db(connection_string, metalabels, tablename)
    regexes = load_regexes(regex_file)
    labels = [label for label, _ in regexes]
    csv_dict = prepare_writers(labels, outpath, metalabels)
    build(doc_iter, regexes, csv_dict, context=context, rowlimit=rowlimit)


if __name__ == '__main__':
    main()
