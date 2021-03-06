from fabric.api import run, prefix, task, sudo, cd
from fabric.colors import yellow
from fabric.contrib.files import exists

REPO = "git://github.com/UWCS/uwcs-website.git"
LOCAL_CLONE = "$HOME/reinhardt/compsoc"
WEBSITE_ENV = "$HOME/uwcs-website-env"
EASY_INSTALL_DIR = "$HOME/easy-install-dir"
CHECKOUT_BRANCH = "origin/master"

@task
def install_prerequisites():
    """Install packages needed to run the django app."""
    sudo("apt-get install -y python2.7 python-virtualenv git mercurial")

@task
def webserver():
    # XXX: setup apache here
    pass

@task
def database():
    # XXX: setup mysql here
    pass

@task
def mailman():
    # XXX: what happens with debconf?
    print yellow("Installing mailman")
    sudo("apt-get install -y mailman")

    print yellow("Creating mailman site mailing list (master list for sending out subscription reminders)")
    domain = raw_input("Enter domain for master mailing list: ")
    sudo("newlist mailman@%s" % domain)

@task
def virtualenv():
    if not exists(WEBSITE_ENV):
        run("mkdir -p {easy} && PYTHONPATH={easy} easy_install --install-dir {easy} virtualenv".format(easy=EASY_INSTALL_DIR))
        run("PYTHONPATH={easy} /usr/bin/python2.7 {easy}/virtualenv --no-site-packages {env}".format(easy=EASY_INSTALL_DIR, env=WEBSITE_ENV))

@task
def deploy():
    if not exists(LOCAL_CLONE):
        run("git clone %s %s" % (REPO, LOCAL_CLONE))

    with cd(LOCAL_CLONE):
        run("git fetch")
        run("git checkout %s" % CHECKOUT_BRANCH)
        virtualenv()

        with prefix(". {env}/bin/activate".format(env=WEBSITE_ENV)):
            run("pip install -r requirements.txt --upgrade")
            run("./manage.py syncdb")

            # TODO: sort out migrations, not sure what state uwcs.co.uk is in
            #run("./manage.py migrate --all")

            # TODO: compsoc.wsgi and settings.py aren't in version control, how
            # do we go about deploying changes to them automatically?

            # make apache notice us
            run("touch apache/compsoc.wsgi")

            # make sure settings.py isn't readable by anyone other than us
            run("chmod og-rwx settings.py")
            run("chmod u+r settings.py")

            # ensure static content can be accessed
            run("chmod a+r static/css/*css")
            run("chmod a+r static/img/*")
