"""paver config file"""

# from testing python book
from paver.easy import sh
from paver.tasks import task, needs


@task
def nosetests():
    """unit testing"""
    sh('nosetests --cover-package=cashflows --cover-tests '
       ' --with-doctest --rednose  ./cashflows/')

@task
def pylint():
    """pyltin"""
    sh('pylint ./cashflows/')

@task
def pypi():
    """Instalation on PyPi"""
    sh('python setup.py sdist')
    sh('twine upload dist/*')

@task
def local():
    """local install"""
    sh("pip uninstall cashflows")
    sh("python setup.py install develop")


@task
def sphinx():
    """Document creation using Shinx"""
    sh('cd docs; make html; cd ..')

@needs('nosetests', 'pylint', 'sphinx')
@task
def default():
    """default"""
    pass
