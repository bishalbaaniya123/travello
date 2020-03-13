# Developement Setup

## 1. Setup python environment

#### Set correct python version for `virtualenv`

Get the python version by looking up the `python_version` setting in the `/Pipfile` folder.
```bash
pyenv virtualenv <project_python_version> saitama
```

##### Install packages
```bash
pip install pipenv
pipenv sync --dev
```

##### Create local settings for django
* `cp saitama/settings/local_base.example.yaml saitama/settings/local/base.yaml`
* Add your db user name
* Add `aws_access_key_id` and `aws_secret_access_key` from your `~/.boto` file.

## 2. Setup node environment
All of the front-end JS and CSS files are generated using node webpack. These files are not
checked into git and need to be built when start working on a project. Same goes for production
files, those will generated on the server.

##### Install packages
```bash
brew install node
brew install yarn
yarn install
```

Note: `yarn install <node_package>` replaces `npm install <node_package>`


## 3. Setup Database
```bash
createdb saitama
./manage.py migrate
./manage.py load_users

#optional

./manage.py createsuperuser
```

## 4. Setup Task Runner

```bash
brew install redis
brew services start redis
```

## 5. Hello World (Actually testing the application)

#### Normal Test Server

1. Create an empty app.scss file in frontend/genos/app.scss folder
2. Run `npm run watch` in terminal #1 (Builds CSS/JS assets)
3. Run `./manage.py runserver` in terminal #2 (Runs localhost:8000 webserver)
4. Run `./manage.py task_queue_celery` in terminal #3 (job runner for background tasks).
    - As an alternative you can put `job_queue_task_always_eager: True` in `settings/local/base.yaml`
      to run the jobs instantly in the browser session. Might slow down API performance.
5. View http://localhost:8000 in your browser.

#### SSL Test server

1. Add the following to `saitama/settings/local/base.yaml`:
    * `wildcard_domain: https://*.dev.big6media.com:9000`
1. Same steps as above, but for step #2 use: `./manage.py runsslserver 127.0.0.1:9000`

## 6. Create a mock website

#### Add a website object

Go to http://localhost:8000/api/website/ in your browser

1. Add following to the HTML form
   1. Name = Test
   2. Domain = helloworld.org
   3. Key = test_key
   4. Template = Van Horne
   5. Config = {}
2. Click **Post**

#### Add a page object

Go to http://localhost:8000/api/website/ in your browser

1. Add following to the HTML form
   1. Website = Pick your previously created site
   2. Page type = Home
   3. Titel = Test Home
   4. Slug = doesnt-matter-for-home
   5. Config = {}
   6. Parent = none
2. Click **Post**

#### View new Website

Go to http://helloworld-org.dev.big6media.com:8000/ in your browser

#### Edit Page Content

For the page http://helloworld-org.dev.big6media.com:8000/page-slug:

Go to  http://helloworld-org.dev.big6media.com:8000/admin/edit/page-slug in your browser

# Development Usage

#### Node Commands

- `npm run watch`: Development mode command to constantly watch for changes and update
  `.js` and `.css` files
- `npm dev`: Development mode command to build the js and css files but not watch for changes
- `npm run build`: Production command to generate hashed versions of the css and js files

#### Frontend (genos)

* TBD: need to figure out how to build these per website from the database
* Probably doing to have a celery job that writes webpack/scss variables to `./dist/${website_key}/**`,
  then the celery job will also call webpack, get the current webpack-stats data and put that back into
  the database for template rendering and CDN/file uploading.

#### View a site

Read **Domains & Sites & Names** section below.

Visit http://DOMAIN-TLD.dev.big6media.com to preview a site webiste. If the internal name is not found
then it will give you a generic 404 page saying "site not found".

### Day-to-Day Commands

#### Pulling new code

Stop the django server, the npm watch script, & any task queues

```bash
# get latest code (may need to fix any merge conflicts)
git pull

# get any new python packages
pipenv sync --dev

# get any new npm packages
yarn install

# update database with any new migrations
./manage.py migrate

# restart django server
./manage.py runserver

# restart npm watch (in separate terminal instance)
npm run watch

# rebuild website assets as the settings change
./manage.py regen_multiple 1,2
# where 1 and 2 are the id's of two websites in your local env

```

### Advanced Commands

#### Managing packages

```bash
# Add pip(python) package to project
pipenv install <pkg name>
pipenv lock --requirements > requirements.txt

# Remove pip package from project
pipenv remove <pkg name>
pipenv lock --requirements > requirements.txt

# Add npm package
yarn add <pkg name>

# Remove npm package
yarn remove <pkg name>

```

## Environments

Test = https://saitama.legalfit.io

Production = https://onepress.legalfit.io

### Loading prod database to local env

```bash
./manage.py load_database

# If you need a clients assets
./manage.py copy_website_assets WEBSITE_ID_1,WEBSITE_ID_2
```

### Setting up TEST for with new code and latest data

```bash
cd /path/to/koopa

# back up production
./shell project=saitama env=production play backup client=saitama

# restore backup in test
./shell project=saitama env=test play restore restore_from_env=production client=saitama

# push latest code
./shell project=saitama env=test play redeploy
```

### Deploying Code to Prod (Sr. Developer)

```bash
cd /path/to/koopa

# push latest code
./shell project=saitama env=production play redeploy
```

# Concepts & Core Ideas

## Domains & Sites & Names

##### Definitions
* saitama.legalfit.io
    * Director (super admin)
        * **path**: `/`
        * **purpose**: This is where we come and build the websites, create logins, etc.
    * Django Admin
        * **path**: `/django-admin`
        * **purpose**: Just for misc administrative things, if we find ourselves coming here then in the normal course of building customer websites then we did something wrong.
