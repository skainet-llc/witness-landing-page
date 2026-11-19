# WITNESS landing page: local helpers. The site itself is static; CI deploys it
# with .github/workflows/pages.yml.
PYTHON ?= python3
REPOS  ?= ..
FIG    := assets/fig
TMP    := build/fig

.PHONY: serve site figures clean

# Serve the repo as is (downloads section shows the "on request" fallback).
serve:
	$(PYTHON) -m http.server 8000

# Same assembly as CI into _site/; put PDFs into _site/downloads/ first to
# test the generated list.
site:
	mkdir -p _site/downloads
	cp -r index.html favicon.ico .nojekyll assets _site/
	$(PYTHON) tools/build_downloads.py _site

# Regenerate the use-case figures as SVG from the sibling use-case repos.
figures:
	$(PYTHON) tools/figures_svg.py $(REPOS)/witness-usecase-railway-points/tools/figures.py $(TMP)/railway --travel throw
	$(PYTHON) tools/figures_svg.py $(REPOS)/witness-usecase-slide-gates/tools/figures.py $(TMP)/slide-gates --travel travel
	$(PYTHON) tools/figures_svg.py $(REPOS)/witness-usecase-valves/tools/figures.py $(TMP)/valves --travel stroke
	cp $(TMP)/railway/power-curve.svg $(FIG)/railway-power-curve.svg
	cp $(TMP)/slide-gates/drift.svg   $(FIG)/slide-gates-drift.svg
	cp $(TMP)/valves/power-curve.svg  $(FIG)/valves-power-curve.svg

clean:
	rm -rf _site build
