## Data Science Project

__> Create virtual enviroment__  
    - conda create -p venv python=3.9 -y

__> Create a setup.py file__
    The complete information about the project is mentioned in setup.py file 

__> Compile template.py file__ 
    This .py file builds the entire project project

> Create .env file for Enviroment Variables 
    To keep confidentiality and easy access to the API credentials and access codes for production as well as training pipelines 

   > __We create enviroment class to access the variables inside the .env file.__

__> Create utils.py for Accessing function which would be called many times__ 

__> Set up for Input and Output for Each Component 
    - Create Folder entity initialise it as a module compile two .py scripts for input and ouput__  
***__Feature_Store  folder is a naming convention used in MLOPS, This is where the pipeline begins.__***

***DataClass***
 __Shortcut for  automatically adding generated special methods such as __init__() and __repr__() to user-defined classes.__