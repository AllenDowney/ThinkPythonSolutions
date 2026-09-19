PROJECT_NAME = ThinkPythonSolutions
PYTHON_VERSION = 3.10
PYTHON_INTERPRETER = python

## Set up the environment
create_environment:
	conda create --name $(PROJECT_NAME) python=$(PYTHON_VERSION) -y
	@echo ">>> conda env created. Activate with:\nconda activate $(PROJECT_NAME)"

## Install Python Dependencies
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt


# Test every chapter. The whole suite takes about 2.5 minutes; chapter 4 is
# roughly a third of that on its own, because jupyturtle sleeps TURTLE_DELAY
# (0.2s) after each visual command and chapter 4 draws a lot. --durations
# keeps that visible, so a chapter that starts to drag is easy to spot.
#
# Use a glob rather than a list of chapter numbers: the previous version used
# two globs, chap0[12356789] and chap1[1345678], which silently left chapters
# 0, 10 and 19 untested for as long as anyone can remember.
tests:
	cd soln; pytest --nbmake --durations=5 chap*.ipynb
