TEX=pdflatex
BUILD=build

SRC=SchottJordanFinalProject.tex
CONTENT=$(wildcard content/*.tex)
FIGURES=$(wildcard figures/*)

OUT=$(BUILD)/SchottJordanFinalProject.pdf

all: $(OUT)

$(BUILD):
	mkdir -p $(BUILD)

$(OUT): $(SRC) $(CONTENT) $(FIGURES) | $(BUILD)
	$(TEX) -output-directory=$(BUILD) $(SRC)
	$(TEX) -output-directory=$(BUILD) $(SRC)

clean:
	rm -rf $(BUILD)

.PHONY: all clean
