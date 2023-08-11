# Prerequisites and Components Setup

For development you will need:

* git
* python3 with pip3 and extra python packages (e.g. flask, argparse, etc),
* development environment (e.g. emacs or code or PyCharm).

For testing you will also need:

* a web browser, e.g. chrome, maybe even with REST extensions, e.g.
[Advanced REST Client](https://chrome.google.com/webstore/detail/advanced-rest-client/hgmloofddffdnphfgcellkdfbfbjeloo?hl=en-US)
or [RESTClient](https://addons.mozilla.org/en-US/firefox/addon/restclient/)
* tools like [curl](https://www.tecmint.com/linux-curl-command-examples/),
or [postman](https://www.getpostman.com/)

My configuration:

* OS: Linux/Ubuntu, Mint to be specific.
* python 3.6
* Development Environment: Microsoft Visual Studio Code

## Git Installation

Recommended ways to get git in the order of preference:

* Get git from your OS vendor.
* Download git from https://git-scm.com/downloads

## Python Installation

You may have already python installed.  Version 2 and 3 of python can co-exist.
We will be using Python 3.6 or later so you will need to make sure you use the
right version. Here are the recommended ways to get python3 in the order of
preference:

* Get python with your IDE.  If you do not know what IDE is, ignore this,
* Get python3 from your OS vendor.
* Download Python from Python.org: https://www.python.org/downloads/

This demonstrates that I have two version of python on my laptop:

```bash
alex@latitude:~/Projects/RESTing-with-Flask$ which python
/usr/bin/python
alex@latitude:~/Projects/RESTing-with-Flask$ python --version
Python 2.7.15+
alex@latitude:~/Projects/RESTing-with-Flask$ which python3
/usr/bin/python3
alex@latitude:~/Projects/RESTing-with-Flask$ python3 --version
Python 3.6.8
```

If you have a new Linux install, just do:

```
sudo apt install python3 python3-venv python3-pip python3-flask
```

## Virtual Environment Setup

Virtual environment ensures isolation from the global system configuration.
Read about it here: https://docs.python-guide.org/dev/virtualenvs/

I am not using virtual environment for this project.
Feel free to use it though.
It is especially beneficial if you intend to pack the service into a Docker container:

```
alex@latitude7490:~/Projects/RESTing-with-Flask/02.rest/farm/ > python3 -m venv venv
alex@latitude7490:~/Projects/RESTing-with-Flask/02.rest/farm/ > source ./venv/bin/activate
(venv) alex@latitude7490:~/Projects/RESTing-with-Flask/02.rest/farm/ > pip3 install flask requests
```

After you download all the packages:

```
alex@latitude7490:~/Projects/RESTing-with-Flask/02.rest/farm/ > pip3 freeze > requirements.txt
```

## Flask Installation

Once you have python3 installed and your virtual environment activated (if using), installing flask is easy:

```bash
alex@latitude:~/Projects/RESTing-with-Flask$ flask

Command 'flask' not found, but can be installed with:

sudo apt install python3-flask

alex@latitude:~/Projects/RESTing-with-Flask$ sudo apt install python3-flask
[sudo] password for alex:
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following additional packages will be installed:
  python3-click python3-colorama python3-itsdangerous python3-jinja2 python3-werkzeug
Suggested packages:
  python-flask-doc python-jinja2-doc ipython3 python3-lxml python3-termcolor python3-watchdog python-werkzeug-doc
Recommended packages:
  python3-blinker python3-simplejson python3-openssl
The following NEW packages will be installed:
  python3-click python3-colorama python3-flask python3-itsdangerous python3-jinja2 python3-werkzeug
0 upgraded, 6 newly installed, 0 to remove and 0 not upgraded.
Need to get 415 kB of archives.
After this operation, 2,017 kB of additional disk space will be used.
Do you want to continue? [Y/n] y
Get:1 http://mirror.os6.org/ubuntu bionic/main amd64 python3-colorama all 0.3.7-1 [14.9 kB]
Get:2 http://mirror.os6.org/ubuntu bionic/main amd64 python3-click all 6.7-3 [56.5 kB]
Get:3 http://mirror.os6.org/ubuntu bionic/main amd64 python3-itsdangerous all 0.24+dfsg1-2 [12.0 kB]
Get:4 http://mirror.os6.org/ubuntu bionic-updates/main amd64 python3-jinja2 all 2.10-1ubuntu0.18.04.1 [95.4 kB]
Get:5 http://mirror.os6.org/ubuntu bionic/universe amd64 python3-werkzeug all 0.14.1+dfsg1-1 [174 kB]
Get:6 http://mirror.os6.org/ubuntu bionic/universe amd64 python3-flask all 0.12.2-3 [62.3 kB]
Fetched 415 kB in 2s (247 kB/s)
debconf: unable to initialize frontend: Dialog
debconf: (Dialog frontend requires a screen at least 13 lines tall and 31 columns wide.)
debconf: falling back to frontend: Readline
Selecting previously unselected package python3-colorama.
(Reading database ... 423988 files and directories currently installed.)
Preparing to unpack .../0-python3-colorama_0.3.7-1_all.deb ...
Unpacking python3-colorama (0.3.7-1) ...
Selecting previously unselected package python3-click.
Preparing to unpack .../1-python3-click_6.7-3_all.deb ...
Unpacking python3-click (6.7-3) ...
Selecting previously unselected package python3-itsdangerous.
Preparing to unpack .../2-python3-itsdangerous_0.24+dfsg1-2_all.deb ...
Unpacking python3-itsdangerous (0.24+dfsg1-2) ...
Selecting previously unselected package python3-jinja2.
Preparing to unpack .../3-python3-jinja2_2.10-1ubuntu0.18.04.1_all.deb ...
Unpacking python3-jinja2 (2.10-1ubuntu0.18.04.1) ...
Selecting previously unselected package python3-werkzeug.
Preparing to unpack .../4-python3-werkzeug_0.14.1+dfsg1-1_all.deb ...
Unpacking python3-werkzeug (0.14.1+dfsg1-1) ...
```

If you are using MacOS, you can use `pip3`:
```
Andreas-MacBook-Pro:RESTing-with-Flask andreadashe$ pip3 install flask
Collecting flask
  Downloading Flask-2.3.2-py3-none-any.whl (96 kB)
     |████████████████████████████████| 96 kB 1.7 MB/s 
Collecting itsdangerous>=2.1.2
  Using cached itsdangerous-2.1.2-py3-none-any.whl (15 kB)
Collecting Jinja2>=3.1.2
  Using cached Jinja2-3.1.2-py3-none-any.whl (133 kB)
Collecting click>=8.1.3
  Downloading click-8.1.6-py3-none-any.whl (97 kB)
     |████████████████████████████████| 97 kB 2.2 MB/s 
Collecting blinker>=1.6.2
  Downloading blinker-1.6.2-py3-none-any.whl (13 kB)
Collecting Werkzeug>=2.3.3
  Downloading Werkzeug-2.3.6-py3-none-any.whl (242 kB)
     |████████████████████████████████| 242 kB 2.1 MB/s 
Collecting MarkupSafe>=2.0
  Downloading MarkupSafe-2.1.3-cp310-cp310-macosx_10_9_x86_64.whl (13 kB)
Installing collected packages: MarkupSafe, Werkzeug, Jinja2, itsdangerous, click, blinker, flask
Successfully installed Jinja2-3.1.2 MarkupSafe-2.1.3 Werkzeug-2.3.6 blinker-1.6.2 click-8.1.6 flask-2.3.2 itsdangerous-2.1.2
```

## Python Packages Installation

```bash
alex@latitude:~$ pip3 install argparse
Collecting argparse
  Downloading https://files.pythonhosted.org/packages/f2/94/3af39d34be01a24a6e65433d19e107099374224905f1e0cc6bbe1fd22a2f/argparse-1.4.0-py2.py3-none-any.whl
Installing collected packages: argparse
Successfully installed argparse-1.4.0
alex@latitude:~$ pip3 install pid
Collecting pid
  Downloading https://files.pythonhosted.org/packages/82/bc/3633e94577c0f64864684be5a73251f194fd8673fb7c1f095597ef34dbc2/pid-2.2.5-py2.py3-none-any.whl
Installing collected packages: pid
Successfully installed pid-2.2.5
```

## Development Environment Setup - Visual Studio Code

Download from: https://code.visualstudio.com

Make sure to install the extensions for python development.  I also have
enabled preview for .md and .asciidoc files.

## Database

We will use [CouchDB](https://couchdb.apache.org), mostly because of its
wonderful support for REST and JSON. Install CouchDB from your OS vendor
repository.  If not there, use pre-built binaries from
https://couchdb.apache.org/#download
