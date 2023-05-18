from service import create_app
import time

print("waiting elastic server on...")
for i in range(30):
    time.sleep(1)
    print(f"\rtime...{i+1}", end="")
print("\rwaiting elastic server on done")

print("start flask app...")
create_app().run(port=7777, debug=False)
