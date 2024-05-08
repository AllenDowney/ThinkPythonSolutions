import sys
import nbformat as nbf

header_filename = sys.argv[1]
notebook_filename = sys.argv[2]

header = nbf.read(header_filename, nbf.NO_CONVERT)
notebook = nbf.read(notebook_filename, nbf.NO_CONVERT)

notebook.cells = header.cells + notebook.cells

print('Adding', header_filename, 'to', notebook_filename)
nbf.write(notebook, notebook_filename)
