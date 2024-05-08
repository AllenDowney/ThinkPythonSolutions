.PHONY: compile_book convert_book

compile_book:
	pdflatex main.tex && evince main.pdf

convert_book:
	cp ../soln/chap*.ipynb .
	sh build.sh chap*.ipynb