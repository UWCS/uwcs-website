Ubuntu setup
============

Currently, need mailman installed

::

    sudo apt-get install mailman

You need python virtualenv stuff to get an isolated environment for libraries:

::

    sudo apt-get install python-virtualenv

If you use zsh you'll probably also need to also run:

::

    echo . /etc/bash_completion.d/virtualenvwrapper >> $HOME/.zshrc
    . $HOME/.zshrc

Then create the virtualenv

::

    mkvirtualenv --no-site-packages website

Currently need mercurial for fetching one of our requirements :(

::

    sudo apt-get install mercurial

Install the requirements

::

    pip install -r requirements.txt
