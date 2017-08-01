# Full Stack Data Flow

The system moves data from devices (from sensors and the fan) through volttron and reports via a user dashboard.


There are three points of synchronization:
1. Volttron samples data at intervals of 60 seconds


---
DEVICES (constant)
---

#### 1) Sensors sample temperature data
Temperature sensors sample at a constant rate (less than 60 seconds).

---
VOLTTRON (every 60 seconds)
---

#### 2) Volttron driver polls sensors and fan
A customized volttron driver reads each sensor at a fixed rate. 

It also reads the fan's state.  
>TODO: How does the sensor communicate with Volttron?

#### 3) Driver publishes sensor and fan data
The driver validates the sensor data. It then publishes the data, including sensor ID, to Volttron's message bus under /record topic. 

It also publishes the fan's state under /devices topic.

#### 4) RawDataHistorian records data
Our customized RawDataHistorian is subscribed to the /record topic. It reads the new sensor and fan data and inserts these into the MySQL database.
>For Historian topic syntax, see http://volttron.readthedocs.io/en/releases-4.1/core_services/historians/Historian-Topic-Syntax.html 

#### 5) DataSync  
The DataSync agent coordinates data with analysis. It waits on a timer for all required data before activating. (If the timer expires, it resets itself). It subscribes to the /devices and /records topics. When it has received the appropriate messages from these, it uses RPC to invoke the FacilityModeller.  
>DataSync acts as a cyclic barrier, blocking analysis and fan control until sufficient data is available. 

>TODO: How should FacilityModeler get the aggregate information? Should this be stored in a set?


#### 6) FacilityModeler updates model
Our customized FacilityModeler agent combines sensor and fan data, analyzes them, and reaches a decision about the fan. It is called by DataSync via an exposed RPC function.

When its analysis is finished, FacilityModeler publishes a decision to the message bus. 
> TODO: We only want the FacilityModeler to be able to call the FanController. Can we check in the RPC call for which agent is calling it?

#### 7) FanController acts on model results 
Our customized FanController waits for a message on its topic (either to change or maintain the fan state). Any decision to change or maintain the fan's state. A decision to change the fan state prompts it a call to volttron's ActuatorAgent to fulfill the change.

#### 8) ControlHistorian records the model's decision. 
Our customized ControlHistorian awakes on FacilityModeler's decision and records it to the database.

---
LOCAL DASHBOARD (on demand)
---

#### 1) Dashboard reads and reports status.
Whenever a user loads the dashboard page, the dashboard fetches data from the system. 

Data is divided into three bins: Current, Last 24 hours, and Historical. If the dashboard page is open, it will update the current data every 90 seconds. Data for the last 24 hours updates every 60 minutes.

 
---
REMOTE DASHBOARD (on demand)
--- 

#### 1) Local MySQL Master replicates to Cloud Slave
With a small delay, the local mysql stream replicates its contents to a remote slave database hosted on a VPS.

#### 2) Remote Dashboard reads and report status. 
The remote dashboard is identical to the local one, except it uses the remote slave database as its data source. 

