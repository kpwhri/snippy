import pathlib

import click

from snippy.build import run_build
from snippy.reader import docs_from_dir


@click.command()
@click.argument('path', type=click.Path(exists=True, path_type=pathlib.Path, file_okay=False))
@click.argument('regex-file', type=click.Path(exists=True, path_type=pathlib.Path, dir_okay=False))
@click.argument('metalabels', nargs=-1, type=str, default=None)
@click.option('--context', default=180, type=int)
@click.option('--rowlimit', default=2000, type=int)
@click.option('--outpath', type=click.Path(path_type=pathlib.Path, file_okay=False), default=pathlib.Path('.'))
def main(path: pathlib.Path, regex_file: pathlib.Path, metalabels: list[str] = None,
         *, outpath=pathlib.Path('.'), context=180, rowlimit=2000):
    doc_iter = docs_from_dir(path, metalabels)
    if not metalabels:
        metalabels = next(doc_iter)
    run_build(context, doc_iter, metalabels, outpath, regex_file, rowlimit)


if __name__ == '__main__':
    main()
