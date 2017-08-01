import logging
import sys

from volttron.platform.vip.agent import Agent, PubSub
from volttron.platform.agent import utils

#
# SETUP
#
utils.setup_logging()
_log = logging.getLogger(__name__)


class TestAgent(Agent):
    def __init__(self, config_path, **kwargs):
        super(TestAgent, self).__init__(**kwargs)

        self.setting1 = 42
        self.default_config = {"setting1": self.setting1}

        self.vip.config.set_default("testagent.config", self.default_config)
        self.vip.config.subscribe(self.configure, actions=["NEW", "UPDATE"], pattern="testagent.config")

    def configure(self, config_name, action, contents):
        config = self.default_config.copy()
        config.update(contents)

        # check for valid configuration settings
        try:
            self.setting1 = int(config["setting1"])
        except ValueError as e:
            _log.error("ERROR PROCESSING CONFIGURATION: {}".format(e))


#
# AGENT FUNCTIONALITY
#

# subscribe agent in volttron by name "listeneragent"
# when topic is received, print out echo in volttron log
@PubSub.subscribe('pubsub', 'heartbeat/listeneragent')
def on_heartbeat_topic(self, peer, sender, bus, topic, headers, message):
    print "TestAgent got\nTopic: {topic}, {headers}, Message: {message}".format(topic=topic, headers=headers,
                                                                                message=message)


# main() accepts arguments from volttron's launcher
# vip_main() is required by every agent to register with the platform
def main(argv=sys.argv):
    utils.vip_main(TestAgent)


if __name__ == '__main__':
    # Entry point for script when called directly
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
