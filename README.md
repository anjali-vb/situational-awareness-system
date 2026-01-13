# Situational Awareness System - WebSocket Server

A real-time vessel tracking and situational awareness system using WebSocket communication.

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## Installation

### 1. Clone or navigate to the project directory

```bash
cd situational-awareness-system
```

### 2. Install dependencies

Install the package and its dependencies using the system Python:

```bash
pip install -e .
```

This will install the package and required dependencies including `websockets>=12.0`.

## Running the Server

### Start the WebSocket server

```bash
python src/server.py
```

You should see output similar to:

```
2026-01-12 23:24:57,915 - INFO - Starting WebSocket server on ws://localhost:8765
2026-01-12 23:24:57,996 - INFO - server listening on 127.0.0.1:8765
2026-01-12 23:24:57,996 - INFO - server listening on [::1]:8765
2026-01-12 23:24:57,996 - INFO - WebSocket server is running
2026-01-12 23:24:57,996 - INFO - Open the index.html file directly in your browser to connect
```

## Accessing the Application

1. The WebSocket server runs on `ws://localhost:8765`
2. Open the `src/index.html` file directly in your web browser
3. The browser will establish a WebSocket connection to the running server

**To open index.html:**

- Navigate to `src/` folder and double-click `index.html`, or
- Right-click `index.html` → "Open with" → Select your web browser, or
- Copy the file path and open it in your browser (e.g., `file:///C:/path/to/situational-awareness-system/src/index.html`)

## Project Structure

```
situational-awareness-system/
├── setup.py                 # Package configuration and dependencies
├── README.md               # This file
├── src/
│   ├── server.py           # WebSocket server
│   ├── index.html          # Web interface
│   ├── world.py            # World/simulation management
│   ├── simulation.py       # Simulation logic
│   ├── vessel.py           # Vessel class
│   ├── position.py         # Position handling
│   ├── motion.py           # Motion calculations
│   ├── alert.py            # Alerting system
│   ├── risk.py             # Risk assessment
│   └── cpa.py              # Closest Point of Approach calculations
└── tests/                  # Test suite
```

## Troubleshooting

### WebSocket Connection Failed

- Ensure the server is running (`python src/server.py`)
- Check that port 8765 is not blocked by your firewall
- Verify the WebSocket URL in index.html matches `ws://localhost:8765`

### Module Not Found Error

- Ensure you've installed the package: `pip install -e .`
- Verify you're using the correct Python environment (check with `which python` or `where python`)

### Permission Denied Error

- On Windows, check if port 8765 is already in use: `netstat -ano | findstr :8765`
- Try running in administrator mode if necessary

## Running Tests

You can run the test suite using the Python standard library's unittest discovery (no external test runner required):

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Development Notes

- The server uses Python's `asyncio` library for asynchronous WebSocket handling
- The websockets library (v12.0+) is required for WebSocket support
- All dependencies are automatically installed via setup.py
