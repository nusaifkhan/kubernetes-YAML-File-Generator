import tkinter as tk
from tkinter import messagebox
import yaml
import os

# This script generates Kubernetes YAML files based on user input.
# It provides a GUI for users to select the API version, resource kind,
# and fill in the required fields for the selected resource kind.
# The generated YAML files are saved in an output folder.

# Function to handle Resource Kind selection
def set_kind(*args):
    """Update description and display corresponding fields based on selected kind."""
    # Get the selected kind from the dropdown menu
    kind = kind_var.get()
    description = {
        "Deployment (Manages workloads, replicas, containers)": 
            "Kind: Deployment\nManages workloads with replicas, selectors, and container templates.",
        "Service (Exposes apps, selectors and ports)": 
            "Kind: Service\nExposes applications via selectors and ports.",
        "Ingress (Routes external traffic using rules)":
            "Kind: Ingress\nRoutes external traffic to services using host, path, and rules."
    }
        # Update the description label based on the selected kind
    kind_description_label.config(text=description.get(kind, "Select a valid resource type."))
    
    # Hide all frames then show the chosen one
    frame_deployment.grid_remove()
    frame_service.grid_remove()
    frame_ingress.grid_remove()
    
    # Show the appropriate frame based on the selected kind
    if "Deployment" in kind:
        frame_deployment.grid(row=4, column=0, columnspan=4, padx=10, pady=5)
    elif "Service" in kind:
        frame_service.grid(row=4, column=0, columnspan=4, padx=10, pady=5)
    elif "Ingress" in kind:
        frame_ingress.grid(row=4, column=0, columnspan=4, padx=10, pady=5)

# Function to generate and save the Kubernetes YAML file
def save_yaml():
    """Generate and save YAML based on user input."""
    # Get the selected kind and resource name
    kind = kind_var.get()
    resource_name = entry_resource_name.get()
    # Extract the selected API version
    selected_api_version = api_version_var.get().split(" ")[0]
    # Check if mandatory fields are filled
    if not kind or not resource_name:
        messagebox.showerror("Error", "Resource Kind and Resource Name are required!")
        return None

    # Create the base YAML structure.
    # We extract only the word before " (" in the kind string.
        # Create the base YAML structure with metadata and spec sections
    resource = {
        "apiVersion": selected_api_version,
        "kind": kind.split(" ")[0], # Extract only the kind name (e.g., "Deployment")
        "metadata": {
            "name": resource_name, # Set the resource name
            "labels": {
                "app": resource_name   # Add labels for matching purposes
            }
        },
        "spec": {}  # Spec section starts empty and is populated later
    }
    
    # Populate fields based on the selected kind
    if "Deployment" in kind:
        # Collect Deployment-specific fields
        replicas = entry_replicas.get()
        selector = entry_selector_deployment.get()
        container_name = entry_container_name.get()
        image_name = entry_image_name.get()
        container_port = entry_container_port.get()
        # Check if all fields are filled
        if not replicas or not selector or not container_name or not image_name or not container_port:
            messagebox.showerror("Error", "All Deployment fields are required!")
            return None
        # Populate the spec section for Deployment
        resource["spec"] = {
            "replicas": int(replicas),  # Number of replicas
            "selector": {"matchLabels": {"app": selector}},  # Match labels for the selector
            "template": {
                "metadata": {"labels": {"app": selector}}, # Add labels to template metadata
                "spec": {
                    "containers": [
                        {"name": container_name, # Container name
                         "image": image_name,  # Image name
                         "ports": [{"containerPort": int(container_port)}]}  # Port exposed by the container
                    ]
                }
            }
        }
    elif "Service" in kind:
        # Collect Service-specific fields
        selector = entry_selector_service.get()
        port = entry_service_port.get()
        target_port = entry_service_target_port.get()
        service_type = entry_service_type.get()
        # Check if all fields are filled
        if not selector or not port or not target_port or not service_type:
            messagebox.showerror("Error", "All Service fields are required!")
            return None
        # Populate the spec section for Service
        resource["spec"] = {
            "selector": {"app": selector},  # Match labels for the service
            "ports": [{"protocol": "TCP", "port": int(port), "targetPort": int(target_port)}],  # Ports for the service
            "type": service_type  # Service type (e.g., ClusterIP, NodePort)
        }
    elif "Ingress" in kind:
        # Collect Ingress-specific fields
        host = entry_ingress_host.get()
        path = entry_ingress_path.get()
        ingress_service_name = entry_ingress_service_name.get()
        ingress_service_port = entry_ingress_service_port.get()
        # Check if all fields are filled
        if not host or not path or not ingress_service_name or not ingress_service_port:
            messagebox.showerror("Error", "All Ingress fields are required!")
            return None
        # Populate the spec section for Ingress
        resource["spec"] = {
            "rules": [
                {
                    "host": host,  # Host for the Ingress
                    "http": {
                        "paths": [
                            {
                                "path": path, # Path for routing
                                "pathType": "Prefix", # Path type (e.g., Prefix)
                                "backend": {
                                    "service": {
                                        "name": ingress_service_name,   # Service name
                                        "port": {"number": int(ingress_service_port)}  # Service port
                                    }
                                }
                            }
                        ]
                    }
                }
            ]
        }

    # Save the generated YAML to an output folder.
    output_folder = os.path.join(os.getcwd(), "output")  # Set the output folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Create the folder if it doesn't exist
    file_path = os.path.join(output_folder, f"{resource_name}.yaml") # Define the file path
    with open(file_path, "w") as yaml_file:
        yaml.dump(resource, yaml_file, default_flow_style=False)  # Save the YAML file
    # Notify the user about the successful save
    messagebox.showinfo("Success", f"YAML file saved at {file_path}")
    return file_path

