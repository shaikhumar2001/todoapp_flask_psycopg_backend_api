#!/bin/bash

# Exit on error
set -e

# --------- COLORS ---------
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
MAGENTA='\033[1;35m'
CYAN='\033[1;36m'
NC='\033[1;37m' # no color
# --------------------------

# --------- CONFIG ---------
PORT=${1:-5000}
HOST="0.0.0.0"
PROJECT_DIR="/home/administrator/dev/todoapp_flask_psycopg_backend_api" # change if needed
VENV_DIR="venv"
# --------------------------

echo -e "${CYAN}=========================================${NC}"
echo -e "${GREEN}⚡ Starting Flask Development Server${NC}"
echo -e "${CYAN}=========================================${NC}"

# go to project directory
if [ -d "$PROJECT_DIR" ]; then
	echo -e "${MAGENTA} 📂 Redirecting to project directory: $PROJECT_DIR${NC}"
	cd "$PROJECT_DIR"
else
	echo -e "${RED} ❌ Project directory not found: $PROJECT_DIR${NC}"
	exit 1
fi

# activate virtual environment
if [ -f "$VENV_DIR/bin/activate" ]; then
	echo -e "${MAGENTA} 💠 Activating virtual environment via $VENV_DIR/bin/activate ...${NC}"
	. "$VENV_DIR/bin/activate"
else
	echo -e "${RED} ❌ Virtual environment not found in $VENV_DIR${NC}"
	exit 1
fi

# set environment variables
export FLASK_ENV=development
export HOST=$HOST
export PORT=$PORT

echo -e "${YELLOW}------------------------------------${NC}"
echo -e "${CYAN} 🌐 HOST:${NC} ${GREEN}$HOST${NC}"
echo -e "${CYAN} 🔌 PORT:${NC} ${GREEN}$PORT${NC}"
echo -e "${YELLOW}------------------------------------${NC}"

echo -e "${GREEN} 🚀 Launching Flask app...${NC}"

# run flask app
python3 server.py

echo -e "${CYAN}============================================${NC}"
