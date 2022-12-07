from setuptools import setup


def find_required():
    with open("requirements.txt") as f:
        return f.read().splitlines()


setup(
    name="vedro-replay",
    version="0.1.1",
    description="vedro-replay package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="2GIS Test Labs",
    author_email="test-labs@2gis.ru",
    python_requires=">=3.9",
    url="https://github.com/2gis-test-labs/vedro-replay",
    license="Apache-2.0",
    packages=['vedro_replay'],
    install_requires=find_required(),
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        "console_scripts": [
            "vedro-replay-generate = vedro_replay:generation",
        ],
    },
    include_package_data=True,
)
