#!/bin/bash
coverage run -m pytest travis_test.py
coverage report -m
