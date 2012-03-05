from fabric.api import *
from fabric.contrib.files import *

REPO = "git://github.com/UWCS/uwcs-website.git"
LOCAL_CLONE = "$HOME/reinhardt/compsoc"

@task
def install_prerequisites():
    sudo("apt-get install -y python2.6 python-virtualenv git")

@task
def webserver():
    # XXX: setup apache here
    pass

@task
def database():
    # XXX: setup mysql here
    pass

@task
def deploy():
    if not exists(LOCAL_CLONE):
        run("git clone %s %s" % (REPO, LOCAL_CLONE))

    with cd(LOCAL_CLONE):
        run("git fetch")
        run("git checkout origin/deployed")

        run("/usr/bin/python2.6 $(which virtualenv) --no-site-packages $HOME/uwcs-website-env")
        with prefix(". $HOME/uwcs-website-env/bin/activate"):
            run("pip install -r requirements.txt")
            run("./manage.py syncdb")

            #run("./manage.py migrate --all")

            # TODO: compsoc.wsgi and settings.py aren't in
            # version control, how do we go about deploying
            # changes to them automatically?

            # make apache notice us
            run("touch apache/compsoc.wsgi")

            # make sure settings.py isn't readable by anyone
            # other than us
            run("chmod og-rwx settings.py")
            run("chmod u+r settings.py")

            # ensure static content can be accessed
            run("chmod a+r static/css/*css")
            run("chmod a+r static/img/*")