* www.client-domain.com
    * Genos (Public site w/ static files)
        * **path**: `/`
        * **purpose**: This is just a preview of the actual website, this will be stored elsewhere as static files in production, but a useful site preview for development.
    * Dr Kuseno (CMS Editor)
        * **path**: `/admin` and `/submit-inquiry`
        * **purpose**: This has two purposes, this is where the clients can login and edit their website and it is where the static website will summit inquiry forms.

##### How sites work in dev

Visit http://lawyer-int-name.dev.big6media.com to preview a site webiste. If the internal name is not found
then it will give you a generic 404 page saying "site not found".

##### How sites work in production - NGINX config

- `/admin` - Will direct to client domain
- `/submit-inquiry` - will direct to client domain
- `/` - Everything else will direct to static generated site
- Technically everything could direct to `/` and the site would work, but we just wouldn't get our
      static page caching.

## Genos Content

Content is a key-value store where the value includes

#### Content types

* `text`
  * Plain text that is 1 line
* `text_plus`
  * Plain text with multiple lines
* `markdown`
* `link`
  *

#### Content helpers

```jinja2
{{ render_markdown(page, key, class="mb-0") }}

{{ render_element(page, prefix + '-title', 'h2', class="section-title") }}

{{ render_image(item, prefix + '-image')}}

{{ render_link(item, prefix + '-link', 'a', class="item-button btn btn-primary") }}

{{ render_bundle('main', 'css', 'GENOS') }}
```



### Rendering Partials with Jinja macros

#### Defining a macro

genos/partials/home.jinja

```jinja2
{%- macro h1(config, obj, prefix='h1') -%}
<div class="container">
	<div class="row">
		<div class="col-md-12">
			{{ render_element(obj, prefix + '-text', 'h1') }}
		</div>
	</div>
</div>
{%- endmacro %}
```

#### Importing and using the macro

genos/page.jinja

```
{% import "genos/partials/home.jinja" as home %}

<html><body>
{% block content %}
  {{ home.h1(page.config.h1, page) }}
{% endblock %}
</body></html>
```



## Django Settings

Most of the Django and Wagtail settings have been moved to yaml files in `saitama/settings`.

The precedence order of settings files:

- /saitama/settings/base.yaml
- /saitama/settings/ENVIRONEMNT.yaml
- /saitama/settings/local/base.yaml
- /saitama/settings/local/ENVIRONMENT.yaml



## 3rd Party Packages

Dangjo





# Front End Concepts

#### Available filters

- Jinja - [List of Builtin Filters](http://jinja.pocoo.org/docs/2.10/templates/#builtin-filters)
- Django filters imported by django-jinja package:
  - [django-jinja.builtins.filters.py](https://github.com/niwinz/django-jinja/blob/master/django_jinja/builtins/filters.py)



### Settings

#### Settings Widgets

* `Text`
  * `TextArray`
* `Color`
* numbers
  * `Integer`
  * `Decimal`
  * `Slider`
  * `PixelSlider`
* boolean
  * `Checkbox`
* options
  * `Dropdown`
    * `FontPair`

#### Website Settings

* Data

  * Name
  * Domain
  * Key
  * Template

* Business Type (family law, criminal defense... )

* Branding

  * Photo Status (none, headshots, professional)

  * Font Pair
  * Colors (may differ per template)
    * Primary
    * Body

* Website Global

  * Header Height
  * `sections`

* Interior Pages

  * `sections`

* Home

  * `sections`



#### Component Settings

###### Constants set in Code (not exposed to an UI)

* css name
  * a unique class that gets attached to it's root element
  * used to tie to CSS therefore must not be changed lightly
* options
  * can translate to a combination of css_classes
* grid_layout (if uses content-grid)

###### Editable in Director

* css_class
  * background classes
* background image

## Components

* Page Sections
  * Blocks of code that go across a page. Usually are lists of things
* Containers
  * sidenav, cards, headers
* Elements
  * buttons, inputs

### Page Sections

#### Website

* `hero`
* `heading_1`
* `team_multiple`
* `footer_locations`
* `footer_inquiry`
* `footer_disclaimer`
* `services` (used for services_index & home)

#### Home page

Can override what website uses

* `hero`
* `heading_1`
* `team`
* `team_single` + `team_multiple`
* `awards`
* `services`

### Containers

* Main Nav
* Side Nav
* Main Content Frame
* Section Frame
* Slideshows

### Compounds

Unique functionality or a collection of elements.

* Blog Summary
* Map View
* Media
* Menu
  - Shape
  - Hover, Focus, Active State
* Lists

### Bootstrap elements

* Buttons
  * Shape
  * Hover, Focus, Active State
* Cards
* Carousel
* Dropdowns
* Forms
* Jumbotron
* List groups
* Nav  / Navbar
*

## Templates

Template composed of:

* Layout
* Colors
  * need definitions & rules
  * Pallete
    * Brand Color
    * Accent Color
    * Variants (dark/light)
  * Application
    * Typography
    * Sections
    * Components
    * Elements
* Typography
  * Singe font
  * Display  + Base
  * Descriptions
  * need rules
* Navigation
  * Elevation
    * above or below
* Backdrop + Main container
  * Elevation
  * Shape
* Page Section
  * Elevation
  * Shape
  * Images
* Containers
  * Elevation
    * Shadow 0-5
  * Shape
    * Rounded, Square, Clipped corner
  * Flourish
    * single/double inside border
* Element Styling
  * Elevation
* Accents & Flourishes
  * Selection indicators
