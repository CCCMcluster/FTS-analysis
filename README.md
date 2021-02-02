# Camp Coordination and Camp Management analysis
This is a basic analysis of FTS financial flows to CCCM from 2005-2020.

## Installation
- Install [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html) and [Git](https://git-scm.com/downloads).
- Open the Anaconda terminal prompt and type ```git clone https://github.com/CCCMcluster/FTS-analysis.git```
- Type ```cd FTS-analysis/``` and then ```conda env create```.

## Usage
- Type ```conda activate cluster-fts``` to activate the conda environment you created above with all the installed libraries listed in *requirements.yml*
- Type ```jupyter lab``` to launch Jupyter lab in the browser.
- Click 'Run all cells' to pull the latest training data from Kobo and produce the analysis.
- Type ```jupyter nbconvert FTS-analysis.ipynb --to slides --no-input --post serve``` to show the analysis as slides.