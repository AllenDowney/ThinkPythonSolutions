import sys
import re

# replace figure URLs with references to local files
# for source listings in Python, add `style=source`
# for output listings, add `style=output`

subs = {
r'\\includegraphics(.*){https://.*/([^/]*)}': r'\\includegraphics\1{figs/\2}',
r'\\includegraphics(.*){figs/([^/]*)}': r'\\includegraphics\1{figs/\2}',
r'language=Python': r'language=Python,style=source',
r'begin{lstlisting}$': r'begin{lstlisting}[style=output]',
'\ufeff': '',
r'\\tightlist': '',
r'\\toprule': r'\\midrule',
r'\\bottomrule': r'\\midrule',
}

def write_line(fout, line):
    for pattern, repl in subs.items():
        line = re.sub(pattern, repl, line)

    fout.write(line + '\n')

def write_chapter(t):
    fout = open(filename, 'w')
    i = 0

    while i < len(t):
        line = t[i]
        if line.startswith('\\backmatter'):
            fout.close()
            return i

        write_line(fout, line)
        i += 1

    fout.close()
    return i

filename = sys.argv[1]

lines = open(filename).read()

# remove an input cell if it's totally empty
pattern = r"""
\\begin{lstlisting}\[language=Python\]
\\end{lstlisting}"""

repl = r''

lines = re.sub(pattern, repl, lines)

# replace figure environments with center environments
pattern = r"""\\begin{figure}
\\centering
\\includegraphics{(.*)}
\\caption{.*}
\\end{figure}"""

repl = r"""\\begin{center}
\\includegraphics[]{\1}
\\end{center}"""

lines = re.sub(pattern, repl, lines)

t = lines.split('\n')

i = 0
while i < len(t):
    line = t[i]
    if line.startswith('\\chapter'):
        i = write_chapter(t[i:])
    else:
        i += 1
