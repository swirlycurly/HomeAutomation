from setuptools import setup

setup(
    name="kasaoutlet",
    version="0.1.0",
    py_modules=["kasaoutlet"],
    install_requires=[
        "Click",
        "logging",
        "kasa",
        "asyncio",
    ],
    entry_points={
        "console_scripts": [
            "kasastate= kasaoutlet:query_state",
        ],
    },
)
