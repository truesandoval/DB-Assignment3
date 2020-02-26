from collections import namedtuple

from flask import g
from flask import escape
from flask import render_template
from flask import request
from flask import redirect

from voyager.db import get_db, execute
from voyager.validate import validate_field, render_errors
from voyager.validate import NAME_RE, INT_RE, DATE_RE

def sailors(conn):
    return execute(conn, "SELECT s.sid, s.name, s.age, s.experience FROM Sailors AS s")

def who_sailed(conn, boat_name):
    return execute(conn, f"SELECT DISTINCT Sailors.name FROM Sailors INNER JOIN Voyages ON Sailors.sid = Voyages.sid INNER JOIN Boats ON Boats.bid = Voyages.bid WHERE Boats.name = '{boat_name}'")
    
def who_sailed_on_date(conn, date):
    return execute(conn, f"SELECT DISTINCT Sailors.name FROM Sailors INNER JOIN Voyages ON Sailors.sid = Voyages.sid WHERE Voyages.date_of_voyage = '{date}'")
    
def who_sailed_on_boat_of_color(conn, color):
    return execute(conn, f"SELECT DISTINCT Sailors.name FROM Sailors INNER JOIN Voyages ON Sailors.sid = Voyages.sid INNER JOIN Boats on Boats.bid = Voyages.bid WHERE Boats.color = '{color}'")

def add_sailor(conn, sailor_name, sailor_age, sailor_exp):
    return execute(conn, f"INSERT INTO Sailors (name, age, experience) VALUES ('{sailor_name}', '{sailor_age}', '{sailor_exp}')")

def views(bp):
    @bp.route("/sailors")
    def _get_all_sailors():
        with get_db() as conn:
            rows = sailors(conn)
        return render_template("table.html", name="sailors", rows=rows)
        
    @bp.route("/sailors/who-sailed", methods=['GET', 'POST'])
    def _get_who_sailed():
        if request.method == "POST":
            with get_db() as conn:
                boat_name = request.form["boat-name"]
                rows = who_sailed(conn, boat_name)
            return render_template("table.html", name=boat_name, rows=rows)
            
    @bp.route("/sailors/who-sailed-on-date", methods=['GET', 'POST'])
    def _get_who_sailed_on_date():
        if request.method == "POST":
            with get_db() as conn:
                date = request.form["date"]
                rows = who_sailed_on_date(conn, date)
            return render_template("table.html", name=date, rows=rows)
            
    @bp.route("/sailors/who-sailed-on-boat-of-color", methods=['GET', 'POST'])
    def _get_who_sailed_on_boat_of_color():
        if request.method == "POST":
            with get_db() as conn:
                color = request.form["color"]
                rows = who_sailed_on_boat_of_color(conn, color)
            return render_template("table.html", name=color, rows=rows)

    @bp.route("/sailors/add", methods=['GET', 'POST'])
    def _add_sailor():
        if request.method == "GET":
            return render_template("addsailor.html")
        if request.method == "POST":
            with get_db() as conn:
                sailor_name = request.form["sailor-name"]
                sailor_age = request.form["sailor-age"]
                sailor_exp = request.form["sailor-exp"]
                rows = add_sailor(conn, sailor_name, sailor_age, sailor_exp)
            return redirect('/')
            

