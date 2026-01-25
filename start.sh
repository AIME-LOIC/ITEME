#!/bin/bash

# ITEME Application Startup Script
# Runs the integrated FastAPI application with both arrival and payment modules

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}   ITEME Application Startup${NC}"
echo -e "${BLUE}================================${NC}"

# Check if virtual environment exists
if [ ! -d "installed" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating...${NC}"
    python3 -m venv installed
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source installed/bin/activate

# Install/upgrade dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -q -r requirements.txt

echo -e "${GREEN}✓ Setup complete!${NC}"
echo ""
echo -e "${BLUE}Available Routes:${NC}"
echo -e "  ${GREEN}Main App${NC}"
echo "    GET  http://localhost:8000/              - Arrival form"
echo "    POST http://localhost:8000/arrival       - Submit arrival"
echo "    GET  http://localhost:8000/arrival/admin - Arrival admin panel"
echo "    POST http://localhost:8000/activate/{id} - Activate student"
echo ""
echo -e "  ${GREEN}Payment Module (mounted at /payment)${NC}"
echo "    GET  http://localhost:8000/payment/           - Payment form"
echo "    POST http://localhost:8000/payment/api/submit - Submit payment"
echo "    GET  http://localhost:8000/payment/admin      - Payment admin panel"
echo ""
echo -e "  ${GREEN}API Docs${NC}"
echo "    http://localhost:8000/docs       - Swagger UI"
echo "    http://localhost:8000/redoc      - ReDoc"
echo ""
echo -e "${BLUE}Starting server on http://localhost:8000${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
echo ""

# Run the application
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
