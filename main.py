from app import app, db
import url.views
import url.models

if __name__ == '__main__':
    app.run(port=5003, debug=True)
