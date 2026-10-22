## Getting Started

To run this project, a virtual environment is required to isolate the dependencies.

### 1. Create the virtual environment
Open your terminal and run the following command to create the `.venv` folder:
```bash
python -m venv .venv
```

### 2. Activate the virtual environment
Activate the environment depending on your operating system or terminal choice:

* **Windows (Command Prompt - CMD):**
  ```cmd
  .venv\Scripts\activate
  ```
* **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
* **Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```

### 3. Install required libraries
Once the environment is activated, install all the project dependencies by running:
```bash
pip install -r requirements.txt
```
