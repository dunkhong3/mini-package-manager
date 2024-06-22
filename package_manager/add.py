import json
import os
import re


def add(input_str: str) -> None:
    # TODO: make this path a variable or read it from a config file
    # or run the program in a container
    current_directory = os.getcwd()
    pkg_json_path = f"{current_directory}/local_packages/package.json"

    # Split the input string into package_name and version
    try:
        package_name, version = input_str.split('@')
    except ValueError:
        print(f"Invalid input format: '{input_str}'. Expected 'package_name@version'.")
        return

    # Validate the correct version format "{num}.{num}.{num}"
    if not re.match(r'^\d+\.\d+\.\d+$', version):
        print(f"Invalid version format: '{version}'. Expected format 'num.num.num'.")
        return
    
    # TODO: make sure the package name and version number does exist in package_repo

    # Load existing package.json if it exists
    try:
        with open(pkg_json_path, 'r') as f:
            package_data = json.load(f)
    # create a package.json if it does not already exist
    except FileNotFoundError:
        package_data = {
            'name': 'test-project',
            'version': '1.0.0',
            "description": "Example project with package dependencies",
            'dependencies': {}
        }

    # Add or update the dependency
    package_data['dependencies'][package_name] = version

    # Write the updated package.json file
    with open(pkg_json_path, 'w') as f:
        json.dump(package_data, f, indent=2)
    
    print(f"Added package '{package_name}' version '{version}' to dependencies.")
    return