# Function to save the YAML file and exit the program
def exit_program():
    """Save the YAML and then exit the program."""
    saved = save_yaml() # Save the YAML file
    if saved is not None:  # If save is successful, close the application
        root.destroy()

########## GUI SETUP ##########

# Initialize the main Tkinter window
root = tk.Tk()
root.title("Kubernetes YAML Generator") # Set the window title

# API Version Selector (Row 0)
tk.Label(root, text="Select API Version:").grid(row=0, column=0, padx=10, pady=10) # Add label for API version
api_version_var = tk.StringVar()  # Create a StringVar to hold the selected API version
api_version_var.set("apps/v1 (Deployments, StatefulSets, ReplicaSets - Workload management)")  # Set default value
api_version_menu = tk.OptionMenu(
    root, api_version_var,
    "apps/v1 (Deployments, StatefulSets, ReplicaSets - Workload management)",  # Option 1
    "v1 (Pods, Services, ConfigMaps, Secrets - Core communication resources)",  # Option 2
    "networking.k8s.io/v1 (Ingress - Route external traffic to Services)"    # Option 3
)
api_version_menu.grid(row=0, column=1, padx=10, pady=10)  # Place the dropdown menu

# Resource Kind Selector Dropdown (Row 1) with short descriptions
tk.Label(root, text="Select Resource Kind:").grid(row=1, column=0, padx=10, pady=5)  # Add label for Resource Kind
kind_var = tk.StringVar()   # Create a StringVar to hold the selected resource kind
kind_var.set("Deployment (Manages workloads, replicas, containers)")  # Default value
kind_menu = tk.OptionMenu(
    root, kind_var,
    "Deployment (Manages workloads, replicas, containers)",  # Option 1
    "Service (Exposes apps, selectors and ports)",          # Option 2
    "Ingress (Routes external traffic using rules)",       # Option 3
    command=set_kind    # Call set_kind when an option is selected
)
kind_menu.grid(row=1, column=1, padx=10, pady=10)  # Place the dropdown menu

# Kind Description Label (Row 2)
kind_description_label = tk.Label(root, text="", fg="blue", wraplength=400, justify="left")
kind_description_label.grid(row=2, column=0, columnspan=4, padx=10, pady=5)

