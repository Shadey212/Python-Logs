from flask import Flask, render_template
from flask_socketio import SocketIO
from faker import Faker
import random
from time import sleep
from dotenv import load_dotenv
from logtail_config import logger

load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app)

generating = False
log_count = 0

def generate_logs():
	global generating, log_count
	fake = Faker()
	http_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

	while generating:
		method = random.choice(http_methods)
		url = fake.url()
		status = random.choice([200, 201, 400, 404, 500])
		log = {
			'method': method,
			'url': url,
			'status': status,
			'error': None,
			'stack': None
		}

		if status >= 400:
			log['error'] = fake.words()
			log['stack'] = fake.words(5)

		# Log the message with the appropriate log level
		if status >= 500:
			logger.error(log)
		elif status >= 400:
			logger.warning(log)
		else:
			logger.info(log)

		log_count += 1
		socketio.emit('log', log_count)  # Emit incremented log count event

		sleep(0.1)  # Delay between generating logs

@app.route('/')
def index():
	return render_template('index.html')

@socketio.on('start')
def start_logging():
	global generating
	if not generating:
		generating = True
		socketio.emit('log', log_count)  # Emit initial log count event
		generate_logs()

@socketio.on('stop')
def stop_logging():
	global generating
	generating = False
	socketio.emit('log', log_count)  # Emit final log count event

if __name__ == '__main__':
	socketio.run(app, host='0.0.0.0', port=int(os.getenv("PORT", 5000)))