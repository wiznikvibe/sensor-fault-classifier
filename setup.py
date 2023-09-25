from setuptools import find_packages, setup
from typing import List

def get_requirements(file_path:str)->List[str]:
    """
    This Function returns list of packages to be installed 
    """
    HYPEN_E_DOT = "-e ."

    with open(file_path) as file_obj:
        requirement = file_obj.readlines()
        requirements = [req.replace('\n','') for req in requirement]
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements


setup(
    name="sensor_fault_classifier",
    version='0.0.1',
    author='nikhil',
    author_email='nikhilshetty439@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements(requirements)
)