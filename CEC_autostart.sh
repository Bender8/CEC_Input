#!/bin/bash
#Wait for thigs to settle out
sleep 5
cd /home/bender/Python/CEC_Input
#Launch CEC_input script using they virtual environment
/home/bender/Python/CEC_Input/.venv/bin/python3 /home/bender/Python/CEC_Input/CEC_input_class.py
