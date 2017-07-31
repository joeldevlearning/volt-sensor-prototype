# Quick Guide to Volttron Agents

Based on Volttron official docs:
http://volttron.readthedocs.io/en/releases-4.1/devguides/agent_development/Agent-Development.html

---
What are agents?
---

Agents are python packages that are... 
1) packaged by volttron (in .volttron/packaged/...)
2) registered with volttron control (aka volttron-ctl)
3) possessing a VIP ID, and optionally a tag name
4) started and stopped by volttron

The core of an agent is a class that derives from volttron's "Agent" class.

Reference: http://volttron.readthedocs.io/en/releases-4.1/specifications/agent-vip-id.html

-------------------------
FOLDER STRUCTURE:
-------------------------
Volttron agents, as packages, live in their own folders:
```
TestAgent/
├── setup.py
├── testagent.config
└── tester
    ├── agent.py
    └── __init__.py
```

#### What do these files do?
##### "setup.py"
- A standard python file. Setup is used to build an agent into wheel file.
(Wheel is a zipped, pre-compiled bytecode format for python packages).
Volttron uses this file when it runs the command "volttron-pkg package TestAgent".

##### "testagent.config"
- Related to setup. The .config can pass arguments to the agent on execution.
A package is finalized by installing the config in the package (via "volttron-pkg configure...").

##### "tester/agent.py"
- A standard volttron file, containing the agent class and methods.
Agents derive from the base volttron Agent.

##### "__init__.py"
- A standard python (2.x) file for packages. Indicates that there is module code in this folder.


> NOTE: Agent packages are placed in the your VOLTTRON_HOME directory. 
This defaults to the home directory of the user you are running under 
(NOT the folder where volttron is located).

--------------------
CONFIGURING AGENTS
--------------------
#### How does Volttron become aware of a new agent? 
Agents can be added to Volttron from any location. To begin, enter the virtualenv, then use the following steps.

1. Setup each agent in its own folder (see structure above)
2. enter the virtualenv (```. env/bin/activate```)
3. package the agent (```volttron-pkg package TestAgent```)
4) attach the config file to the agent's package (```volttron-pkg configure PACKAGE_FILE CONFIG_FILE```)
5) install the agent (```volttron-ctl install PACKAGE_FILE --tag AGENT_NAME```)

>...Start the platform with ```volttron -vv -l volttron.log&```
6) start the agent (```volttron-ctl start --name AGENT_NAME```)


The command ```volttron-ctl stop --name AGENT_NAME``` will stop the agent.

The command ``volttron-ctl list`` will list non-core installed agents. 
The command ``volttron-ctl status`` will list non-core agents that are running.

The command ```volttron-ctl remove --name <AGENT_NAME>``` will uninstall the agent and remove it from ```list``` results.


References: 
http://volttron.readthedocs.io/en/releases-4.1/devguides/agent_development/Agent-Development.html#packaging-agent

http://volttron.readthedocs.io/en/releases-4.1/core_services/control/AgentManagement.html


---------------------
COMMUNICATING WITH AGENTS
---------------------

Agents can communicate through various methods:
 
1) Local or remote RPC calls. Adding the @RPC.export decorator to an agent's function, 
http://volttron.readthedocs.io/en/releases-4.1/specifications/external-rpc-enhancement.html

2) use pub/sub on the local or remove message bus via @PubSub.subscribe
http://volttron.readthedocs.io/en/releases-4.1/specifications/pubsub-enhancement.html

OR
use pub/sub locally or remotely


respond to external network requests (URL path for static files, JSON for dynamic,
or websocket for bidirectional communication)
see:
-
 http://volttron.readthedocs.io/en/develop/specifications/webframework.html

