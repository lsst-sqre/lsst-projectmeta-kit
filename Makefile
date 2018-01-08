.PHONY: test

test:
	pytest --flake8 --doctest-modules lsstprojectmeta tests
