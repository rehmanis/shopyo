import json
import os

from flask import Blueprint, flash, redirect, render_template, url_for

from flask_login import login_required, login_user, logout_user

from shopyoapi.enhance import base_context
from shopyoapi.html import notify_danger

from modules.admin.models import User
from modules.login.forms import LoginForm

dirpath = os.path.dirname(os.path.abspath(__file__))
module_info = {}

with open(dirpath + "/info.json") as f:
    module_info = json.load(f)

login_blueprint = Blueprint(
    "login",
    __name__,
    url_prefix=module_info["url_prefix"],
    template_folder="templates",
)


@login_blueprint.route("/", methods=["GET", "POST"])
def login():
    context = base_context()
    login_form = LoginForm()
    context["form"] = login_form
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_hash(password):
            flash(notify_danger("please check your user id and password"))
            return redirect(url_for("login.login"))
        login_user(user)
        return redirect(url_for("control_panel.index"))
    return render_template("/login.html", **context)


@login_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")
