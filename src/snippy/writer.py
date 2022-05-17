import csv
import datetime
import pathlib


class Writer:

    def __init__(self, outpath: pathlib.Path, label: str, dt: str, metacolumns: list[str], encoding='utf8'):
        self.outpath = outpath / f'{label}_{dt}.csv'
        self.fh = open(self.outpath, 'w', newline='', encoding=encoding)
        self.writer = csv.DictWriter(
            self.fh,
            fieldnames=['id'] + metacolumns + ['precontext', 'keyword', 'postcontext']
        )
        self.writer.writeheader()

    def write(self, data: dict):
        self.writer.writerow(data)

    def __del__(self):
        self.fh.close()


def prepare_writers(labels, outpath: pathlib.Path, metacolumns: list[str]):
    dt = datetime.datetime.now().strftime('%Y%m%d')
    d = {}
    for label in labels:
        d[label] = Writer(outpath, label, dt, metacolumns)
    return d
