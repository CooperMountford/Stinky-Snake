# starter-snake-python

Fork of [starter-snake-python](https://github.com/battlesnakeio/starter-snake-python)  
Based off my group's work last year in [battlesnake-python](https://github.com/rolinb/battlesnake-python)

#### You will need...

* a working Python 2.7 development environment ([getting started guide](http://hackercodex.com/guide/python-development-environment-on-mac-osx/))
* experience [deploying Python apps to Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#introduction)
* [pip](https://pip.pypa.io/en/latest/installing.html) to install Python dependencies

## Running the Snake Locally

1) [Fork this repo](https://github.com/battlesnakeio/starter-snake-python/fork).

2) Clone repo to your development environment:
```
git clone git@github.com:<your github username>/starter-snake-python.git
```

3) Install dependencies using [pip](https://pip.pypa.io/en/latest/installing.html)
```
pip install -r requirements.txt
```

4) Run local server:
```
python app/main.py
```

5) Start the battlesnake test server
```
cd battlesnake-engine
engine.exe dev  
```

6) Open the game page
```
Navigate to [localhost:3010](http://localhost:3010)
```

## Deploying to Heroku

1) Create a new Heroku app:
```
heroku create [APP_NAME]
```

2) Deploy code to Heroku servers:
```
git push heroku master
```

3) Open Heroku app in browser:
```
heroku open
```
or visit [http://APP_NAME.herokuapp.com](http://APP_NAME.herokuapp.com).

4) View server logs with the `heroku logs` command:
```
heroku logs --tail
```
