#! /usr/bin/env python3
# coding: utf-8

from Database import Database
from Setup import Setup
from Input import Input


class Main:

    def __init__(self):
        Setup()
        Input()

Main()