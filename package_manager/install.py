import json
import os
import shutil
import yaml


def install() -> None:
    # TODO: make these paths a variable or read them from a config file
    # or run the program in a container
    current_directory = os.getcwd()
    pkg_json_path = f"{current_directory}/local_packages/package.json"
    node_modules_path = f"{current_directory}/local_packages/node_modules"

    # Load package.json to read dependencies
    try:
        with open(pkg_json_path, 'r') as f:
            package_data = json.load(f)
    except FileNotFoundError:
        print("Error: package.json not found.")
        return

    # Create node_modules folder if it doesn't exist
    if not os.path.exists(node_modules_path):
        os.makedirs(node_modules_path)

    # generate a set of all packages to install
    init_pkg_list = list(set(package_data.get('dependencies', {}).items()))

    # using DFS to generate all packages to install without circular dependencies
    pkg_to_install = dfs_install(init_pkg_list)

    # installing all needed packages
    for pkg_name, version in pkg_to_install:
        install_single_package(pkg_name, version)

    print("All dependencies installed successfully.")


def dfs_install(init_pkgs: list[(str, str)]) -> list[(str, str)]:
    # stack is the set of packages to install
    # visited is the output list of packages to install
    stack = list(set(init_pkgs))
    visited = set(init_pkgs)
    while stack:
        pkg_name, version = stack.pop()
        for dep_pkg_name, dep_pkg_version in find_pkg_dependencies(pkg_name, version):
            if (dep_pkg_name, dep_pkg_version) not in visited:
                stack.append((dep_pkg_name, dep_pkg_version))
                visited.add((dep_pkg_name, dep_pkg_version))
    return list(visited)


# getting all dependencies of a package, ie. all neighbors of a node in the graph
def find_pkg_dependencies(pkg_name: str, version: str) -> list[(str, str)]:
    # TODO: make these paths a variable or read them from a config file
    # or run the program in a container
    current_directory = os.getcwd()
    pkg_registry_path = f"{current_directory}/package_repo/registry/package_{pkg_name.lower()}.yaml"

    # TODO: make sure the package exits in the registry
    try:
        with open(pkg_registry_path, 'r') as file:
            data = yaml.safe_load(file)
    # TODO: better error handling here
    except FileNotFoundError:
        print(f"Error: The file '{pkg_registry_path}' does not exist.")
        return []
    except yaml.YAMLError as e:
        print(f"Error: An error occurred while parsing YAML file: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []
    
    if not data["versions"][version].get('dependencies', []):
        return []

    res = []
    for pkg in data["versions"][version].get('dependencies', []):
        pkg_name, pkg_version = pkg.split('@')
        res.append((pkg_name, pkg_version))
    return res


def install_single_package(pkg_name: str, version: str) -> None:
    # TODO: make these paths a variable or read them from a config file
    # or run program in a container
    current_directory = os.getcwd()
    pkg_repo_path = f"{current_directory}/package_repo/metadata"
    local_pkg_path = f"{current_directory}/local_packages/node_modules"

    # TODO: make sure the package name and version number does exist in package_repo
    pkg_src_file_path = f"{pkg_repo_path}/{pkg_name}/{pkg_name}@{version}_src.txt"
    pkg_dest_folder_path = f"{local_pkg_path}/{pkg_name}"
    pkg_dest_file_path = f"{local_pkg_path}/{pkg_name}/{pkg_name}@{version}_src.txt"

    # Ensure destination folder exists; create if it doesn't
    if not os.path.exists(pkg_dest_folder_path):
        os.makedirs(pkg_dest_folder_path)

    shutil.copyfile(pkg_src_file_path, pkg_dest_file_path)
    print(f"Installed package {pkg_name} version {version} to node_modules")
