# Dashboard Overview
Information and format of the dashboard. 
>TODO: Consider using Volttron Central. However it is beta and has limited customization.

---
CATEGORIES OF DATA
---

- Measurement data is divided into three time bins: Current, Last 24 hours, and Historical. If the dashboard page is open, it will update the current data every 90 seconds. Data for the last 24 hours updates every 60 minutes.

- Each set of measurement data has summary statistics, including a range, averages, totals, etc.
>TODO: Can we calculate statistics via a database trigger?

- Status data reports on the activity of devices and the system overall.

- Logs are copied and read from the system.
>TODO: Currently no description of code to do this. We need the volttron log, plus an error log.

-------------------------
PAGES
-------------------------
The dashboard presents essential data on its main page, and detailed data in sub-pages. 
 
```
ROOT/ 

├── /data
    └──/current
├── └──/last24
├── └──/history
├── /status
    └──/all
    └──/device
    └──/volttron
└──/log
    └──/all
    └──/normal
    └──/warning    
```

#### ROOT
The root page is default. It summarizes status and data information.

>The root page is customized for general purpose. Other pages specialize and provide more detail.

#### data/current
Full view of current data only. Auto-refreshes every 90 seconds.

#### data/last24
Summary of the last 24 hours of data. Auto-refreshes every 3600 seconds (hour).  

#### data/history
Summary of all data recorded in the system. No auto-refresh.  

####  /status and /status/all
Summary of the state of the devices, volttron, and logs  

####  /log and /log/all
Tab interface to read paginated logs

-------------------------
GUI ELEMENTS
-------------------------
The dashboard is based on text, but includes simple graphical elements.

### Graphs
>TODO: Need a charting library

### Gauges
>TODO: Consider an animated gauge, something like http://justgage.com/

### Customizable Grid Layout
>TODO: Consider a flexible grid layout that allows resizing (e.g. https://github.com/hootsuite/grid). 
This would allow an "everything" dashboard page.

