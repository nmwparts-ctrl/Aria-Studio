
# AriaStudio Bridge Service

> **Important**: This service runs as the **backend core** of the **AriaStudio** ecosystem. It is **not intended for modification** by end users. If you have specific requirements or encounter issues, please contact us at:  
> 📧 **service@dspixel.com**

---

## Overview

The `Aria Bridge.py` script is a lightweight Flask‑based bridge service that acts as the **data and command hub** between your PC (running AriaStudio) and the AriaStudio terminal device.

It handles:

- **HTML template hot‑reloading** – push and store custom dashboards.
- **Video file management** – upload and store background videos.
- **Voice file storage** – store AI‑generated voice responses.
- **System telemetry** – receive and aggregate PC performance data (CPU, memory, temperature, etc.).
- **Heartbeat & binding** – maintain a persistent connection with the PC client.
- **Reverse control** – forward commands from the A527 terminal to the PC (e.g., keyboard shortcuts, URL launches).


---

