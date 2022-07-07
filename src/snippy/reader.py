import json
import pathlib

import sqlalchemy as sa


class Document:

    def __init__(self, text: str, meta: dict[str]):
        self.meta = meta
        self.text = text

    @classmethod
    def fromlists(cls, text: str, metalabels: list[str], metavalues: list[str]):
        return cls(text, {label: value for label, value in zip(metalabels, metavalues)})


def docs_from_db(connection_string: str, metalabels: list[str], tablename: str):
    query_string = f", {','.join(metalabels)}" if metalabels else ''
    eng = sa.create_engine(connection_string)
    for text, *meta in eng.execute(f'select note_text {query_string} from {tablename}'):
        yield Document.fromlists(text, metalabels, meta)


def docs_from_dir(path: pathlib.Path, metalabels: list[str] = None, *, metasuffix='meta', encoding='utf8'):
    if metalabels and '_docid' not in metalabels:
        metalabels.insert(0, '_docid')
    for file in path.iterdir():
        if file.is_dir() or file.suffix not in {'', '.txt'}:
            continue
        with open(file, encoding=encoding) as fh:
            text = fh.read()
        data = {}
        if (metafile := file.parent / f'{file.stem}.{metasuffix.strip(".")}').exists():
            with open(metafile, encoding=encoding) as fh:
                data = json.load(fh)
        data['_docid'] = file.stem
        if metalabels:
            data = {k: v for k, v in data.items() if k in metalabels}
        else:
            metalabels = list(data.keys())
            if '_docid' in metalabels:
                metalabels.remove('_docid')
            metalabels.insert(0, '_docid')
            yield metalabels
        yield Document(text, data)
