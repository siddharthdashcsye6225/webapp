from setuptools import setup, find_packages

# Function to read requirements from requirements.txt
def parse_requirements(filename):
    with open(filename) as f:
        return f.read().splitlines()

setup(
    name='webapp',
    version='1.0.0',
    description='A web application using FastAPI',
    author='Siddharth Dash',
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
)
