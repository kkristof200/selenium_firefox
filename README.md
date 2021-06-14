# selenium_firefox



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