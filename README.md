# selenium_firefox

![PyPI - package version](https://img.shields.io/pypi/v/selenium_firefox?logo=pypi&style=flat-square)
![PyPI - license](https://img.shields.io/pypi/l/selenium_firefox?label=package%20license&style=flat-square)
![PyPI - python version](https://img.shields.io/pypi/pyversions/selenium_firefox?logo=pypi&style=flat-square)
![PyPI - downloads](https://img.shields.io/pypi/dm/selenium_firefox?logo=pypi&style=flat-square)

![GitHub - last commit](https://img.shields.io/github/last-commit/kkristof200/selenium_firefox?style=flat-square)
![GitHub - commit activity](https://img.shields.io/github/commit-activity/m/kkristof200/selenium_firefox?style=flat-square)

![GitHub - code size in bytes](https://img.shields.io/github/languages/code-size/kkristof200/selenium_firefox?style=flat-square)
![GitHub - repo size](https://img.shields.io/github/repo-size/kkristof200/selenium_firefox?style=flat-square)
![GitHub - lines of code](https://img.shields.io/tokei/lines/github/kkristof200/selenium_firefox?style=flat-square)

![GitHub - license](https://img.shields.io/github/license/kkristof200/selenium_firefox?label=repo%20license&style=flat-square)

## Description

User-friendly implementation of a firefox based selenium client

## Features
- Easily create a firefox selenium webdriver with proxy(host/port), extensions and other settings, such as, full-screen-window,
private session.
- Override user-agent
- Easily save and load cookies for websites

## Install

~~~~bash
pip install selenium_firefox
# or
pip3 install selenium_firefox
~~~~

## Usage

~~~~python
from selenium_firefox import Firefox

ff = Firefox()
ff.get('https://www.google.com')

import time
time.sleep(999)
~~~~

## Dependencies

[geckodriver-autoinstaller](https://pypi.org/project/geckodriver-autoinstaller), [kproxy](https://pypi.org/project/kproxy), [noraise](https://pypi.org/project/noraise), [selenium](https://pypi.org/project/selenium), [selenium-browser](https://pypi.org/project/selenium-browser)