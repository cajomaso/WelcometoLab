### Welcome to Digi Lab

This is game is set in the Digital Media Lab, which is open to all Digital Media Students. 
You are a new student visiting the Lab for the first time. In the Lab you meet other Digital Media Students from higher Semester. 
Get to know them and their quirks. You might even trigger a special event.


<img src="media/WelcometoDigiLab.png" width="300">

---
#### Installation

First clone the repository.
Also make sure to have the following installments:
```
pip install -r requirements.txt
import pygame
import sys
import os
import json
import time
```

#### Usage
When you have access to all the files in your environment you can start the game by writing following in the terminal:
```
python main.py
```


---
### WelcometoDigiLab | Structure


```
WelcometoLab/
├── main.py
├── settings.py
├── states.py
├── UI.py
├── media/
├── savefiles/
├── .gitignore
├── README.md
├── requirements.txt
└── documentation.md
```

- `main.py`: Game logic
- `settings.py`: All the parameters for hitboxes, character texts, UI Colors, etc.
- `states.py`: All the screens, including events
- `UI.py`: User Interface -> DropDown Menu and Hitboxes.
- `media/`: All my drawings for the game
- `.gitignore`: safety first
- `LICENSE`: Charges are coming 
- `README.md`: <- This me, Hello!
- `requirements.txt`: required
- `documentation.md/pdf`: This is the extra/detailed documentation file that needs to be submitted along with the final project. It can include:
  - Initial sketches(/plan) and research - (This can be recycled from your intermediate presentation)
  - Development process and challenges
  - Future improvements and known limitations
  - References
  - Any other things that makes sense to put here for your project
