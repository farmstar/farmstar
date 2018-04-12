# Farmstar
High precision farm management system.

*NOTE: This is a side project, we have no idea what we are doing.*

![Logo v1.2](/docs/media/logojoy-01.2.png?raw=true)

## Vision
Help feed 10 billion people.

### Farming Industry problems
- Expensive proprietary hardware and software in machines.
- Complicated unintuitive interfaces.
- Seeding, spraying, harvesting inefficiencies.
- Aging farming expertise.
- Fully autonomous tractors are kinda expensive.
- Some farms here in Australia are bigger than entire countries, mate.

### Mockup

*Version 1*

![Mockup v1.1](/docs/media/Mockup-v1.1.jpg?raw=true)

### Goals
*See TODO / wiki / project board for specific project goals*

#### Short Term
- Plug and play displays
- Simple clean interface
- On or offline mapping
- Basic positioning
- Heatmap of spray area

#### Medium Term
- Peer-to-peer communication
- High precision positioning
- Mapping activities, seeding, harvesting, spraying.
- Machine messaging
- Timing of tasks


#### Long Term
- Machine interfacing
- Vision systems
- Navigation
- Machine health and diagnostics


#### Dream Big
- Self driving autonomous machines
- Individual plant health recognition vision system
- Machine learning optimization of routes
- End-to-end crop cycle management

### Principles
- High precision farming at the smallest possible cost.
- Intuitive and simple as possible.
- Versatile, work on anything with a screen.
- Primarily developed for RasberyPi, or other cheap hardware.
- Ad-hoc peer-to-peer communication.
- Swappable hardware, easily put in any machine.

### Design
- Primarily written in python
- WebUI interface
- Initially using django for web framework
- Seperate backend and frontend 
- Backend processes and logs data to sqlite
- Serve live position and other real-time data to simple .json http GET
- Django frontend for local and remote WebUI
- Leaflet mapping with custom tiles and layers.
- Primary buttons and info overlayed ontop of map
- Boot to kiosk mode sort of thing.
- Consideration for multiple GPS receivers, on spray booms and whatever.
- Plug and play add on hardware such as additional sensors / IO / stereo output / additional screens / whatever





