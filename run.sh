#!/usr/bin/env bash

set -e

if [ ! -f "./xmir_base/xmir_init.py" ]; then
	echo "ERROR: XMiR: Current working directory is not correct!"
	return 1
fi

PY3_PATH=`which python3`
if [ "$PY3_PATH" = "" ]; then
	echo "ERROR: XMiR: python3 binary not found!"
	return 1
fi

if [ "$VIRTUAL_ENV" = "" -o ! -e "$VIRTUAL_ENV/bin/python3" ]; then
	CLEAN_INSTALL=true
	[ -e "./venv/pyvenv.cfg" ] && CLEAN_INSTALL=false
	python3 -m venv venv
	if [ ! -e "./venv/bin/activate" ]; then
		echo "ERROR: XMiR: python3 venv not initialized!"
		return 1
	fi
	source ./venv/bin/activate
	PY3_PATH=`which python3`
	if [ "$PY3_PATH" = "" ]; then
		echo "ERROR: XMiR: python3 venv binary not found!"
		return 1
	fi
	if [ "$CLEAN_INSTALL" = "true" ]; then
		python3 -m pip install -r requirements.txt
	fi
fi

if [ "$VIRTUAL_ENV" = "" -o ! -e "$VIRTUAL_ENV/bin/python3" ]; then
	echo "ERROR: XMiR: python3 binary not founded!"
	return 1
fi

export PYTHONUNBUFFERED=TRUE

if [ "$1" = "" ]; then
	python3 menu.py
else
	python3 "$@"
fi

#deactivate