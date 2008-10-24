#!/bin/sh

WEBSITE_DIR=/var/tmp/website

pysetup ()
{
    /var/tmp/website/bin/python setup.py install --prefix=$WEBSITE_DIR
}

standard_setup ()
{
    # $1 = source URL
    # $2 = untarred directory
    curl $1 | tar zxv && cd $2 && pysetup
    cd $WEBSITE_DIR
}

install_django ()
{
    standard_setup http://media.djangoproject.com/releases/1.0/Django-1.0.tar.gz Django-1.0
}

install_python ()
{
    curl http://mulletron.uwcs.co.uk/python26.tar | tar xv
}

install_setuptools ()
{
    standard_setup http://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c9.tar.gz setuptools-0.6c9
}

install_markdown ()
{
    standard_setup http://pypi.python.org/packages/source/M/Markdown/markdown-1.7.tar.gz markdown-1.7
}

install_docutils ()
{
    wget http://docutils.sourceforge.net/docutils-snapshot.tgz && tar zxvf docutils-snapshot.tgz && cd docutils && pysetup
    cd $WEBSITE_DIR
}

install_dateutil ()
{
    standard_setup http://labix.org/download/python-dateutil/python-dateutil-1.4.1.tar.gz python-dateutil-1.4.1
}

install_vobject ()
{
    standard_setup http://vobject.skyhouseconsulting.com/vobject-0.7.1.tar.gz vobject-0.7.1
}

mkdir -p $WEBSITE_DIR
cd $WEBSITE_DIR

install_python
install_setuptools
install_django
install_markdown
install_docutils
install_dateutil
install_vobject
