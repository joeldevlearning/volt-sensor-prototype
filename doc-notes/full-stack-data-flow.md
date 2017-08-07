# Full Stack Data Flow

##What data?
The purpose of the system is to optimize fan state: The fan should only run when necessary, and otherwise remain off. To accomplish this the system needs data from:
- Devices (sensors and fans)
- System components (to analyze data and keep the system working)
- External APIs (to complement the analysis)

Additionally, the dashboard reads data.

##How is data processed?
The system has four main loops:
1. Every 2 minutes Volttron collects data on the devices and system status ("status loop")
2. Every 20 minutes, Volttron collects all data needed for the decision loop ("aggregate loop")
3. Every 25 minutes, Volttron runs an aggregate-analyze-decide-control ("decision loop")
4. Every 60 minutes, Volttron calls an external API for pricing information ("price-quote loop")

The dashboard updates on-demand, whenever the user loads it or leaves the dashboard window open.

---
 STATUS LOOP (every 2 minutes)
---

### 1) Volttron driver polls sensors and fan
A customized volttron driver reads each sensor and the fan state. It validates and publishes these to the message bus.
 
### 2) WatchDog runs  
Our customized WatchDog agent checks various system pieces:
- that sensors report in and that their values are reasonable
- that the fan state reports in
- that all required Volttron agents are running
- that the MariaDB database is operating
- that Volttron can access the Internet
    
WatchDog writes any failed checks to the log, sends an alert to the cloud, and publishes its results to the message bus.
    
### 3) StatusHistorian records any warnings or errors 
Our customized StatusHistorian records WatchDog status results in the database.

### 4) Gauge agents sample sensor and fan data
Our customized Gauge agents retain the state of each device for the desired sampling period. They continuously update.
  
### 5) GaugeHistorian agent stores sensor and fan data
Our custom GaugeHistorian subscribes to all device data and stores it long-term in the database. It also exposes access to this data via an RPC method.

>For Historian topic syntax, see http://volttron.readthedocs.io/en/releases-4.1/core_services/historians/Historian-Topic-Syntax.html 

---
AGGREGATE LOOP (every 20 minutes)
---

### 1) WeatherAgent calls external API for data
An agent collects weather data, which the FanDecisionLogic will use during the decision loop.
>WeatherUndergrounds API free tier gives us 10 calls/minute with a max of 500 calls every 24 hours.

### 2) SeasonalFacilityModel updates long-term model
Our SeasonalFacilityModel calls the GaugeHistorian for data, updates its own model, and publishes results on the message bus. 

### 3) LiveFacilityModel updates short-term model
Our customized FacilityModel agent calls the GaugeHistorian for data and returns the optimal fan state. It publishes this to the message bus.

### 4) FacilityAcitivityModel updates short-term model
The FacilityActivityModel checks the time and date and predicts the human impact factor of fan state. It reports this to the message bus.

### 4) ModelHistorian 
All model results are subscribed to by the ModelHistorian and stored in the database.

### 5) WeatherHistorian 
All weather updates are subscribed to by the WeatherAgent and stored in the database.

---
DECISION LOOP (every 10 minutes)
---

### 1) FanDecisionLogic retrieves data, processes rules, and chooses an action
First, FanDecisionLogic retrieves the aggregated data. It calls the GaugeHistorian, WeatherHistorian, and ModelHistorian for the most recent results. 

Second, FanDecisionLogic applies any operating rules governing the fan state.

Finally, after processing data and rules, FanDecisionLogic either (a) calls the FanController via RPC to turn on the fan or (b) exits. It publishes its decision to the message bus.

### 2) If called, FanController processes the command
Our customized FanController is a wrapper around Volttron's ActuatorAgent. It can start or stop the fan. It reports on its action to the message bus.

### 3) FanActionHistorian records FanDecisionLogic and FanController results. 
DecisionHistorian records the decision of FanDecisionLogic and the results of FanController to the database.

---
ADDITIONAL OPERATIONS (every hour or more)
---

### 1) PriceQuoteAgent 
EIA agent to collect pricing.

---
LOCAL DASHBOARD (on demand)
---

### 1) Dashboard reads and reports status.
Whenever a user loads the dashboard page, the dashboard fetches data from the system. 

Data is divided into three bins: Current, Last 24 hours, and Historical. 
If the dashboard page is open, it will update the current data every 90 seconds. Data for the last 24 hours updates every 30 minutes.

Current data is returned live from Gauge agents, while historical data is retrieved directly from the database (due to its size).
 
---
REMOTE DASHBOARD (on demand)
--- 

### 1) Local MySQL Master replicates to Cloud Slave
With a small delay, the local mysql stream replicates its contents to a remote slave database hosted on a VPS.

### 2) Remote Dashboard reads and report status. 
The remote dashboard is identical to the local one, except it uses the remote slave database as its data source. 

