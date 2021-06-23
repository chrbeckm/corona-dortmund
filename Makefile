GOOGLEPATH=/mnt/e/cloud-google/corona

all: build/insta_story.png \
	build/dortmund.pdf \
	build/bezirke_insta.png \
	build/r-wert.pdf \
	build/altersinzidenz.pdf \
	build/virusvarianten.pdf \
	copy

build/FB53-Coronafallzahlen.csv: FORCE | build
	rm -f $@
	wget https://opendata.dortmund.de/OpenDataConverter/download/Gesundheit/FB53-Coronafallzahlen.csv -P build
	sed -i 's/,/./g' $@

build/FB53-Coronafallzahlen-Stadtbezirke.csv: FORCE | build
	wget https://opendata.dortmund.de/OpenDataConverter/download/Gesundheit/FB53-Coronafallzahlen%20Stadtbezirke.csv -P build
	mv 'build/FB53-Coronafallzahlen Stadtbezirke.csv' $@
	sed -i 's/,/./g' $@

build/FB53-Coronafallzahlen-R-Wert.csv: FORCE | build
	wget https://opendata.dortmund.de/OpenDataConverter/download/Gesundheit/FB53-Coronafallzahlen%20R-Wert.csv -P build
	mv 'build/FB53-Coronafallzahlen R-Wert.csv' $@
	sed -i 's/,/./g' $@

build/FB53-Coronafallzahlen-Altersinzidenzen.csv: FORCE | build
	wget https://opendata.dortmund.de/OpenDataConverter/download/Gesundheit/FB53-Coronafallzahlen%20Altersinzidenzen.csv -P build
	mv 'build/FB53-Coronafallzahlen Altersinzidenzen.csv' $@

build/FB53-Coronafallzahlen-Virusvarianten.csv: FORCE | build
	wget https://opendata.dortmund.de/OpenDataConverter/download/Gesundheit/FB53-Coronafallzahlen%20Virusvarianten.csv -P build
	mv 'build/FB53-Coronafallzahlen Virusvarianten.csv' $@


build/insta_story.png: python/insta_story.py build/FB53-Coronafallzahlen.csv | build
	TEXINPUTS="$$(pwd):" python python/insta_story.py

build/faelle-pro-tag.pdf: python/dortmund_tex.py build/FB53-Coronafallzahlen.csv | build
	TEXINPUTS="$$(pwd):" python python/dortmund_tex.py

build/dortmund.pdf: FORCE  build/faelle-pro-tag.pdf | build
		TEXINPUTS=build: \
		max_print_line=1048576 \
	latexmk \
		--lualatex \
	  --output-directory=build \
	  --interaction=batchmode \
	  --halt-on-error \
	tex/dortmund.tex


build/bezirke_insta.png: python/stadtbezirke.py build/FB53-Coronafallzahlen-Stadtbezirke.csv | build
	TEXINPUTS="$$(pwd):" python python/stadtbezirke.py

build/r-wert.pdf: python/r-wert.py build/FB53-Coronafallzahlen-R-Wert.csv | build
	TEXINPUTS="$$(pwd):" python python/r-wert.py

build/altersinzidenz.pdf: python/altersinzidenz.py build/FB53-Coronafallzahlen-Altersinzidenzen.csv | build
	TEXINPUTS="$$(pwd):" python python/altersinzidenz.py

build/virusvarianten.pdf: python/virusvarianten.py build/FB53-Coronafallzahlen-Virusvarianten.csv | build
	TEXINPUTS="$$(pwd):" python python/virusvarianten.py


copy:
	cp build/*.pdf $(GOOGLEPATH)
	rm -r python-png
	cp -r python python-png
	for file in python-png/*; do \
		echo $${file}; \
		sed -i 's/(constrained_layout=True)/(constrained_layout=True, figsize=(5, 5))/g' $$file; \
	  sed -i 's/.pdf"/.png", dpi=333/g' $$file; \
		TEXINPUTS="$$(pwd):" python $$file; \
	done
	cp build/*.png $(GOOGLEPATH)


clean:
	rm -rf build

build:
	mkdir -p build

FORCE:

.PHONY: FORCE all clean copy
