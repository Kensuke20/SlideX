import lib.db
import routing


if __name__ == '__main__':
    lib.db.init_db()
    routing.app.run(debug=True, host='0.0.0.0')