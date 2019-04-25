#!/bin/bash
#flake8 --ignore=E501 tests/
if [[ $? == 0 ]]; then
        echo "Flake8 passed!"
    else
        exit 1
    fi

mkdir -p report
nose2 --verbose --plugin nose2.plugins.junitxml --plugin=nose2.plugins.mp -N20 -s tests/api -c unittest.cfg
