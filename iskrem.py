import time
from Adafruit_IO import Client, Feed, RequestError
import pyfirmata

run_count = 0
ADAFRUIT_IO_USERNAME = "poggersman"
ADAFRUIT_IO_KEY = "aio_ZXNZ35y3IU0RnqtVNE1FNwTrxjpe"

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

board = pyfirmata.Arduino('COM4')

it = pyfirmata.util.Iterator(board)
it.start()

digital_output = board.get_pin('d:11:o')
analog_input = board.get_pin('a:0:i')

try:
	digital = aio.feeds('digital')
except RequestError:
	feed = Feed(name='digital')
	digital = aio.create_feed(feed)

while True:
	print('Sending count:', run_count)
	run_count += 1
	aio.send_data('counter', run_count)
	aio.send_data('chart', analog_input.read())

	data = aio.receive(digital.key)

	print('Data: ', data.value)

	if data.value == "ON":
		digital_output.write(True)
	else:
		digital_output.write(False)

	time.sleep(3)