# Common Resource Name Field (Row 3)
tk.Label(root, text="Resource Name:").grid(row=3, column=0, padx=10, pady=5)
entry_resource_name = tk.Entry(root)
entry_resource_name.grid(row=3, column=1, padx=10, pady=5)

# Predefined Frames for each resource kind:
# Deployment Frame
frame_deployment = tk.Frame(root, borderwidth=1, relief="solid")
tk.Label(frame_deployment, text="Replicas:").grid(row=0, column=0, padx=10, pady=5)
entry_replicas = tk.Entry(frame_deployment)
entry_replicas.grid(row=0, column=1, padx=10, pady=5)
tk.Label(frame_deployment, text="Selector (app):").grid(row=1, column=0, padx=10, pady=5)
entry_selector_deployment = tk.Entry(frame_deployment)
entry_selector_deployment.grid(row=1, column=1, padx=10, pady=5)
tk.Label(frame_deployment, text="Container Name:").grid(row=2, column=0, padx=10, pady=5)
entry_container_name = tk.Entry(frame_deployment)
entry_container_name.grid(row=2, column=1, padx=10, pady=5)
tk.Label(frame_deployment, text="Image Name:").grid(row=3, column=0, padx=10, pady=5)
entry_image_name = tk.Entry(frame_deployment)
entry_image_name.grid(row=3, column=1, padx=10, pady=5)
tk.Label(frame_deployment, text="Container Port:").grid(row=4, column=0, padx=10, pady=5)
entry_container_port = tk.Entry(frame_deployment)
entry_container_port.grid(row=4, column=1, padx=10, pady=5)

# Service Frame
frame_service = tk.Frame(root, borderwidth=1, relief="solid")
tk.Label(frame_service, text="Selector (app):").grid(row=0, column=0, padx=10, pady=5)
entry_selector_service = tk.Entry(frame_service)
entry_selector_service.grid(row=0, column=1, padx=10, pady=5)
tk.Label(frame_service, text="Port:").grid(row=1, column=0, padx=10, pady=5)
entry_service_port = tk.Entry(frame_service)
entry_service_port.grid(row=1, column=1, padx=10, pady=5)
tk.Label(frame_service, text="Target Port:").grid(row=2, column=0, padx=10, pady=5)
entry_service_target_port = tk.Entry(frame_service)
entry_service_target_port.grid(row=2, column=1, padx=10, pady=5)
tk.Label(frame_service, text="Service Type (e.g., ClusterIP):").grid(row=3, column=0, padx=10, pady=5)
entry_service_type = tk.Entry(frame_service)
entry_service_type.grid(row=3, column=1, padx=10, pady=5)

# Ingress Frame
frame_ingress = tk.Frame(root, borderwidth=1, relief="solid")
tk.Label(frame_ingress, text="Host:").grid(row=0, column=0, padx=10, pady=5)
entry_ingress_host = tk.Entry(frame_ingress)
entry_ingress_host.grid(row=0, column=1, padx=10, pady=5)
tk.Label(frame_ingress, text="Path:").grid(row=1, column=0, padx=10, pady=5)
entry_ingress_path = tk.Entry(frame_ingress)
entry_ingress_path.grid(row=1, column=1, padx=10, pady=5)
tk.Label(frame_ingress, text="Service Name:").grid(row=2, column=0, padx=10, pady=5)
entry_ingress_service_name = tk.Entry(frame_ingress)
entry_ingress_service_name.grid(row=2, column=1, padx=10, pady=5)
tk.Label(frame_ingress, text="Service Port:").grid(row=3, column=0, padx=10, pady=5)
entry_ingress_service_port = tk.Entry(frame_ingress)
entry_ingress_service_port.grid(row=3, column=1, padx=10, pady=5)

# Initially hide all kind-specific frames
frame_deployment.grid_remove()
frame_service.grid_remove()
frame_ingress.grid_remove()

# Save YAML Button (Row 5)
tk.Button(root, text="Generate YAML", command=save_yaml).grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Save & Exit Button (Row 5)
tk.Button(root, text="Save & Exit", command=exit_program).grid(row=5, column=2, columnspan=2, padx=10, pady=10)

root.mainloop()
