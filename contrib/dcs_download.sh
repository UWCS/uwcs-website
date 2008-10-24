#!/bin/sh

set -eu

cd /var/tmp
mkdir website
cd website

curl http://mulletron.uwcs.co.uk/django.tar | tar xv
curl http://mulletron.uwcs.co.uk/python26.tar | tar xv

export PYTHONPATH=/var/tmp/website/lib/python2.4/site-packages/:$PYTHONPATH
