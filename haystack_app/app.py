from service import create_app
import time

print("waiting elastic server on...")
# time.sleep(30)

print("start flask app...")
create_app().run(port=7777, debug=False)
