install:
	poetry install --no-root

space-game:
	poetry run space-game

build: lint
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

lint:
	poetry run flake8 space_game