TEX=pdflatex
BIB=bibtex
BUILD=build

SRC=SchottJordanFinalProject.tex
CONTENT=$(wildcard content/*.tex)

OUT=$(BUILD)/SchottJordanFinalProject.pdf

all: $(OUT)

$(BUILD):
	mkdir -p $(BUILD)

$(OUT): $(SRC) $(CONTENT) | $(BUILD)
	$(TEX) -output-directory=$(BUILD) $(SRC)
	$(TEX) -output-directory=$(BUILD) $(SRC)

clean:
	rm -rf $(BUILD)

.PHONY: all clean
