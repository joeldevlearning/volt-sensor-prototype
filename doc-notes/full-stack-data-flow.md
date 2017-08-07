# Full Stack Data Flow

##What data?
The purpose of the system is to optimize fan state: The fan should only run when necessary, and otherwise remain off. To accomplish this the system needs three streams of data from:
- Devices (sensors and fans)
- System components (to analyze data and keep the system working)
- External APIs (to complement the analysis)

An additional need for data is for the dashboard, which reports to end-users.

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
  
### 5) GaugeHistorian agent store sensor and fan data
Each type of GaugeAgent has its own Historian that stores the gauge data in the database, for long-term use. 

>For Historian topic syntax, see http://volttron.readthedocs.io/en/releases-4.1/core_services/historians/Historian-Topic-Syntax.html 

---
AGGREGATE LOOP (every 20 minutes)
---

### 1) WeatherAgent calls external API for data
An agent collects weather data, which the FanDecisionLogic will use during the decision loop.

### 2) SeasonalFacilityModel updates
A customized volttron driver reads each sensor and the fan state. It validates and publishes these to the message bus.


---
DECISION LOOP (every 10 minutes)
---

### 1) FanDecisionLogic begins
FanDecisionLogic retrieves the aggregated data and begins a chain sequence. First it calls an RPC on FacilityModel.

### 2) FacilityModel updates model
Our customized FacilityModel agent combines sensor and fan data, analyzes them, and reaches a decision about the fan. It returns this decision to FanDecisionLogic.

### 3) FanDecisionLogic decides what command to send to the fan
FanDecisionLogic uses the FacilityModel results to determine if the fan state should change or remain the same. If a change is needed, it calls the FanController via RPC. It reports on its decision to the message bus.

### 5) If called, FanController processes the command
Our customized FanController is a wrapper around Volttron's ActuatorAgent. It can start or stop the fan. It reports on its action to the message bus.

### 8) DecisionHistorian records the model's decision. 
DecisionHistorian records the decision of FanDecisionLogic and the results of FanController to the database.


---
ACCESSORY DATA LOOP (every 60 minutes)
---


---
LOCAL DASHBOARD (on demand)
---

### 1) Dashboard reads and reports status.
Whenever a user loads the dashboard page, the dashboard fetches data from the system. 

Data is divided into three bins: Current, Last 24 hours, and Historical. If the dashboard page is open, it will update the current data every 90 seconds. Data for the last 24 hours updates every 30 minutes.

 
---
REMOTE DASHBOARD (on demand)
--- 

### 1) Local MySQL Master replicates to Cloud Slave
With a small delay, the local mysql stream replicates its contents to a remote slave database hosted on a VPS.

### 2) Remote Dashboard reads and report status. 
The remote dashboard is identical to the local one, except it uses the remote slave database as its data source. 

