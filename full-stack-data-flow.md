# Full Stack Data Flow

The system moves data from devices (from sensors and the fan) through volttron and reports via a user dashboard.

The system has four main loops:
1. Every 60 seconds Volttron checks the status of all system components ("status loop")
2. Every 5 minutes Volttron stores sensor and fan data ("sampling loop")
3. Every 10 minutes, Volttron runs an aggregate-analyze-decide-control ("decision loop")
4. Every 60 minutes, Volttron runs external data collection (weather, pricing, etc.) ("accessory data loop") 

And one on-demand component:
1. When the user loads the dashboard, it reports on the status and details of the system.

---
STATUS LOOP (every 60 seconds)
---

#### 1) Volttron driver polls sensors and fan
A customized volttron driver reads each sensor and the fan state. It validates and publishes these to the message bus.
 
#### 2) WatchDog runs  
Our customized WatchDog agent checks various system pieces:
    - that sensors report in and that their values are reasonable
    - that the fan state reports in
    - that all required Volttron agents are running
    - that the MariaDB database is operating
    - that Volttron can access the Internet
    
WatchDog writes any failed checks to the log, sends an alert to the cloud, and publishes its results to the message bus.
    
#### 3) StatusHistorian records sensor data and fan state 
Our customized StatusHistorian records the following in the database:
    - the current values of sensors and fan state (data is overwritten after 24 hours)
    - any errors reported by WatchDog 

---
SAMPLING LOOP (every 5 minutes, i.e. 300 seconds)
---
#### 1) Volttron driver polls sensors and fan
As part of its 60 second routine, volttron reads sensor and the fan state, publishing these to the message bus.

#### 2) SamplingHistorian records sensor data and fan state 
Our customized SamplingHistorian records sensor data and fan state to the database. This data is permanent and used for analysis.

>TODO: Should we keep all of this data on the local database? or should we keep a set amount locally and send all of it to the cloud?

>For Historian topic syntax, see http://volttron.readthedocs.io/en/releases-4.1/core_services/historians/Historian-Topic-Syntax.html 

---
DECISION LOOP (every 10 minutes)
---

#### 1) DataAggregator retrieves and publishes relevant data
DataAggregator fetches sensor data, the fan state, and any other relevant data into a collection. It publishes this to the message bus.
 
#### 2) FanDecisionLogic begins
FanDecisionLogic retrieves the aggregated data and begins a chain sequence. First it calls an RPC on FacilityModel.

#### 3) FacilityModel updates model
Our customized FacilityModel agent combines sensor and fan data, analyzes them, and reaches a decision about the fan. It returns this decision to FanDecisionLogic.

#### 4) FanDecisionLogic decides what command to send to the fan
FanDecisionLogic uses the FacilityModel results to determine if the fan state should change or remain the same. If a change is needed, it calls the FanController via RPC. It reports on its decision to the message bus.

#### 5) If called, FanController processes the command
Our customized FanController is a wrapper around Volttron's ActuatorAgent. It can start or stop the fan. It reports on its action to the message bus.

#### 8) DecisionHistorian records the model's decision. 
DecisionHistorian records the decision of FanDecisionLogic and the results of FanController to the database.


---
ACCESSORY DATA LOOP (every 60 minutes)
---


---
LOCAL DASHBOARD (on demand)
---

#### 1) Dashboard reads and reports status.
Whenever a user loads the dashboard page, the dashboard fetches data from the system. 

Data is divided into three bins: Current, Last 24 hours, and Historical. If the dashboard page is open, it will update the current data every 90 seconds. Data for the last 24 hours updates every 30 minutes.

 
---
REMOTE DASHBOARD (on demand)
--- 

#### 1) Local MySQL Master replicates to Cloud Slave
With a small delay, the local mysql stream replicates its contents to a remote slave database hosted on a VPS.

#### 2) Remote Dashboard reads and report status. 
The remote dashboard is identical to the local one, except it uses the remote slave database as its data source. 

