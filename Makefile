# Makefile for tm_simulator

.PHONY: all clean

# Default target
all: tm_simulator

# Create the tm_simulator executable
tm_simulator:
	echo '#!/usr/bin/env python3' > tm_simulator
	cat tm_simulator.py >> tm_simulator
	chmod +x tm_simulator

# Clean up generated files
clean:
	rm -f tm_simulator
