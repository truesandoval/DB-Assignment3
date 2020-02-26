
from collections import namedtuple

from flask import render_template
from flask import request
from flask import escape
from flask import redirect

from voyager.db import get_db, execute

def boats(conn):
    return execute(conn, "SELECT b.bid, b.name, b.color FROM Boats AS b")

def sailed_by(conn, sailor_name):
    return execute(conn, f"SELECT DISTINCT Boats.name FROM Boats INNER JOIN Voyages ON Boats.bid = Voyages.bid INNER JOIN Sailors ON Sailors.sid = Voyages.sid WHERE Sailors.name = '{sailor_name}'")

def popularity(conn):
    return execute(conn, "SELECT Boats.name, count(*) FROM Boats INNER JOIN Voyages ON Boats.bid = Voyages.bid GROUP BY Boats.name ORDER BY count(*) DESC")

def add_boat(conn, boat_name, boat_color):
    return execute(conn, f"INSERT INTO Boats (name, color) VALUES ('{boat_name}', '{boat_color}')")

def views(bp):
    @bp.route("/boats")
    def _boats():
        with get_db() as conn:
            rows = boats(conn)
        return render_template("table.html", name="boats", rows=rows)
        
    @bp.route("/boats/sailed-by", methods=['GET', 'POST'])
    def _get_sailed_by():
        if request.method == "POST":
            with get_db() as conn:
                sailor_name = request.form["sailor-name"]
                rows = sailed_by(conn, sailor_name)
            return render_template("table.html", name=sailor_name, rows=rows)
            
    @bp.route("/boats/by-popularity")
    def _get_popular_boat():
        with get_db() as conn:
            rows = popularity(conn)
        return render_template("table.html", name="boats by popularity", rows=rows)

    @bp.route("/boats/add", methods=['GET', 'POST'])
    def _add_boat():
        if request.method == "GET":
            return render_template("addboat.html")
        if request.method == "POST":
            with get_db() as conn:
                boat_name = request.form["boat-name"]
                boat_color = request.form["boat-color"]
                rows = add_boat(conn, boat_name, boat_color)
            return redirect('/')


        

