# Project Dashboard

# Milestone 1
### Volttron reads data from simulated and real sensors
- [ ] Identify viable sensor and sensor interface
- [ ] Run through Volttron example agents and lightly modify them 
- [ ] Create sample Volttron datapublisher (fake/mock device) for subscriber 
- [ ] Create sample Volttron subscriber/listener agent
- [ ] Create Volttron agent quick guide to centralize information 
- [ ] Mock sensor input in Volttron
- [ ] Refactor pub/sub samples for realistic sensor data
- [ ] Unit test sensor input
- [ ] Unit test pub/sub flow 
- [ ] Procure real sensor for trial
- [ ] Create functional test for real sensor and pub/sub agents
- [ ] Finish full-stack document and corresponding diagrams

# Milestone 2
### Data is stored, analyzed, and reported
- [ ] Define key reporting metrics
- [ ] Define algorithm for aggregating and processing sensor data
- [ ] Create schema for raw and aggregate sensor data
- [ ] Create Volttron historian agent for MySQL database
- [ ] Create web API endpoint for pub/sub sensor data (callable from outside volttron)
- [ ] Setup remote replication of database
- [ ] Start sending errors to logs
- [ ] Develop "alert" agent for getting error data outside Volttron
- [ ] Develop watchdog agent to check that other agents and system are working normally 

# Milestone 3
### GUI allows visualization of logs and analytics
- [ ] Attempt to use Volttron's built-in web GUI
- [ ] Prototype barebones, one page analytics summary

# Milestone 4
### Full prototype works and passes tests
- [ ] Build functional tests for data pipeline
- [ ] Build performance/stress test for data pipeline

# Milestone 5
### Data is used to generate decisions and control fan
- [ ] Finalize details on fan motor control
- [ ] Develop safety switch to disable Volttron control of fan

# Milestone 6
### Prototype is deployed on site and passes tests