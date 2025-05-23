from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    """
    This function returns a list of requirements.
    """

    requirement_list: List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()

            for line in lines:
                requirement = line.strip()
                # Ignoring empty lines and -e line
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found. Please ensure it exists in the current directory.")

    return requirement_list

setup(
    name = "NetworkSecuritySystem",
    version = "0.0.1",
    author = "Ben GJ",
    author_email = "bengj1015@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements()
)