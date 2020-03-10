- [Project Basics](#project-basics)
- [Setup](#setup)
  * [Software Dependencies](#software-dependencies)
  * [Setup *legalfit* `pyenv` environment](#setup-legalfit-pyenv-environment)
  * [Install python packages](#install-python-packages)
  * [Set your local server to run from <u>legalfit.local</u> and <u>admin.local</u>](#set-your-local-server-to-run-from-ulegalfitlocalu-and-uadminlocalu)
  * [Setup your PostgreSQL](#setup-your-postgresql)
  * [Manually load the database](#manually-load-the-database)
  * [Setup job queues](#setup-job-queues)
  * [Setup SASS compiler](#setup-sass-compiler)
- [Usage](#usage)
  * [Pipenv](#pipenv)
  * [Install python packages](#install-python-packages-1)
  * [Check security vulnerabilities](#check-security-vulnerabilities)
  * [Updating python package](#updating-python-package)
  * [Adding python packages](#adding-python-packages)
  * [Database](#database)
  * [View job queues](#view-job-queues)
  * [Download prod data to your local environment](#download-prod-data-to-your-local-environment)
  * [Front-end](#front-end)
  * [CSS: Run SASS compiler](#css-run-sass-compiler)
- [Notes](#notes)
    + [Environment](#environment)
  * [How Django Settings work](#how-django-settings-work)
    + [Front-End](#front-end-1)
  * [FusionCharts](#fusioncharts)
  * [Maisionette Theme](#maisionette-theme)
  
# Project Basics

* #### Legalfit is split into 2 main UI views

   * Team-only CRM View
      - Production: https://crm.legalfit.io/
      - Development: http://localhost:8000/
     
   * Customer Dashboard View
     - Production: https://dashboard.legalfit.io/
     - Development: http://dashboard.local:8000/

* #### Django Configuration

    a. Because there are many environments, viz. development, testing, staging and production
       environments, and for security configuration there is a configuration
       file hierarchy using YAML files. These YAML files are merged together
       and the settings can be modified like any normal Django project
       (e.g. `settings.DEBUG`)
       
    b. File priorities:
    
    `legalfit/settings/base.yml`
    `legalfit/settings/$ENVIRONMENT.yml`
    `legalfit/settings/local/base.yml` (in `.gitignore`)
    `legalfit/settings/local/$ENVIRONMENT.yml` (in `.gitignore`)


# Setup

## Software Dependencies

### Mac

##### Redis
- `brew install redis`
- `brew services start redis`
##### PostgreSQL
- `brew install postgresql`
- `brew services start postgresql`
##### Memcached
- `brew install memcached`
- `brew services start memcached`
      
### Ubuntu
##### Update Packages
- `sudo apt update`
##### Install Redis, Memcached and PostgreSQL
- `sudo apt install redis-server memcached postgresql postgresql-contrib`

## Setup *legalfit* `pyenv` environment 
1. see [toolbox](https://github.com/big6media/toolbox/blob/master/README.md#0-setup-python-environment) for detailed instructions

2. `pyenv virtualenv 3.7.2 legalfit`

## Install python packages

* `pip install pipenv`
* `pipenv sync --dev`

## Set your local server to run from <u>legalfit.local</u> and <u>admin.local</u>

- Add `127.0.0.1   dashboard.local` to `/etc/hosts`
- Create and Populate `legalfit/settings/local/base.yaml` for environment specific settings (e.g. api keys, database config, etc) (use `legalfit/settings/local_base.example` as reference)
    - Below is an example dashboard domain configuration:

```yaml
...
allowed_hosts:
    - localhost
    - dashboard.local

legalfit_portal_url: 'http://dashboard.local:8000'
...
```

## Setup your PostgreSQL

1. setup postgres user/password
    - Mac: Default `brew` install creates user `$USER` with no password
    - Linux
```
$ sudo -i -u postgres
$ createuser --interactive
Enter name of role to add: bill
Shall the new role be a superuser? (y/n) y
$ psql
postgres=# ALTER USER bill WITH PASSWORD 'bill';
postgres=# \q
$ exit

```
2. set local postgresql user in `settings/local/base.yaml`
3. `createdb legalfit`
4. `./manage.py load_database`
    - This assumes the `toolbox` repository is configured and is in the same
      parent folder as the `legalfit` repository (Use `settings.TOOLBOX_LOCATION` to specify a different location)
5. `./manage.py createsuperuser` to create a user for testing
6. `./manage.py runserver`

Navigate to `http://localhost:8000` or `http://legalfit.local`

## Manually load the database
Manual installation of database
```
$ dropdb legalfit
$ createdb legalfit

# this loads the database and keeps /tmp/legalfit.sql if don't want to download and unzip it again
~/projects/toolbox> ./restore_postgres legalfit --require_env staging --keep-temp
~/projects/legalfit> ./manage.py migrate

# assuming you have /tmp/legalfit.sql from previous command, here is how you load it
$ dropdb legalfit
$ createdb legalfit
$ psql legalfit < /tmp/legalfit.sql
~/projects/legalfit> ./manage.py migrate
```


## Setup job queues

Typically in alternate terminal tabs, when testing at a macro level

- `./manage.py task_queue_celery`Celery job queue
- `./manage.py task_queue_throttled` Celery throttled queue

## Setup SASS compiler

- Install `node` (`brew install nodejs`)
- `cd 3rdparty/maisonnette`
- `npm install`

# Usage

Common scenarios to be productive as a dev on this project

## Pipenv

## Install python packages

- `pipenv sync --dev`

## Check security vulnerabilities

- `pipenv check`

## Updating python package

- `pipenv update` or `pipenv update <package_name>`

## Adding python packages

- Development only: `pipenv install --dev <package_name>`
- Production:
  - `pipenv install <package_name>`
  - `pipenv lock --requirements > requirements.txt`

## Database

## View job queues

- `./manage.py task_queue_monitor` Celery monitor frontend http://localhost:5555

## Download prod data to your local environment

- Disconnect all of the things from the DB (workers/test webservers/pg admin)
- `dropdb legalfit`
- `createdb legalfit`
- `cd ~/projects/toolbox && ./postgres_restore legalfit --restore_env production`
- `cd ~/projects/legalfit && ./manage.py migrate`

## Front-end

## CSS: Run SASS compiler

`portal/static/css/app_generated.css` is generated dynamically, don't update it directly as the next
generation will just undo everything, instead update `portal/static/css/main.scss`.

- In a new terminal window, go to `3rdparty/maisonnette`
-  `npm run-script big6`
  - Monitors `.scss` in `portal/static/css` for changes and compiles to `app.css` and `app.css.map`
- Make changes to `.scss` files in `portal/static/css``
- Upon saving a new `app.css` will be generated be sure to commit
  - Refer to `3rdparty/maissonnette/src/sass/config/_maisonnette-variables.scss` for all of the maisonnette variables
  - `3rdparty/maisonnette/src/assets/lib` is generated by `npm install` and is the default assets
    for all of the plugins as reference

# Notes

### Environment

## How Django Settings work

Most of the Django and Wagtail settings have been moved to yaml files in `legalfit/settings`.

The precedence order of settings files:

- base.yaml
- ENVIRONMENT.yaml
- local/base.yaml
- local/ENVIRONMENT.yaml

Files in `settings/local` are not added to the repository. The `*.example` files
in the settings folder should have starter local settings to get the project go

## Front-End

### FusionCharts

- Galleries:
  - [Chart Gallery](https://www.fusioncharts.com/charts?product=fusioncharts) pretty product demos
  - [Chart Gallery](https://www.fusioncharts.com/dev/demos/chart-gallery#Gallary) for designers by intent good for picking out what to use

- Documentation:
  - [List of Charts](https://www.fusioncharts.com/dev/chart-guide/list-of-charts) - detailed info on charts
  - [Chart Attributes](https://www.fusioncharts.com/dev/chart-attributes/?chart=heatmap) - detailed info on settings and options

## Maisionette Theme

- [Documentation](http://foxythemes.net/preview/products/maisonnette/documentation.php)

- Dependencies:
  - [jQuery 1.9.1](https://jquery.com/) (or later)
  - [Bootstrap 4.1.2](http://getbootstrap.com/)
  - [Perfect Scrollbar 1.4.0](https://github.com/noraesae/perfect-scrollbar)
  - ~~[Stroke 7 Icon Font 1.0.1](https://github.com/olimsaidov/pixeden-stroke-7-icon)~~  > Font-Awesome
  
  ## steps to install/setup Robot Framework
  
  - pip install numpy==1.16.1
  - sudo python3 -m pip install https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-18.04/wxPython-4.0.7.post2-cp37-cp37m-linux_x86_64.whl
  -  pip install robotframework-ride
  - on terminal, type ride.py
