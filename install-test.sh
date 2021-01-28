#!/bin/sh

pip install --upgrade pip || exit 1
pip install coverage pytest || exit 1
pip install -e .[test] || exit 1
