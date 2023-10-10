# SENSOR FAULT CLASSIFIER
The system in focus is the Air Pressure system (APS) which generates pressurized air that is utilized in various functions in a truck, such as braking and gear changes. The datasets' positive class consists of component failures for a specific component of the APS system. The negative class consists of trucks with failures for components not related to the APS. The data consists of a subset of all available data, selected by experts.

The total cost of a prediction model the sum of Cost_1 multiplied by the number of Instances with type 1 failure and Cost_2 with the number of instances with type 2 failure, resulting in a Total_cost. In this case Cost_1 refers to the cost that an unnecessary check needs to be done by an mechanic at an workshop, while Cost_2 refer to the cost of missing a faulty truck, which may cause a breakdown. Cost_1 = 10 and Cost_2 = 500, and Total_cost = Cost_1*No_Instances + Cost_2*No_Instances.



## __> Create virtual enviroment__  
    - conda create -p venv python=3.9 -y

## __> Create a setup.py file__
    The complete information about the project is mentioned in setup.py file 

## __> Compile template.py file__ 
    This .py file builds the entire project project

## > __Create .env file for Enviroment Variables__ 
    To keep confidentiality and easy access to the API credentials and access codes for production as well as training pipelines 

   > __We create enviroment class to access the variables inside the .env file.__

## __> Create utils.py for Accessing function which would be called many times__ 

## __> __Set up for Input and Output for Each Component__ 
    - Create Folder entity initialise it as a module compile two .py scripts for input and ouput__  
***__Feature_Store  folder is a naming convention used in MLOPS, This is where the pipeline begins.__***


***DataClass***

 __Shortcut for  automatically adding generated special methods such as __init__() and __repr__() to user-defined classes.__