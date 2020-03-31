# flask_template

templates used to fast create flask project.

## install

`pip install flask_template`


# usage

`flasktemplate create [-t simple] project_name`

will create a flask project directory named after project_name on current path.

`flasktemplate create [-t mongo] project_name`

will create a flask project  directory named after project_name on current path.
mongo template will use mongodb instead of mysql.

`flasktemplate list` will list current supported templates.

normal project initial usage flow:
1. `cd {project_name}`
2. `pyenv virtualenv {python_version} {virtualenv_name}`
3. `pyenv activate {virtualenv_name}`
4. modify `SQLALCHEMY_DATABASE_URI` with correct database account and database name
5. design and develop models and migrate, apply them into database with:
    1. `python manage.py db migrate`
    2. `python manage.py db upgrade`
6. design develop apis

# update logs

## 0.4.3
1. add mongo template
	1. change db from mysql into mongodb
	2. add  hamlet user authentication, send email
	3. add celery wokers
	4. add send email,  tar/zip file,  send file
	5. add dockerfile

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
