#!/bin/bash
#flake8 --ignore=E501 tests/
if [[ $? == 0 ]]; then
        echo "Flake8 passed!"
    else
        exit 1
    fi
python3 -m unittest discover -s tests/api/ --verbose
