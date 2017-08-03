# Quick Guide to Volttron Agents

Based on Volttron official docs:
http://volttron.readthedocs.io/en/releases-4.1/devguides/agent_development/Agent-Development.html

---
What are agents?
---

Agents are python modules which operate like plugins to Volttron. They exist inside Volttron's virtualenv ("virtual environment"). The core of an agent is a class that derives from volttron's "Agent" class.

#### Packaging
Agents are packaged into python wheel files and stored in ```/.volttron/packaged/```. This is accomplished via the command ```volttron-pkg```. Packaging requires each agent to have a setup.py file.

#### Discovery and Importing("installation")
Agents are discovered and imported by the user explicitly installing them with the ```volttron-ctl``` command. They are given a VIP ID and optionally can be assigned a "tag" for human-friendly naming.

#### Enabling/Disabling ("starting/stopping")
Agents are enabled after Volttron starts. They can be set to automatically enable with the command command using ```volttron-ctl enable``` or enabled once with ```volttron-ctl start```. The corresponding commands are ```disable``` and ```stop```.

#### Integration
Agents implement a class that derives from Volttron's Agent class. A custom agent them uses built-in API methods.
>TODO: What about Drivers and Historian agents? 

#### Invocation
 An agent's class is executed by Volttron via a Reactor pattern. The agent reactor dispatches the agent to a thread and polls regularly to execute it.
>TODO: How are agents initially run?

Agent IDs: http://volttron.readthedocs.io/en/releases-4.1/specifications/agent-vip-id.html

Platform Commands: http://volttron.readthedocs.io/en/4.1/core_services/control/PlatformCommands.html

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
- A standard python file. Setup is used to build an agent into wheel file and enter the agent into Volttron's virtualenv namespace.
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
 
#### RPC (Remote Procedure Call) 

An agent method marked with the @RPC.export decorator can be called by another agent.

If the web system is running, an RPC method can be remotely invoked. 
http://volttron.readthedocs.io/en/releases-4.1/specifications/external-rpc-enhancement.html

#### Message bus
(ZeroMQ, message queue, etc.)

Agents come with built-in publication-subscribe functionality (e.g. @PubSub.subscribe).

http://volttron.readthedocs.io/en/releases-4.1/specifications/pubsub-enhancement.html

>TODO: Can this be used remotely?

#### Direct web requests

If the web system is running, agents can be forwarded web requests. There are three techniques here:

- Agents can be bound to a URL path. In this case, they can only return static files. 
- Agents can respond to a JSON-RPC request. Their response can be dynamic.
- Agents can be bound to a websocket. This allows for bidirectional communication.

http://volttron.readthedocs.io/en/develop/specifications/webframework.html

