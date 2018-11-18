# TimeTracker

A simple time tracker built with Python3 and love.

![image of the application window](img/main_window.png)


## Features

+ Track how much time you spend on your activities.
+ **Create graphs** from your data:
  + Heat maps: daily, weekly, monthly, yearly time count.
  + Bar plots: total activity time count.
+ Entries are saved on a `csv` file.

## Dependencies

+ Pandas
+ Numpy
+ Matplotlib
+ (Optional) Ipython3: this is for the terminal of the Analyzer window. If doesn't find it in your path it will use `python3` instead.

## How to run

First clone this repository:

`$ git clone git@github.com:AnderRasoVazquez/time-tracker.git`

### Method 1: Using the terminal

From your terminal:

`$ cd time-tracker`

`$ python3 timetracker/__main__.py`

### Method 2 (Linux) Use desktop file

If you want to add TimeTracker to your applications menu change the `exec` line of the `time-tracker/data/timetracker.desktop` file and copy it to `~/.local/share/applications`.

## Get the last changes

At the moment there isn't an installer yet so this is how you update the app.

`$ cd time-tracker`

`$ git pull`


