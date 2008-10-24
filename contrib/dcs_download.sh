#!/bin/sh

set -eu

WEBSITE_DIR=/var/tmp/website

mkdir -p $WEBSITE_DIR
cd $WEBSITE_DIR

curl http://mulletron.uwcs.co.uk/django.tar | tar xv
curl http://mulletron.uwcs.co.uk/python26.tar | tar xv
curl http://ftp.de.debian.org/debian/pool/main/p/python-markdown/python-markdown_1.7.orig.tar.gz | tar xv && cd markdown-1.7 && python setup.py install --prefix=/var/tmp/website
cd $WEBSITE_DIR

export PYTHONPATH=$WEBSITE_DIR/lib/python2.4/site-packages/:$PYTHONPATH
