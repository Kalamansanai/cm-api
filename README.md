# cm-api

We using pipenv for a virtual enviroment, to manage the packages and modules.
You need to install it. (pip install pipenv)

First you need to spawn a sell. (pipenv shell)
After the first time, you can open it again with the same command.

package installation:

- pipenv install <packagename>

before commit:

- pipenv lock

Adds every package to the Pipenv.lock you installed with pipenv install.

after pull:

- pipenv install

Its install every package that is downloaded in on other branch.
