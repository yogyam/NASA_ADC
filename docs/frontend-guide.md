# NASA_ADC - Frontend Developer Guide

## 🎯 Project Overview

This project provides a backend system for visualizing lunar terrain data in 3D.  From a frontend perspective, you'll be interacting with a pre-built 3D environment powered by the Ursina engine. Your role will focus on integrating this 3D visualization into a larger frontend application, potentially enhancing its user interface, adding features, and customizing the visual presentation of the lunar data.  You won't need to directly modify the core data processing or pathfinding algorithms, but understanding the data structures they produce is crucial for effective integration.  Think of the backend as a powerful API serving rich 3D scenes.


## 🚀 Quick Start for Frontends

This guide assumes you have a basic understanding of HTML, CSS, and JavaScript.  The core interaction with the backend happens through the Ursina engine, which is handled server-side.  Your focus will be on integrating the Ursina application into your frontend.

**1. Install Ursina (if needed):**

While the backend handles Ursina's heavy lifting, you might need to familiarize yourself with it for advanced customization or debugging. Installation (if needed):

```bash
pip install ursina
```

**2. Clone the Repository:**

```bash
git clone <repository_url>
```

**3. Run the Backend (typically `main.py` or `main2.py`):**

The backend needs to be running to serve the 3D scene.  The exact command will depend on your environment, but it will likely be something like:

```bash
python main.py
```

This starts a local server (most likely Ursina's built-in server).  Note the port the server is using (usually a default).

**4. Integrate into your Frontend:**

You'll likely embed the 3D visualization within an `<iframe>` element in your HTML. Replace `<your_server_ip_or_localhost>` and `<port>` with your actual server information.

```html
<!DOCTYPE html>
<html>
<head>
<title>NASA Lunar Terrain</title>
</head>
<body>
  <iframe src="http://<your_server_ip_or_localhost>:<port>" width="800" height="600"></iframe>
</body>
</html>
```

**5.  Interact and Customize:**

Now you can interact with the 3D lunar terrain within your frontend application. Further customization will likely involve understanding the data structures (e.g., coordinates, heightmaps) exposed by the backend (through potential APIs - if added in future)  to allow for dynamic updates and user interactions.


## 🏗️ Architecture Overview

From a frontend perspective, the architecture is relatively simple.  The backend acts as a server rendering a 3D scene using Ursina. Your frontend acts as a client that embeds this scene using an `<iframe>`.  The communication is implicit; the backend serves the 3D application, and the frontend displays it. No direct API calls or data exchange are initially required.


## 🔧 Key Components

* **Ursina Engine (Backend):**  Handles the rendering of the 3D environment. This is a black box for frontend developers, requiring minimal direct interaction.
* **Data Visualization (Backend):** The backend processes and visualizes lunar data. This provides the 3D scene displayed in the frontend.
* **Frontend Integration Point (HTML):** The `<iframe>` element acts as the interface between your frontend and the backend's 3D application.


## 📦 Dependencies & Tools

From a frontend perspective, you primarily need to be familiar with:

* **HTML:** For embedding the 3D scene using `<iframe>`.
* **CSS:** For styling the overall layout of your frontend application, integrating the iframe seamlessly.
* **JavaScript:**  For enhancing user interaction, handling any potential dynamic updates with the scene (if future API is created).
* **Ursina (Indirect):**  Understanding Ursina's basic functionality is beneficial for debugging and for advanced integrations in future.


## 🛠️ Development Workflow

1. **Understand the Backend:** Familiarize yourself with the capabilities of the backend (data visualization types, potential user interaction points).
2. **Frontend Integration:** Embed the Ursina application using an `<iframe>`.
3. **UI/UX Design:** Design your frontend's user interface to integrate the 3D visualization seamlessly.
4. **Testing:** Verify that the 3D scene renders correctly and integrates smoothly within your application.


## 🧪 Testing & Debugging

Testing will mostly focus on verifying the correct display and integration of the 3D scene within your frontend.

* **Browser Developer Tools:** Use your browser's developer tools to inspect the `<iframe>` and troubleshoot any rendering issues.
* **Backend Debugging (if necessary):** If you need to debug backend issues, refer to the backend documentation and use appropriate debugging tools for Python.


## 📚 Additional Resources

* **Ursina Documentation:** [Link to Ursina's documentation]  (This will be helpful if you're planning advanced customization).
* **NASA's ADC website:** [Link to NASA's ADC website] (for understanding the data source).


Remember that this guide focuses on the frontend perspective.  Direct interaction with the complex data processing elements of the backend is not necessary for basic integration.  If you need to interact more deeply, future API additions could simplify that process, improving flexibility.
