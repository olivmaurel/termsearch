Install and run Termsearch locally
==================================

Termsearch is a web application accessible at [insert url].
This repository allows you to fork and run locally the project.

Overview
--------
Termsearch is a web application for translators, students and other people looking for the translation of a word, an expression, an acronym or any other term.
Just type in the term you are looking for, the language pair, and you will be prompted with the results from different online sources, namely Termium, Proz, IATE, and the FAO.

Its objective is to save time for translators by offering them all the results at a glance.


Setting up
----------

To setup the project you need to create a new virtualenv directory and install
the dependencies listed in the requirements file::

    virtualenv termsearch
    source termsearch/bin/activate
    pip install -r requirements.txt

Next setup the Django instance::

    ./manage.py syncdb

And finally run the project::

    ./manage.py runserver

Open the url http://127.0.0.1:8000/aggregator/search and do a test search, everything should be in place and you should get the results from Termium, Proz, Iate etc.

Database
--------

The project installs a fresh postgresql DB on your machine, without any search registered.
Once installed, every request you try on the local url will be registered, along with the results.

Flushing the Database
---------------------

If you want to erase all the searches and start anew, the easiest way to do it is to log into the admin interface and delete all the existing searches from there.
You can of course also flush the DB with a fresh install of the project, or using the appropriate postgresql command.