Changelog
=========

0.3.0 - 2021-02-08
------------------
* Added mob_skill_db.txt converter
* Updated dependencies:
    - packaging (20.8 -> 20.9)
    - virtualenv (20.2.2 -> 20.4.2)
    - pytest (6.2.1 -> 6.2.2)
    - tox (3.21.0 -> 3.21.4)
    - pyyaml (5.3.1 -> 5.4.1)

0.2.5 - 2021-01-23
------------------
* Excluded max level when value is 999

0.2.4 - 2021-01-15
------------------
* Added view to converted output

0.2.3 - 2021-01-14
------------------
* Fixed config failing during first call in clean install

0.2.2 - 2021-01-10
------------------
* Fixed config not loading saved values correctly

0.2.1 - 2021-01-10
------------------
* Fixed issue with loading ~/.dp2rathena.conf

0.2.0 - 2021-01-09
------------------
* Added support for Python 3.6
* Added "config" CLI command for storing API key
* Changed interface for "item" CLI command
* Changed interface for "dp2rathena" base command to allow passing API key
* Added codecov.io integration

0.1.1 - 2021-01-07
------------------
* Fixed build pipeline issues with TravisCI and PyPI

0.1.0 - 2021-01-06
------------------
* Initial Release
* Added ability to convert divine-pride item data to rathena yaml
