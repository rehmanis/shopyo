"""
file: api/tests/conftest.py
All pytest fixtures local only to the api/tests are placed here
"""

import pytest
import os
from shopyo.api.scripts import cli
from pathlib import Path
from shutil import rmtree, copytree, ignore_patterns
import sys
import subprocess


@pytest.fixture
def startbox_runner(flask_app, tmpdir, flag_option):
    """fixture for command startbox2. Sets up a modules directory inside tmpdir
    and depending on the flag_option tuple, the fixture will either try to
    create an existing box or create a unique one. The option part of the tuple
    will determine either to run with the option or not. See test_cli.py for
    example usage

    Parameters
    ----------
    flask_app : flask app object
        the test flask application
    tmpdir : pyest fixture
        built-in pytest fixture for creating unique temp directories
    flag_option : tuple (bool, str)
        flag part of the tuple determines whether to create an exiting
        box or create a unique box. Option contains the cmd option
        to be used with `startbox2` cmd

    Yields
    -------
    tuple(runner result obj, str)
        runner result object returned when cmd command is invoked
        and the path of the for new box is returned as tuple
    """
    flag, option = flag_option
    name = "foo"

    if not bool(flag):
        modules_path = tmpdir.mkdir("modules")
        path = os.path.join(modules_path, f"box__{name}")
    else:
        path = tmpdir.mkdir("modules").mkdir(f"box__{name}")

    os.chdir(tmpdir)
    runner = flask_app.test_cli_runner()

    if option is None:
        result = runner.invoke(cli, ["startbox2", name])
    else:
        result = runner.invoke(cli, ["startbox2", name, option])

    yield result, path


@pytest.fixture
def create_foo_project(venv):
    # old_path = sys.path
    # sys.path = sys.path[:]
    # sys.path.insert(0, "C:\\Users\\shams\\Documents\\init_test\\foo")
    # here = os.path.abspath(os.path.dirname(__file__))
    here = os.path.dirname(os.getcwd())
    # print(here)
    # os.chdir("C:\\Users\\shams\\Documents\\init_test\\foo")

    # install_requires = open(
    #     os.path.join("requirements.txt"), encoding="utf-8"
    # ).read().split("\n"),  # Optional
    # print(install_requires)
    # venv.install(install_requires, upgrade=True)
    # venv.install("-r" + os.path.join(here, "requirements.txt"), upgrade=True)    
    # venv.install("shopyo", upgrade=True)

    os.chdir("C:\\Users\\shams\\Documents\\init_test\\foo\\foo")
    # subprocess.run([sys.executable, "-m", "venv", "env"])
    yield
    # sys.path = old_path


@pytest.fixture
def create_new_project(tmpdir):
    """
    """

    project_path = os.path.join(tmpdir, "foo/foo")
    # get the shopyo src path that the new project will mimic
    src = Path(__file__).parent.parent.parent.absolute()
    # copy the shopyo/shopyo content to a new shopyo project
    copytree(
        src, project_path,
        ignore=ignore_patterns(
            "*.pyc", "__main__.py", "api", ".tox", ".coverage", "*.db"
        )
    )
    os.chdir(project_path)
    yield
    # print(project_path)


@pytest.fixture
def create_hello():
    os.chdir("C:\\Users\\shams\\Documents\\init_test\\hello")
    yield


@pytest.fixture
def virtual():
    os.chdir("C:\\Users\\shams\\Documents\\init_test\\hello")
    subprocess.run([sys.executable, "-m", "venv", "env"])
    yield


@pytest.fixture
def db_session():
    pass

# @pytest.fixture
# def db():
#     """
#     creates and returns the initial testing database
#     """
#     # Create the database and the database table
#     _db.app = test_client
#     _db.create_all()

#     # Insert admin, non admin, and unconfirmed
#     _db.session.add(non_admin_user)
#     _db.session.add(admin_user)
#     _db.session.add(unconfirmed_user)

#     # add the default settings
#     with open("config.json", "r") as config:
#         config = json.load(config)
#     for name, value in config["settings"].items():
#         s = Settings(setting=name, value=value)
#         _db.session.add(s)

#     # Commit the changes for the users
#     _db.session.commit()

#     yield _db  # this is where the testing happens!

#     # _db.drop_all()