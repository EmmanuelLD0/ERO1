# ERO1 - Clearing Snow in Montreal

## 🤓 Team Members

- Raj Mahajan
- David Calderon
- Maxime Bardouil
- Terence Miralves
- Emmamnuel Le Dreau

## ✨ Introduction
People from Montréal are concerned with snowplowing operations, but increasing the allowed funds
is still a delicate point for the city council [Lef19], and it is now an objective to reduce these operations cost,
while still providing an effecient snowplow service to the inhabitants. The city tasks your company with a study.
The goal is to minimize the cost of a typical snowplowing day. Our’s role is to find a short enough path
for the snowplows around the Montréal road network, while still remove snow from the whole given zone.

## 📂 File Structure
```bash
.
├── AUTHORS
├── Doxyfile
├── images
│   └── montreal.png
├── main.sh
├── README.md
├── requirements.txt
├── setup.sh
├── src
│   ├── demo.py
│   ├── drone_flight
│   │   ├── flight_creator.py
│   │   └── __init__.py
│   ├── equipement
│   │   ├── drone.py
│   │   ├── __init__.py
│   │   └── snowplow.py
│   ├── graphical_interface.py
│   ├── __init__.py
│   ├── removal_planning
│   │   ├── __init__.py
│   │   └── planning.py
│   └── tools
│       ├── dijikstra.py
│       ├── display.py
│       └── __init__.py
├── tests
│   ├── dijikstra.py
│   ├── graph_doc_test.py
│   └── init.py
└── test.sh
```

```
./src/graphical_interface.py - Runs the UI for the demo
./src/equipement/* - Classes for drones and snowplows
./src/drone_flight/* - Creates path for the drones
./src/removal_planning/* - Creates path for the snowplows
./src/tools/* - Supporting algorthims used
./tests/* - Tests for tools functions
```

## 📝 Dependencies / Setup
```bash
./setup.sh
```

### Depending on your system
Arch Linux
```
sudo pacman -S tk
```

Debian Based System
```
apt-get install python-tk
```

## 🚀 Build System
To run the demo
```
./main.sh
```

## :scroll: Documentation
```
firefox documentations/html/index.html
```
