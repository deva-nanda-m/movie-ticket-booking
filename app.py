from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("movies.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def homepage():
    conn = get_db()
    now_showing = conn.execute("SELECT * FROM movies WHERE status='now_showing'").fetchall()
    coming_soon = conn.execute("SELECT * FROM movies WHERE status='coming_soon'").fetchall()
    
    conn.close()
    return render_template("homepage.html", now_showing=now_showing, coming_soon=coming_soon)

@app.route("/show")
def show():
    movie_id = request.args.get("movie_id")
    if not movie_id:
        return "<h1>Error: No movie selected</h1>"
    conn = get_db()
    movie = conn.execute("SELECT * FROM movies WHERE id=?", (movie_id,)).fetchone()
    showtimes = conn.execute("SELECT * FROM showtimes WHERE movie_id=?", (movie_id,)).fetchall()
    conn.close()
    return render_template("show.html", movie=movie, showtimes=showtimes)

@app.route("/get_seats/<int:showtime_id>")
def get_seats(showtime_id):
    conn = get_db()
    seats = conn.execute("SELECT * FROM seats WHERE showtime_id=?", (showtime_id,)).fetchall()
    conn.close()
    return jsonify([dict(seat) for seat in seats]) #return in json format for js to read

@app.route("/book", methods=["POST"])
def book():
    showtime_id = request.form['showtime_id']
    seats = request.form['seats'].split(',')
    user_name = request.form['user_name']
    user_email = request.form['user_email']
    user_phone = request.form['user_phone']

    if not seats or seats == ['']:
        return "<h1>No seats selected!</h1>"

    conn = get_db()
    
    # Mark seats as booked
    for seat in seats:
        check = conn.execute(
            "SELECT available FROM seats WHERE showtime_id=? AND seat_number=?",
            (showtime_id, seat)
        ).fetchone()

        if not check or check['available'] == 0:
            conn.close()
            return f"<h1>Seat {seat} is already booked!</h1>"

        # Insert booking
        conn.execute(
            "INSERT INTO bookings (showtime_id, seat_number, user_name, user_email, user_phone) VALUES (?,?,?,?,?)",
            (showtime_id, seat, user_name, user_email, user_phone)
        )
        # Update seat availability
        conn.execute("UPDATE seats SET available=0 WHERE showtime_id=? AND seat_number=?", (showtime_id, seat))

    conn.commit()

    # Get movie & showtime info
    showtime = conn.execute("SELECT * FROM showtimes WHERE id=?", (showtime_id,)).fetchone()
    movie = conn.execute("SELECT * FROM movies WHERE id=?", (showtime['movie_id'],)).fetchone()
    conn.close()

    return render_template("payment.html", movie=movie, showtime=showtime, seats=seats,
                           user_name=user_name, user_email=user_email, user_phone=user_phone,)
@app.route("/payment")
def payment():
    return "<h1>Payment Page (Static)</h1>"

if __name__ == "__main__":
    app.run(debug=True)
