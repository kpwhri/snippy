import sqlalchemy as sa


class Document:

    def __init__(self, text: str, metalabels: list[str], metavalues: list[str]):
        self.meta = {label: value for label, value in zip(metalabels, metavalues)}
        self.text = text


def docs_from_db(connection_string: str, metalabels: list[str], tablename: str):
    query_string = f", {','.join(metalabels)}" if metalabels else ''
    eng = sa.create_engine(connection_string)
    for text, *meta in eng.execute(f'select note_text {query_string} from {tablename}'):
        yield Document(text, metalabels, meta)
