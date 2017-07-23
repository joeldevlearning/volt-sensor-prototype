# Full Stack Overview
Hardware, software, and interfaces
---


### + **Devices** `hardware/software`
| Component             | Description  |
| temperature sensor    | feeds data to Volttron in real time |
| ???                   | ??? |

### + **Device-Volttron Interface** `API`
| ???                           | allows Volttron to read sensor data in real time |

### + **Local Server** `hardware\software` ()
| Raspberry Pi                  | server hardware |
| Raspbian (Debian Linux)       | server OS |
| MySQL                         | database |

### + **Volttron** `software` 
| Volttron platform             | runs data pipeline connecting sensors to analytics; can control fan |
| Volttron publisher agent      | code within Volttron reading data from sensors |
| Volttron historian agent      | code within Volttron writing to SQL database |
| Volttron alert agent          | code within Volttron responding to important/exceptional events |

### + **Storage Replicator** `software`
| ???                           | mirrors database to cloud |

### + **Analytics** `software`
| ???                           | aggregates and summarizes sensor data; generates actionable reports |

### + **Cloud app** `hardware\software`
| Linux VPS host                | hosts remote database, web server, and app |
| Cloud web app                 | provides remote monitoring of platform |


---
## Devices `hardware/software`