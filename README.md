# Kubernetes YAML Generator

A graphical user interface (GUI) tool for generating Kubernetes YAML files based on user input. This project simplifies the process of creating Kubernetes configuration files for **Deployment**, **Service**, and **Ingress** resources.

---

## ✨ Features

- Generate Kubernetes YAML files interactively via a GUI.
- Supports resource types:
  - **Deployment**: Manage workloads with replicas and containers.
  - **Service**: Expose applications with selectors and ports.
  - **Ingress**: Route external traffic using rules.
- Automatically saves the YAML files into an `output` folder.

---

## 🔧 Prerequisites

- Python 3.7 or higher  
- `pip` (Python package installer)  
- A working internet connection for installing dependencies

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/kubernetes-YAML-File-Generator.git
cd kubernetes-YAML-File-Generator

```
### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python main.py
```

### 4. Generate YAML Files

- Open the GUI and select **API version** and **Resource Kind** from the dropdown menus.  
- Fill out the required fields based on your selected resource kind.  
- Click **Generate YAML** to save your configuration.  
- The YAML file will be automatically saved in the `output` folder.

---

## 📁 Project Structure

```plaintext
kubernetes-YAML-File-Generator/
├── main.py                 # Main application script
├── requirements.txt        # Python dependencies
├── output/                 # Folder where generated YAML files are saved
└── README.md               # Project documentation
```

---

## 📦 requirements.txt

Install with:

```bash
pip install -r requirements.txt
```

**Dependencies:**

```
PyYAML==6.0
tk
```

---

## 🤝 Contributing

1. **Fork** this repository to your GitHub account.  
2. **Clone** your fork:

    ```bash
    git clone https://github.com/<your-username>/kubernetes-YAML-File-Generator.git
    ```

3. **Create a new branch**:

    ```bash
    git checkout -b feature-or-fix-name
    ```

4. **Make changes and push**:

    ```bash
    git add .
    git commit -m "Add feature or fix"
    git push origin feature-or-fix-name
    ```

5. **Submit a Pull Request** on GitHub.

---

## 🪪 License

This project is licensed under the **MIT License**.

---

## 📬 Contact

**Author:** Nusaif Khan  
**GitHub Issues:** [Submit here](https://github.com/<your-username>/kubernetes-YAML-File-Generator/issues)
```


