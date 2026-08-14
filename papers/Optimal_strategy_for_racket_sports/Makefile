# Build the paper with pandoc, using Typst (via the official IEEE
# "charged-ieee" template) as the PDF engine.
#
# Usage:
#   > make            # build paper.pdf
#   > make figures    # regenerate figures/*.png
#   > make clean      # remove build artifacts

PANDOC = pandoc
SRC = paper.md
TEMPLATE = templates/ieee-template.typ
OUT = paper.pdf

.PHONY: all figures clean

all: $(OUT)

$(OUT): $(SRC) $(TEMPLATE) references.bib figures/trajectory_schematic.png figures/toy_example_scores.png
	$(PANDOC) $(SRC) \
		--from markdown+smart \
		--template $(TEMPLATE) \
		--to typst \
		--pdf-engine typst \
		-o $(OUT)

figures: figures/make_figures.py
	python3 figures/make_figures.py

clean:
	rm -f $(OUT)
