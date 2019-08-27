#!/bin/bash
mkdir -p results
behave --verbose --junit --junit-directory results -s ui/features/
