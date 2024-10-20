# To run the commands in this file, "just command runner" is required to be installed with "brew install just".
# To view the available commands, run "just -l"
# To setup the environment, it requires pyenv to be installed with "brew install pyenv"

# Set environment variables
# set dotenv-required
# set dotenv-load

python_version := `cat .python-version`

# Set python virtual environment
setup:
    @pyenv local {{python_version}}
    @brew install pipx && pipx ensurepath
    @pipx install "poetry==1.8.3" && poetry env use {{python_version}}
    @poetry install

# Format the code
format:
    @poetry run ruff format .

# Lint the code
lint:
    @-poetry run ruff check . --fix