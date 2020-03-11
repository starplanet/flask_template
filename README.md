# flask_template

templates used to fast create flask project.

## install

`pip install flask_template`


# usage

`flasktemplate create [-t simple] project_name`

will create a flask project directory named after project_name on current path.

`flasktemplate list` will list current supported templates.


# update logs

## 0.4.2
1. update requirements
2. fix bugs

## 0.4.1

1. modify config.py;

2. format by pycodestyle;

## 0.4

1. add migrations directory，modify env.py script to support alembic:include, alembic:exclude 
options in alembic.ini to limit alembic dectecting tables;

2. fix some typo；
