import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.image as mpimg
import numpy as np
import tkinter as tk
from tkinter import filedialog
from matplotlib.patches import Circle, Wedge, Polygon, Rectangle
from matplotlib.collections import PatchCollection
import pandas as pd


def main():
	headers = ['col1', 'col2', 'col3', 'col4', 'col5', 'col6']
	dtypes = {'col1': 'float', 'col2': 'float', 'col3': 'float', 'col4': 'float', 'col5': 'str', 'col6': 'str'}
	parse_dates = [['col5', 'col6']]
	df=pd.read_csv('data.csv', sep=',', header=None, names=headers, dtype=dtypes, skiprows=5, parse_dates=parse_dates)

	time =df['col5_col6']
	humidity1 =df['col1']
	temperature1 =df['col2']
	humidity2 =df['col3']
	temperature2 =df['col4']
	fig, ax=plt.subplots()
	
	ax.plot(time, humidity1, time, humidity2)
	ax.set_title("Humidity")
	ax.set_xlabel("Date")
	ax.set_ylabel("Humidity %")
	plt.legend(["Sensor 1", "Sensor 2"])
	plt.xticks(rotation=90)
	ax.xaxis.set_major_locator(dates.WeekdayLocator(byweekday=(0), interval=1))
	ax.xaxis.set_major_formatter(dates.DateFormatter('%D'))
	ax.xaxis.set_minor_locator(dates.DayLocator())


	# ax.plot(time, temperature1, time, temperature2)
	# ax.set_title("Temperature")
	# ax.set_ylabel("Temperature (C)")
	# plt.legend(["Sensor 1", "Sensor 2"])
	# plt.xticks(rotation=90)
	# ax.xaxis.set_major_locator(dates.WeekdayLocator(byweekday=(0), interval=1))
	# ax.xaxis.set_major_formatter(dates.DateFormatter('%D'))
	# ax.xaxis.set_minor_locator(dates.DayLocator())


	plt.show()



if __name__=='__main__':
	main()	