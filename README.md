# Farmstar
High precision farm management system.

*NOTE: This is a side project, progress is slow.*

![Logo v1.2](/docs/media/logo-small.png?raw=true)

## Vision
Help feed 10 billion people by 2050.

### Farming Industry problems
- Expensive proprietary hardware and software in machines.
- Complicated unintuitive interfaces.
- Seeding, spraying, harvesting inefficiencies.
- Aging farming expertise.
- Fully autonomous tractors are kinda expensive.
- Some farms here in Australia are bigger than entire countries, mate.

### Principles
- High precision farming at the smallest possible cost.
- Intuitive and simple as possible.
- Versatile, work on anything.
- Primarily developed for RasberyPi, or other cheap hardware.
- Ad-hoc peer-to-peer communication.
- Plug and play hardware, easily put in any machine.

### Components
#### Frontend
- Angular 6 / Node.js / Electron
#### Backend
- Python for data acquisition
#### Hardware
- Raspberry Pi or other cheap SBC
#### Communications
- Combination WiFi Mesh and cellular



### Screenshots-Large

*Version 2*

![Map v2](/docs/media/screenshots/map_large.PNG?raw=true)
![Apps v2](/docs/media/screenshots/apps_large.PNG?raw=true)

### Screenshots-Mobile

*Version 2*

![Map-mobile v2](/docs/media/screenshots/map_mobile.PNG?raw=true)
![Apps-mobile v2](/docs/media/screenshots/apps_mobile.PNG?raw=true)

### Goals
*See TODO / wiki / project board for specific project goals*

#### Short Term
- Plug and play displays
- Simple clean interface
- Basic positioning
- Heatmap of spray area

#### Medium Term
- Live positioning of multiple devices
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



### Design (v2)
- Backend written in python for data acquisition
- Frontend developed in Angular 6 / Node.js
- Compiled into electron for standalone portability
- Considering google firebase platform
- Serve live position and other real-time data to simple .json http GET
- Mapbox mapping
- Primary buttons and info overlayed ontop of map
- Consideration for multiple GPS receivers, on spray booms and whatever.
- Plug and play add on hardware such as additional sensors / IO / stereo output / additional screens / whatever





