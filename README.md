# patches-tool

## Overview

This tool helps users to search for contributions in the upstream QEMU and Linux Kernel repositories.
It list the commits that have been tagged with `Tested-by` or `Reported-by` filtering  by the email ID.
This is useful for developers, maintainers, and contributors who want to track specific reports and tests related to the changes made in these repositories.

## Features

- Search into the QEMU and Linux Kernel upstream repositories.
- Filter by `Tested-by` tag.
- Filter by `Reported-by` tag.

## Prerequisites

Before using this tool, ensure that you have Python 3.6+ installed and run the `setup.py` which will install **Git** if needed and clone the QEMU and Kernel repositories. 

> **Important:** QEMU and Linux Kernel paths should be updated in `patches_search.py`
