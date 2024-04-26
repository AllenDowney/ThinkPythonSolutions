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


tests:
	# testing notebook 04 takes too long
	cd soln; pytest --nbmake chap0[12356789]*.ipynb
	# testing notebook 12 fails on windows (unicode!)
	cd soln; pytest --nbmake chap1[1345678]*.ipynb
