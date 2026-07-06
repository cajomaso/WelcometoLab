### Welcome to Digi Lab

A README.md file is often the first thing people see from your project. Begin your README.md with a brief, compelling description of what your project does. Consider adding a feature image or demo GIF here to showcase your project visually.

<img src="media/WelcometoDigiLab.png" width="300">
<img src="media/comment.jpeg" width="300">

#### Installation
If your project includes any 3rd-party libraries, you shall include an Installation section. For your project, it might look like this:

Install required dependencies:
```
pip install -r requirements.txt
pip install pygame
pip install time
```

#### Usage
Here you shall provide instructions on how to run your project in command line. This is especially important if your project have multiple `.py` files. And it probably looks like this:
```
python title.py
```
(Even if you are just running your python files from your IDE or installing your libraries from the code editor, it's still important to have these two sections in your README file.)

---
### Sample Project

This repository is an example structure for a standalone project and is created to provide guidance for people who are relatively new to Python.
Here is a sample project structure for a final project for Technical Basics I.

```
Firstname_Lastname_Title/
├── title.py
├── (helper.py)
├── media/
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── documentation.md (or documentation.pdf)
```

- `title.py`: The entry point of your application. This should contain your primary logic and be the file users run to start your program.
- `helper.py`: In case you want to split your project into multiple files, you might have more than one `.py` files in your repository. Name them in meaningful way (Ex: if you have a separate file for the class Ghost, name it `ghost.py`)
- `media/`: Please put all non-code assets into one folder (images, sounds and fonts), so that the rest of your project structure can stay clean. 
- `.gitignore`: If you are using git to manage your project, it is important to add a `.gitignore` file to your folder so that you won't accidentally commit something that you don't want to (ex: your virtual environment).
- `LICENSE`: [Optional] When we are uploading our code to GitHub as public repository, we are open sourcing our code. Common types of Open Source Licenses are `MIT`, `Apache` and `GPL`. You can read more about this topic [here](https://gist.github.com/nicolasdao/a7adda51f2f185e8d2700e1573d8a633).
- `README.md`: See this file.
- `requirements.txt`: A list of libraries to be installed by pip. Generated with `pip freeze > requirements.txt`
- `documentation.md/pdf`: This is the extra/detailed documentation file that needs to be submitted along with the final project. It can include:
  - Initial sketches(/plan) and research - (This can be recycled from your intermediate presentation)
  - Development process and challenges
  - Future improvements and known limitations
  - References
  - Any other things that makes sense to put here for your project
