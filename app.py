'''
Flask App
Flask app to run the web based interface
Made by Red in 2020
Greetings, from the ROC!

https://github.com/nlMeminger/MagiCarp

This code is licensed under the GNU General Public License
For more information see the LICENSE file that was distributed with this code
Or visit https://www.gnu.org/licenses/gpl-3.0.en.html
'''

import flask
from flask import render_template
import redis
import os

import CONFIG
import tabs


app = flask.Flask(__name__) #init flask
red = redis.StrictRedis() #Listen for redis events


def event_stream():
	pubsub = red.pubsub()
	pubsub.subscribe('server_msg') #subscribe to server_msg stream
	for message in pubsub.listen():
		#print(message) #Debug
		yield 'data: %s\n\n' % message['data'] #return a properly formatted server side event


def sever_msg(data):
	#Send a string to the server_msg stream
	red.publish('server_msg', u'%s' % (data))


@app.route("/")
def index():
	#Render the index page
	return render_template("index.html")


@app.route('/favicon.ico')
def favicon():
	#Send the favicon because why not
    return flask.send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/ico')


@app.route("/stream")
def stream():
	#The event stream for the server side events
	return flask.Response(event_stream(), mimetype="text/event-stream") #return the event stream with the proper mime so that chrome is happy


@app.after_request
def set_response_headers(response):
	#This function runs after each request and tells the browser not to cache anything.
	#Not going to waste data or cycles because it's local-only comms
	response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
	response.headers['Pragma'] = 'no-cache'
	response.headers['Expires'] = '0'
	return response


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080) #Run the app on port 80