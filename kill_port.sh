#!/bin/bash

# exit if error
set -e

# source colors
. "$(dirname "$0")/terminal_colors.sh"

PORT=$1

# check if the argument was provided
if [ -z "$PORT" ]; then
	echo -e "${RED}Please provide a port number.${NC}"
	exit 1
fi

# check if PORT is a valid number
if ! echo -n "$PORT" | grep -q -E '^[0-9]+$'; then
	echo -e "${YELLOW}$PORT is not a valid port number.${NC}"
	exit 1
fi

# find the PID using the port
PID=$(lsof -t -i :"$PORT" || true)

if [ -z "$PID" ]; then
	echo -e "${CYAN}No process found running on port $PORT.${NC}"
	exit 0
fi

kill -9 $PID

echo -e "${MAGENTA}PIDs:${NC} "$PID""
echo -e "${GREEN}running on port $PORT killed successfully 👍${NC}"

