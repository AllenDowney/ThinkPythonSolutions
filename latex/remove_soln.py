import sys
import nbformat as nbf

filename = sys.argv[1]
ntbk = nbf.read(filename, nbf.NO_CONVERT)

keep_cells = []

for cell in ntbk.cells:
    # skip empty cells
    source = cell['source']
    if len(source) == 0:
        continue

    # skip solutions
    if source.startswith('# Solution'):
        continue

    keep_cells.append(cell)

ntbk.cells = keep_cells

print('Removing solutions from', filename)
nbf.write(ntbk, filename)
