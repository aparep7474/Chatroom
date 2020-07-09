import os, requests

from flask import Flask, session, redirect, render_template, request, url_for, flash
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime
from helpers import login_required

app = Flask(__name__)
app.config["SECRET_KEY"] = "4301"
socketio = SocketIO(app, async_mode='eventlet')

users_online = []

channels_created = []

messages_created = {}

messages_created2 = {}

@app.route("/")
@login_required
def index():

    if session.get("current_channel") is None:
        return redirect("/create_channel")

    else:
        return redirect("/channels/" + session.get("current_channel"))


@app.route("/log_in", methods=['GET','POST'])
def log_in():

    username = request.form.get("username")

    if request.method == "POST":

        if len(username) == 0:
            flash("Username can't be empty.")
            return redirect("/log_in")

        if username in users_online:
            flash("That username already exists.")
            return redirect("/log_in")

        if username == "admin":
            return redirect("/authorize")

        users_online.append(username)

        session['username'] = username

        session.permanent = True

        return redirect("/create_channel")

    else:
        return render_template("log_in.html")


@app.route("/authorize", methods=['GET','POST'])
def authorize():

    password = request.form.get("password")

    if request.method == "POST":

        if password != "4301":
            flash("Wrong password.")
            return redirect("/authorize")

        users_online.append("admin")

        session['username'] = "admin"

        session.permanent = True

        return redirect("/create_channel")

    else:
        return render_template("authorize.html")


@app.route("/log_out", methods=['GET','POST'])
def log_out():

    try:
        users_online.remove(session['username'])
    except ValueError:
        pass

    session.clear()

    return redirect("/")


@app.route("/create_channel", methods=['GET','POST'])
@login_required
def create_channel():

    session.pop("room", None)

    new_channel = request.form.get("channel")

    if request.method == "POST":

        if len(new_channel) == 0:
            flash("Channel can't be empty.")
            return redirect("/create_channel")

        if new_channel in channels_created:
            flash("That channel already exists.")
            return redirect("/create_channel")

        channels_created.append(new_channel)

        messages_created[new_channel] = []

        return redirect("/channels/" + new_channel)

    else:
        return render_template("create_channel.html", channels=channels_created, users=users_online)


@app.route("/channels/<channel>", methods=['GET','POST'])
@login_required
def channel_name(channel):

    session['room'] = channel

    session.permanent = True

    if channel not in channels_created:
        flash("That channel doesn't exist")
        return redirect("/create_channel")

    return render_template("channel.html", channels=channels_created, messages_created=messages_created[channel], messages_created2=messages_created2)


@socketio.on("submit post")
def post(data):

    room = session.get("room")

    if room not in channels_created:
        emit('redirect', {'url': url_for('create_channel')})

    if len(messages_created[room]) > 100:
        messages_created[room].pop(0)

    messages_created[room].append([session.get("username"), data["message"], datetime.now().strftime("Sent on %m-%d at %H:%M")])

    message = data["message"]

    time = datetime.now().strftime("Sent on %m-%d at %H:%M")

    emit("announce post", {"message": message, "time": time, "username": session.get("username")}, room=room)


@socketio.on("submit worldwide post")
def worldwide(data):

    messages_created2.update({data["message"] : datetime.now().strftime("Broadcasted Worldwide on %m-%d at %H:%M")})

    message = data["message"]

    time = datetime.now().strftime("Broadcasted Worldwide on %m-%d at %H:%M")

    emit("announce post worldwide", {"message": message, "time": time, "username": session.get("username")}, broadcast=True)


@socketio.on("joined", namespace='/')
def joined():

    room = session.get('room')

    join_room(room)

    emit('status', {'msg': session.get('username') + ' has joined the channel'}, room=room)


@socketio.on("left", namespace='/')
def left():

    room = session.get('room')

    leave_room(room)

    emit('status', {'msg': session.get('username')  + ' has left the channel'}, room=room)

@socketio.on("delete channel")
def delete():

    channels_created.remove(session['room'])

    emit('redirect', {'url': url_for('create_channel')})


if __name__ == '__main__':
    socketio.run(app, debug=True)
