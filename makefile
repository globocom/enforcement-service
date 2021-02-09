all-tests: tests coverage generate

tests:
	pipenv run coverage run -m unittest discover -s test -v
coverage: tests
	pipenv run coverage report -m 
generate: coverage
	pipenv run coverage html