PDFLATEX ?= pdflatex
BIBTEX ?= bibtex
PYTHON ?= python3

.PHONY: all pdf supplement test clean

all: pdf supplement

pdf: main.pdf

supplement: mti-extensions-supplement.pdf

test:
	$(PYTHON) -B -m unittest discover -s tests -v

main.pdf: main.tex refs.bib
	$(PDFLATEX) -interaction=nonstopmode -halt-on-error main.tex
	$(BIBTEX) main
	$(PDFLATEX) -interaction=nonstopmode -halt-on-error main.tex
	$(PDFLATEX) -interaction=nonstopmode -halt-on-error main.tex

mti-extensions-supplement.pdf: mti-extensions-supplement.tex refs.bib
	$(PDFLATEX) -interaction=nonstopmode -halt-on-error mti-extensions-supplement.tex
	$(BIBTEX) mti-extensions-supplement
	$(PDFLATEX) -interaction=nonstopmode -halt-on-error mti-extensions-supplement.tex
	$(PDFLATEX) -interaction=nonstopmode -halt-on-error mti-extensions-supplement.tex

clean:
	rm -f *.aux *.bbl *.blg *.fdb_latexmk *.fls *.log *.out *.synctex.gz *.toc
