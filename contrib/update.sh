#!/bin/sh

cd /home/webmaster/reinhardt/compsoc/
./manage.py update
./manage.py add_active_members_to_list compsoc-announce
