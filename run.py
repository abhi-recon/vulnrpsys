# Run a server.
import os
#from gevent.pywsgi import WSGIServer
from app import app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
