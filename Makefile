PDFLATEX ?= pdflatex
BIBTEX ?= bibtex

.PHONY: all pdf supplement clean

all: pdf supplement

pdf: main.pdf

supplement: mti-extensions-supplement.pdf

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
