# Clue Module for Kodi

**Clue Module** package is designed to be used as primary API and library
layer for all Kodi add-ons in correlation with the all **Clue** addons.

This addon doesn't require any dependency and run over any Python version,
but is expecting to find the os OS level the following Python livrariers:
 - `re` (it has to be embedded in Python environment)
 - `xbmc` (Kodi Python API) 
 - `urllib3` (for Python 2.7 and Python 3)
 - `locale` (Internationalization services)
 - `subprocess` (typically is embedded in Python environment)

Development, testing and deployment activities are driven by CCM process (Clue 
Configuration Management), built over GNU `make` utility. To see all make rules
try `make help`.

_Enjoy!_
