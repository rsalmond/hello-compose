#!/bin/bash

unset HELLO_BINDS_SLAVE
unset HELLO_BINDS_MASTER

HELLO_TESTING=True HELLO_BINDS_MASTER=sqlite:// nosetests -s
