VITYARTHI 2026 PYTHON PROJECT
ENIVORMENTAL DEPENDANCY - This project is engineered with a Zero-Dependency Reliability framework. It runs entirely on the native Python Standard Library, meaning no third-party runtime dependencies or package installations are required to run the core simulation application.
Python 3.10 or higher installed on your operating terminal.
PROJECT CONFIGRATION- Contains the scientific emission weights and baseline operational constants (such as the default idle state of 0.15 W/kg or network weights). If you need to tweak the simulation variables or threshold ceilings, modify this file directly before execution.
EXECUTION AND RUNNING THE VERIFICATION : This file acts as the persistent storage ledger where your calculated exposure records append automatically. The engine will look for or initialize this local ledger file upon boot.
The main entry point, interactive user interface loop, and route manager are handled inside src/main.py.To
