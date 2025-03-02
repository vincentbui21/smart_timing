# Smart timing project _ Vincent Bui & Eric Darko

## Overview

This project consists of a Raspberry Pi server and ESP32-based cones that communicate over WiFi. The server provides a UI for monitoring and managing the system, while the ESP32 cones establish a connection to the server.

## Server-Side (Raspberry Pi)

### Requirements

- Raspberry Pi (any model with WiFi capability)
- Python installed
- Streamlit installed

### Setup & Running the Server

#### First-Time Setup

If this is the first time running the project, follow these steps:

1. Navigate to your project directory:
   ```sh
   cd /path/to/your/project
   ```

2. Create a virtual environment named `.venv`:
   ```sh
   python -m venv .venv
   ```

3. Activate the virtual environment:
   ```sh
   source .venv/bin/activate
   ```

4. Install the required dependencies:
   ```sh
   pip install streamlit mysql-connector-python
   ```

5. Run the setup script:
   ```sh
   python first_time_setup.py
   ```

#### Normal Execution

Before starting the server, activate the virtual environment:
```sh
source .venv/bin/activate
```

To start the server, run:

```sh
python -m streamlit run ui.py --server.port 8502
```

#### Accessing the UI

Once the server is running, open your browser and navigate to:

```
http://localhost:8502
```

Ensure that the Raspberry Pi is connected to the same WiFi network as the ESP32 cones.

---

## ESP32 Cones

### Setup & Connection

1. Ensure the ESP32 cones are fully charged.
2. Power up the ESP32.
3. Observe the LED behavior:
   - If all LEDs are blinking fast, the cone has successfully connected to the WiFi network and is ready to communicate with the server.
4. Press the **big button** on the ESP32 cone to initiate the connection with the server.
   - If all LEDs light up and stop blinking, the connection has been successfully established.

---

## Notes

- Ensure that the Raspberry Pi server and ESP32 cones are connected to the same WiFi network.
- If connection issues occur, restart both the Raspberry Pi and ESP32 cones, then retry the steps above.

For further troubleshooting or modifications, refer to the project documentation.

