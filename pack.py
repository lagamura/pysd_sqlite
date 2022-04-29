import pysd
from os import path
import pathlib
import matplotlib.pyplot as plt



fileDir = f'./models/Teacup'
fileExt = r'*.py'
model_path = list(pathlib.Path(fileDir).glob(fileExt))

if (not path.exists(fileDir)):
    raise Exception("There is not such a name model")

model = pysd.load(model_path[0])

stop_step = 1
input = 30

for i in range(100):
    next_step = model.time() + stop_step
    stocks = model.run(params={'Room Temperature': input}, initial_condition="current", final_time=next_step)

'''
stocks = model.run()
stocks["Teacup Temperature"].plot()
plt.title("Teacup Temperature")
plt.ylabel("Degrees F")
plt.xlabel("Minutes")
plt.grid()
'''