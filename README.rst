Ubuntu setup
============

Currently, need mailman installed

    sudo apt-get install mailman

You need python virtualenv stuff to get an isolated environment for libraries:

    sudo apt-get-install virtualenvwrapper

Then create the virtualenv

    mkvirtualenv --no-site-packages uwcs-website
    workon uwcs-website

Currently need mercurial for fetching one of our requirements :(

    sudo apt-get install mercurial

Install the requirements

    pip install -r requirements.txt
