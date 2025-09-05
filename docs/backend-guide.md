# NASA_ADC - Backend Developer Guide

## 🎯 Project Overview

This project provides the backend infrastructure for processing and generating lunar terrain data, crucial for applications requiring realistic lunar simulations or visualizations. From a backend perspective, this repository focuses on data manipulation, algorithm implementation (A* pathfinding, Perlin noise generation), and efficient data management.  The frontend visualization (using Ursina) is secondary; the core functionality crucial to backend developers lies in the robust data processing and algorithm implementation.  This allows for the creation and modification of lunar terrain datasets without requiring interaction with the Ursina visualization components.

## 🚀 Quick Start for Backends

This guide focuses on setting up the backend components only.  The Ursina-related parts can be skipped if you are solely interested in the data processing and algorithm functions.

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd NASA_ADC
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**  Note that we only need a subset of the dependencies for the backend.  Remove Ursina related dependencies and any purely frontend visualization packages from `requirements.txt`. Install remaining dependencies with pip:
   ```bash
   pip install -r requirements.txt  # After modifying requirements.txt accordingly.
   ```

4. **Test Core Backend Functionality:** Run unit tests (see Testing & Debugging section) to verify core data processing and algorithm modules are working correctly.  For example, you can directly call functions from `DataProcessor`, `DataProcessorPerlinNoise`, or `astar` modules to test individual components.


## 🏗️ Architecture Overview

The backend architecture is modular, with core modules focusing on distinct functionalities:

* **`DataProcessor`:** Loads raw lunar data (from NASA ADC) and performs transformations (e.g., coordinate conversions).  This is the primary data ingestion and pre-processing layer.
* **`DataProcessorPerlinNoise`:** Generates Perlin noise heightmaps, adding realistic texture to the lunar surface.  This is a key component for simulating terrain variability.
* **`HeightMaps`:** Manages the generation and saving of heightmap data, potentially using different formats or compression techniques.
* **`astar`:** Implements the A* pathfinding algorithm. This module is independent of visualization and focuses purely on path computation.
* **`helper`:** Contains utility functions used across multiple modules.
* **`generator`:** Creates terrain maps from pre-processed data.  This might involve combining heightmap data with other data sources.

The main scripts (`main.py`, `main2.py`) are primarily for frontend integration and can be largely ignored for backend development.


## 🔧 Key Components

For backend developers, the most critical components are:

* **`DataProcessor`:**  Understanding how data is loaded and pre-processed is vital. Pay close attention to the data structures and format used.  Example:
   ```python
   from DataProcessor import DataProcessor
   processor = DataProcessor()
   data = processor.load_data("path/to/lunar_data.hkl")  # Example - Adapt to actual data loading method
   transformed_data = processor.to_cartesian(data)
   ```
* **`astar`:** The A* pathfinding algorithm is a central component.  Understanding its input/output and how to modify the heuristic function for different scenarios is important. Example:
   ```python
   from astar import astar_search
   path = astar_search(start_node, end_node, graph)
   ```
* **`DataProcessorPerlinNoise`:**  The Perlin noise generation allows for creation of realistic terrain.  Understanding the parameters and their effect on the generated heightmaps is crucial.
* **`HeightMaps`:** This module manages the persistence of generated heightmaps. It's crucial for data management and potentially scalability.


## 📦 Dependencies & Tools

Backend developers need to focus on these dependencies: `numpy`, `hickle`, `networkx`, `matplotlib`, `PIL`, `noise`, `seaborn`, `scipy`, `cv2`.  `panda3d` and `ursina` are frontend specific and can be omitted for pure backend work.


## 🛠️ Development Workflow

1. **Focus on individual modules:** Work on one module at a time to understand its functionality.  Write unit tests for each module to ensure correctness.
2. **Use version control (Git):** Commit changes regularly with descriptive commit messages.
3. **Follow a consistent coding style:** Adhere to PEP 8 guidelines for Python code.
4. **Write comprehensive documentation:** Add docstrings to functions and modules to explain their purpose and usage.


## 🧪 Testing & Debugging

1. **Unit testing:** Write unit tests for each module using a testing framework like `pytest`.  This ensures that individual functions and components work as expected.  Example (pytest):
   ```python
   import pytest
   from DataProcessor import DataProcessor

   def test_data_loading():
       processor = DataProcessor()
       data = processor.load_data("path/to/test_data.hkl") # Replace with a test data file
       assert data is not None
   ```
2. **Integration testing:** Test the interaction between different modules.
3. **Logging:** Use the Python `logging` module to track the execution flow and identify errors.
4. **Debugging tools:** Use a debugger (like pdb) to step through the code and identify issues.


## 📚 Additional Resources

* [Python documentation](https://docs.python.org/3/)
* [NumPy documentation](https://numpy.org/doc/)
* [A* search algorithm explanation](https://en.wikipedia.org/wiki/A*_search_algorithm)
* [Perlin noise explanation](https://en.wikipedia.org/wiki/Perlin_noise)


This guide provides a starting point for backend developers working with the NASA_ADC repository. Remember to adapt the steps and examples to your specific needs and the actual structure of the repository.  Always consult the code's comments and docstrings for more detailed information.
