# cm-api

package installation:

- pipenv install <packagename>

before commit:

- pipenv lock

Adds every package to the Pipenv.lock you installed with pipenv install.

after pull:

- pipenv install -dev

Its install every package that is downloaded in on other branch.
