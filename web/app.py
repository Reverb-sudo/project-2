import os.path
import config
import logging
from flask import Flask, abort, send_from_directory
from os import path

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)

app = Flask(__name__)
@app.route("/<string:name>")
def hello(name):
    if '..' in name or '~' in name:
        abort(403)
    elif not os.path.exists('pages/' + name):
        abort(404)
    return send_from_directory('pages/', name), 200
    #return "<h1>UOCIS docker demo!</h1>"
@app.errorhandler(403)
def forbidden(e):
    return send_from_directory('pages/', '403.html'), 403

@app.errorhandler(404)
def four(e):
    return send_from_directory('pages/', '404.html'), 403

def get_options():
    """
    Options from command line or configuration file.
    Returns namespace object with option value for port
    """
    # Defaults from configuration files;
    #   on conflict, the last value read has precedence
    options = config.configuration()
    # We want: PORT, DOCROOT, possibly LOGGING

    if options.PORT <= 1000:
        log.warning(("Port {} selected. " +
                         " Ports 0..1000 are reserved \n" +
                         "by the operating system").format(options.port))

    return options

if __name__ == "__main__":
    options = get_options()
    portnum = str(options.PORT)
    debugbool = options.DEBUG
    log.info(portnum)
    log.info(portnum)
    log.info(debugbool)
    app.run(debug=debugbool, port=portnum, host='0.0.0.0')
