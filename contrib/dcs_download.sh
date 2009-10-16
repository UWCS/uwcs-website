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

install_textile ()
{
    standard_setup http://pypi.python.org/packages/source/t/textile/textile-2.0.11.tar.gz textile-2.0.11
}

install_jquery ()
{
    cd "$WEBSITE_DIR/compsoc/static/js"
    wget http://jqueryjs.googlecode.com/files/jquery-1.3.2.js
    ln -s jquery-1.3.2.js jquery.js
}

install_recaptcha ()
{
    cd "$WEBSITE_DIR/compsoc/static/js"
    curl http://mulletron.uwcs.co.uk/recaptcha.tar.gz | tar xz
}

install_pytz ()
{
    standard_setup http://pypi.python.org/packages/source/p/pytz/pytz-2009n.tar.gz pytz-2009n
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
install_textile
install_jquery
install_recaptcha
install_pytz
