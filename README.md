# cm-api

We using pipenv for a virtual enviroment, to manage the packages and modules.
You need to install it.
`pip install pipenv`

First you need to spawn a sell. (pipenv shell)
After the first time, you can open it again with the same command.
`pipenv shell`

package installation:

`pipenv install <packagename>`

before commit:

`pipenv lock`

Adds every package to the Pipenv.lock you installed with pipenv install.

after pull:

`pipenv install`

Its install every package that is downloaded in on other branch.

# Running the app

`python app.py`

# How to make a requirements.txt

`pipenv lock -r > requirements.txt`

# DOCKER

sudo docker build -t cm-api/init .
sudo docker run -p 3214:3214 cm-api/init