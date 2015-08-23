# [YGOrganizer](http://ygorganizer.com)

This web application provides an easy to use interface for Yu-Gi-Oh! players and collectors to manage their card and decks collections.

This repository is meant to streamline any future community efforts in developing the application and also provide issue tracking, in order to follow new features, improvements and bugs with ease.

## Installation Instructions #

### I. Initial setup ###

This application has only been tested on a Linux distribution (namely Ubuntu Server) and the installation process is intended for a Linux distro. Windows folks, you're on your own, but I disagree with using Windows as a server environment.

You will need to install the following software:

 * [Python 2.7](https://www.python.org/downloads/)
 * [Pip](https://pip.pypa.io/en/latest/installing.html)
 * [Virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) (optional, but I strongly recommend it)
 * [Node.js & NPM](https://nodejs.org/download/)
 * [MySQL](http://www.mysql.com/downloads/)
 * [nginx](http://nginx.org/en/download.html) (optional, but I recommend it for development as well, it serves static files faster)
 * [Rabbit.mq](http://www.rabbitmq.com/download.html)
 * [memcached](http://memcached.org/downloads) (optional, if you wish to simulate the production environment)
 * [Supervisor](http://supervisord.org/) (optional, same as above)


### II. Front-end ###

The front-end uses Require.js to modularize Javascript code and LESS for the styling. While in debug (dev) mode, the R.js modules do not need compilation / optimization, but the LESS files still need to be pre-compiled.

You will have to run `npm install` inside the source directory. This will install all the required packages from `package.json`.

You can compile all the files for development mode using the command `grunt`. In order to auto-compile files while editing them, run `grunt watch`.

To compile files for the production environment (concatenation, minification), run `grunt prod`.


### III. Back-end ###

For the back-end, I recommend that you use virtualenv to isolate the development environment for this project. [Initialize the virtualenv to your desired location, then activate it](https://virtualenv.pypa.io/en/latest/userguide.html). Use pip to install the required packages using the command `pip -r <path/to/source/directory>requirements.txt`.

*Note: pyquery uses lxml, which might cause problems during installation. If so, start from their [installation instructions](http://lxml.de/installation.html) and see how to properly install it on your distribution.*

After everything is install, you should configure all the required settings and configuration / running files. Copy `settings.example` to `settings` and start replacing everything between `<...>` with the relevant data.

Then, head on to the conf folder and do the same thing for the `local` and `prod` folders (or only `local`, if you don't intend to simulate the production environment).

Finally, database. Make sure you completed the correct database credentials in the settings files, create the correct database in your MySQL server and also make sure the virtualenv is activated, then run `python manage.py migrate` from the source folder. This will create all the tables required.

*Note: for the time being, there is no sample data provided. I will prepare a package in the future*

All that remains now is to actually run the necessary processes. Use the script `conf/local/run.sh`. If you want importing and automatic price data fetching to work, also run `celery.sh` and, optionally, `flower.sh` for Celery monitorization.

If you wish to simulate the production, you will have to use Supervisor for that or run the commands from `supervisord.conf` manually.

Optionally, you can also use nginx and link the nginx.conf file in `/etc/nginx/sites-enabled`. Make sure you get all the ports right. Nginx will serve all static files that exist and upstream every other request to Django.

If you have any question or issue, contact me at contact@ygorganizer.com or post a question in the [issues section](https://github.com/monovertex/ygorganizer/issues).


## Repository Guidelines ##

 * Use a linting / syntax checker for Python, JavaScript, LESS and HTML and respect their suggestions
 * Lines should not go over 80 characters, unless there's a compelling reason (or you're writing HTML, it's understandable there)
 * Use 4 spaces for indentation
 * Configure your editor to trim trailing spaces on save
 * Use Linux line endings
 * Configure your git to ignore permissions for this repository, to avoid unnecessary conflicts
 * Use parentheses to wrap your multi-line Python statements, it's easier to read and understand than backslashes.
 * Try to use full names in your variables, unless you have an extremely long variable name
 * Use meaningful variable names
 * Be consistent in your coding style with the rest of the repository


## Contributors and important mentions ##

**Thank you,**

 * @mkaatman, for all his suggestions, ideas and support
 * All the folks over at the [/r/yugioh](https://www.reddit.com/r/yugioh/) subreddit for their suggestions and feedback
