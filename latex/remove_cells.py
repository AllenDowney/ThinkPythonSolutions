import sys
import nbformat as nbf

filename = sys.argv[1]
print('Clearing cells from', filename)
ntbk = nbf.read(filename, nbf.NO_CONVERT)


def remove_input(cell):
    cell['source'] = ''


def remove_output(cell):
    if hasattr(cell, 'outputs'):
        cell['outputs'] = []
    if hasattr(cell, 'execution_count'):
        cell['execution_count'] = 0


def remove_both(cell):
    cell['source'] = ''
    if hasattr(cell, 'outputs'):
        del cell['outputs']
    if hasattr(cell, 'execution_count'):
        del cell['execution_count']


def clip_output(cell):
    """Clip each lines of the output to the first 80 characters.

    This has not been tested.
    """
    for output in cell.get('outputs', []):
        data = output.get('data', {})
        if 'text/plain' in data:
            lines = [line[:80] for line in data['text/plain'].split('\n')]
            data['text/plain'] = '\n'.join(lines)


def truncate_output(cell):
    """Remove all but the first lines.
    """
    for output in cell.get('outputs', []):
        data = output.get('data', {})
        if 'text/plain' in data:
            lines = data['text/plain'].split('\n')
            data['text/plain'] = '\n'.join(lines[:6])
    #print(cell['outputs'])


for cell in ntbk.cells:

    # if a cell has a remove-cell tag, remove the source and outputs
    cell_tags = cell.get('metadata', {}).get('tags', [])
    #print(cell_tags)
    if ('remove-input' in cell_tags or
        'hide-input' in cell_tags ):
        remove_input(cell)

    if ('remove-output' in cell_tags or
        'hide-output' in cell_tags ):
        remove_output(cell)

    if ('clip-output' in cell_tags):
        clip_output(cell)

    if ('truncate-output' in cell_tags):
        truncate_output(cell)

    if ('remove-cell' in cell_tags or
        'hide-cell' in cell_tags or
        'remove-print' in cell_tags):
        remove_both(cell)
        cell['cell_type'] = 'raw'



nbf.write(ntbk, filename)
