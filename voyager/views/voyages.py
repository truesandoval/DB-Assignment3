from collections import namedtuple

from flask import render_template
from flask import request
from flask import redirect

from voyager.db import get_db, execute

def voyages(conn):
    return execute(conn, "SELECT v.sid, v.bid, v.date_of_voyage FROM Voyages AS v")

def add_voyage(conn, sid, bid, voyage):
    return execute(conn, f"INSERT INTO Voyages (sid, bid, date_of_voyage) VALUES ('{sid}', '{bid}', '{voyage}')")

    
def views(bp):
    @bp.route("/voyages")
    def _get_all_voyages():
        with get_db() as conn:
            rows = voyages(conn)
        return render_template("table.html", name="voyages", rows=rows)

    @bp.route("/voyages/add", methods=['GET', 'POST'])
    def _add_voyage():
        if request.method == "GET":
            return render_template("addvoyage.html")
        if request.method == "POST":
            with get_db() as conn:
                sid = request.form["sid"]
                bid = request.form["bid"]
                voyages = request.form["voyage"]
                rows = add_voyage(conn, sid, bid, voyage)
            return redirect('/')