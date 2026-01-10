from setuptools import setup, find_packages

setup(
    name="situational-awareness-system",
    version="0.1.0",
    description="A situational awareness system for vessel tracking",
    author="anjali-vb",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
)
