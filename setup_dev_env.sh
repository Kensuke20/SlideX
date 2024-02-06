#!/bin/bash

if [ ! -e venv_SlideX/bin/activate ]; then
	python3 -m venv venv_SlideX
fi
source venv_SlideX/bin/activate

# required python library
REQUIREMENTS_LIST=("Flask")

for requirement in ${REQUIREMENTS_LIST[@]};
do
	pip freeze | grep $requirement
	if [ $? -ne 0 ]; then
		pip install $requirement
	fi
done
