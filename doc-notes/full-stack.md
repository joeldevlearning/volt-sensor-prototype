# Full Stack Overview
##Hardware, software, and interfaces
---


## **Devices** `hardware/software`
| Component             | Description  |
| :---         |     :---:      |
| temperature sensor    | feeds data to Volttron in real time |
| ???                   | ??? |

## **Device-Volttron Interface** `API`
| Component             | Description  |
| :---         |     :---:      |
| ???                           | allows Volttron to read sensor data in real time |

## **Local Server** `hardware\software`
| Component             | Description  |
| :---         |     :---:      |
| Raspberry Pi                  | server hardware |
| Raspbian (Debian Linux)       | server OS |
| MySQL                         | database |

## **Volttron** `software` 
| Component             | Description  |
| :---         |     :---:      |
| Volttron platform             | runs data pipeline connecting sensors to analytics; can control fan |
| Volttron publisher agent      | code within Volttron reading data from sensors |
| Volttron historian agent      | code within Volttron writing to SQL database |
| Volttron alert agent          | code within Volttron responding to important/exceptional events |


## **Storage Replicator** `software`
| Component             | Description  |
| :---         |     :---:      |
| ???                           | mirrors database to cloud |

## **Analytics** `software`
| Component             | Description  |
| :---         |     :---:      |
| ???                           | aggregates and summarizes sensor data; generates actionable reports |

## **Cloud app** `hardware\software`
| Component             | Description  |
| :---         |     :---:      |
| Linux VPS host                | hosts remote database, web server, and app |
| Cloud web app                 | provides remote monitoring of platform |


---
## Devices `hardware/software`