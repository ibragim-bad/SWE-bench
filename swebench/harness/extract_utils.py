import os
import re
import yaml
import toml
from typing import List, Dict
from collections import defaultdict


INSTALL_COMMANDS = {
    "requirements.txt": "pip install -r requirements.txt",
    "environment.yml": "conda env create -f environment.yml",
    "setup.py": "pip install -e .",  # or "python setup.py install"
    "pyproject.toml": "poetry install",
    "Pipfile": "pipenv install",
    "tox.ini": "tox",
    "conda-requirements.txt": "conda install --file conda-requirements.txt",
    "requirements.in": "pip-compile && pip-sync"
}

def find_files(directory: str, filenames: List[str]) -> Dict[str, List[str]]:
    """
    Find specific files in the given directory and its subdirectories.
    
    Args:
        directory (str): The directory to search in.
        filenames (list[str]): A list of filenames to search for.
    
    Returns:
        dict[str, list[str]]: A dict of paths to the found files.
    """
    found_files = defaultdict(list)
    for root, _, files in os.walk(directory):
        for file in files:
            cur_file = os.path.relpath(os.path.join(root, file), directory)
            if file in filenames:
                found_files[file].append(cur_file)
            elif file.startswith("requirements"):
                found_files["requirements.txt"].append(cur_file)
    return found_files

def parse_requirements_txt(filepath: str) -> List[str]:
    """
    Parse a requirements.txt file to extract package information.
    
    Args:
        filepath (str): The path to the requirements.txt file.
    
    Returns:
        List[str]: A list of packages with their versions.
    """
    packages = []
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                line = line.split(';')[0]
                packages.append(line)
    return packages

def parse_environment_yml(filepath: str) -> List[str]:
    """
    Parse an environment.yml file to extract package information.
    
    Args:
        filepath (str): The path to the environment.yml file.
    
    Returns:
        List[str]: A list of packages with their versions.
    """
    packages = []
    with open(filepath, 'r') as file:
        env = yaml.safe_load(file)
        dependencies = env.get('dependencies', [])
        for dep in dependencies:
            if isinstance(dep, str):
                packages.append(dep)
            elif isinstance(dep, dict) and 'pip' in dep:
                packages.extend(dep['pip'])
    return packages

def parse_setup_py(filepath: str) -> List[str]:
    """
    Parse a setup.py file to extract package information.
    
    Args:
        filepath (str): The path to the setup.py file.
    
    Returns:
        List[str]: A list of packages with their versions.
    """
    packages = []
    with open(filepath, 'r') as file:
        content = file.read()
        install_requires_match = re.search(r'install_requires\s*=\s*\[(.*?)\]', content, re.DOTALL)
        if install_requires_match:
            requires = install_requires_match.group(1)
            packages = [req.strip().strip('"').strip("'") for req in requires.split(',')]
       # Extract testing extras_require
        extras_require_match = re.search(r'extras_require\s*=\s*{.*?["\']testing["\']\s*:\s*\[(.*?)\]', content, re.DOTALL)
        if extras_require_match:
            testing_requires = extras_require_match.group(1)
            packages.extend([req.strip().strip('"').strip("'") for req in testing_requires.split(',')])
    
    return packages

def parse_pyproject_toml(filepath: str) -> List[str]:
    """
    Parse a pyproject.toml file to extract package information.
    
    Args:
        filepath (str): The path to the pyproject.toml file.
    
    Returns:
        List[str]: A list of packages with their versions.
    """
    packages = []
    with open(filepath, 'r') as file:
        pyproject = toml.load(file)
        dependencies = pyproject.get('tool', {}).get('poetry', {}).get('dependencies', {})
        dev_dependencies = pyproject.get('tool', {}).get('poetry', {}).get('dev-dependencies', {})
        
        for dep, version in dependencies.items():
            if isinstance(version, str):
                packages.append(f"{dep}=={version}")
            elif isinstance(version, dict) and 'version' in version:
                packages.append(f"{dep}=={version['version']}")
            else:
                packages.append(dep)
        
        for dep, version in dev_dependencies.items():
            if isinstance(version, str):
                packages.append(f"{dep}=={version}")
            elif isinstance(version, dict) and 'version' in version:
                packages.append(f"{dep}=={version['version']}")
            else:
                packages.append(dep)
    packages = [p.replace("==^", ">=") for p in packages if not p.startswith("python==")]
    return packages

def is_valid_package_name(package: str) -> bool:
    """
    Determine if a package name is valid.
    
    Args:
        package (str): The package name to validate.
    
    Returns:
        bool: True if the package name is valid, False otherwise.
    """
    # Regular expression to match valid package names
    valid_package_regex = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_.-]*\s*(?:[=<>!~]=.*)?$')
    return bool(valid_package_regex.match(package))

def get_required_packages(directory: str) -> List[str]:
    """
    Get a list of required packages with their versions from the given directory.
    
    Args:
        directory (str): The directory to search in.
    
    Returns:
        List[str]: A list of packages with their versions.
    """
    files_to_check = ['requirements.txt', 'environment.yml', 'setup.py', 'pyproject.toml']
    found_files = find_files(directory, files_to_check)
    
    all_packages = []
    for filepath in found_files:
        file = os.path.basename(filepath)
        if file.startswith('requirements') and 'docs' not in filepath:
            all_packages.extend(parse_requirements_txt(filepath))
        elif file == 'environment.yml':
            all_packages.extend(parse_environment_yml(filepath))
        elif file == 'setup.py':
            all_packages.extend(parse_setup_py(filepath))
        elif file == 'pyproject.toml':
            all_packages.extend(parse_pyproject_toml(filepath))
    # Remove duplicates while preserving order
    seen = set()
    unique_packages = []
    for pkg in all_packages:
        if pkg not in seen and is_valid_package_name(pkg):
            unique_packages.append(pkg.split("#")[0].replace(" ", ""))
            seen.add(pkg)
    
    return unique_packages

def get_required_packages_file(directory: str) -> Dict[str, list]:
    """
    Get a list of required packages with their versions from the given directory.
    
    Args:
        directory (str): The directory to search in.
    
    Returns:
        List[str]: A list of packages with their versions.
    """
    files_to_check = ['requirements.txt', 'environment.yml', 'setup.py', 'pyproject.toml', 'tox.ini']
    found_files = find_files(directory, files_to_check)


    return found_files



import os
import re
import toml
import yaml

def extract_python_version_from_travis_yml(file_path):
    with open(file_path, 'r') as file:
        travis_yml = yaml.safe_load(file)
        python_versions = travis_yml.get('python')
        if isinstance(python_versions, list):
            return [str(version) for version in python_versions]
        elif isinstance(python_versions, str):
            return [python_versions]
        return []


def get_all_markdown_files(directory):
    markdown_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    return markdown_files

def extract_versions_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Regular expression to find versions in the format like 3.9, 3.6, etc.
    pattern = r'\b(\d+\.\d+(\.\d+)?)\b'
    matches = re.findall(pattern, content)
    return [match[0] for match in matches]

def is_possible_python_version(version):
    major, minor, *patch = version.split('.')
    if int(major) == 3 and 6 <= int(minor) <= 12:  # Basic check for Python 3.x.x versions
        return True
    return False

def extract_python_version_from_setup_py(file_path):
    extracted = []
    with open(file_path, 'r') as file:
        content = file.read()
    
    python_requires_match = re.search(r'python_requires\s*=\s*[\'"](.+?)[\'"]', content)
    if python_requires_match:
        version_spec = python_requires_match.group(1)
        versions = re.findall(r'\b(\d+\.\d+(\.\d+)?)\b', version_spec)
        extracted += [match[0] for match in versions]
    
    pattern = r'Programming Language :: Python :: (\d+\.\d+)'
    matches = re.findall(pattern, content)
    extracted += [match for match in matches]

    return extracted

def extract_python_version_from_pyproject_toml(file_path):
    with open(file_path, 'r') as file:
        pyproject = toml.load(file)
        requires = pyproject.get('tool', {}).get('poetry', {}).get('dependencies', {}).get('python')
        if requires:
            versions = re.findall(r'\b(\d+\.\d+(\.\d+)?)\b', requires)
            return [match[0] for match in versions]
    
    return []

def get_max_python_version(versions):
    def is_valid_python_version(version):
        parts = version.split('.')
        if len(parts) < 2 or len(parts) > 3:
            return False
        try:
            major, minor = int(parts[0]), int(parts[1])
            if not (3, 5) <= (major, minor) <= (3, 12):
                return False
            if len(parts) == 3:
                patch = int(parts[2])
            return True
        except ValueError:
            return False
    
    # Filter out invalid version strings
    valid_versions = [v for v in versions if is_valid_python_version(v)]
    
    if valid_versions:
        # Find the maximum version from the valid versions
        max_version_tuple = max((tuple(map(int, v.split('.'))) for v in valid_versions))
        return '.'.join(map(str, max_version_tuple))
    
    return None


def get_python_version_from_directory(directory):
    markdown_files = get_all_markdown_files(directory)
    possible_versions = []
    
    for file_path in markdown_files:
        versions = extract_versions_from_file(file_path)
        for version in versions:
            possible_versions.append(version)
    
    setup_py_path = os.path.join(directory, 'setup.py')
    if os.path.exists(setup_py_path):
        versions = extract_python_version_from_setup_py(setup_py_path)
        for version in versions:
            possible_versions.append(version)

    travis_yml_path = os.path.join(directory, '.travis.yml')
    if os.path.exists(travis_yml_path):
        versions = extract_python_version_from_travis_yml(travis_yml_path)
        for version in versions:
            possible_versions.append(version)
    
    pyproject_toml_path = os.path.join(directory, 'pyproject.toml')
    if os.path.exists(pyproject_toml_path):
        versions = extract_python_version_from_pyproject_toml(pyproject_toml_path)
        for version in versions:
            possible_versions.append(version)
    
    
    version = get_max_python_version(possible_versions)
    return version if version else None

def get_repo_version_candidate(repo_path):
    cand = None
    
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file == '.travis.yml':
                with open(os.path.join(root, file), 'r') as f:
                    try:
                        travis_data = yaml.safe_load(f)
                        if 'version' in travis_data:
                            cand = travis_data['version']
                    except yaml.YAMLError:
                        pass
            
            elif file.lower() in ['version', '.version']:
                with open(os.path.join(root, file), 'r') as f:
                    cand = f.read().strip()
            
            elif os.path.basename(file) in ['version.py', '__init__.py', '__version__.py', '__pkginfo__.py']:
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    version_match = re.search(r'(__version__|VERSION)\s*=\s*["\']?([\d\w.]+)["\']?', content)
                    if version_match:
                        cand = version_match.group(2)
            
            elif file == 'pyproject.toml':
                with open(os.path.join(root, file), 'r') as f:
                    try:
                        toml_data = toml.load(f)
                        if 'tool' in toml_data and 'poetry' in toml_data['tool'] and 'version' in toml_data['tool']['poetry']:
                            cand = toml_data['tool']['poetry']['version']
                        elif 'project' in toml_data and 'version' in toml_data['project']:
                            cand = toml_data['project']['version']
                    except toml.TomlDecodeError:
                        pass
            
            elif file == 'setup.py':
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    version_match = re.search(r'version\s*=\s*["\']([\d.]+)["\']', content)
                    if version_match:
                        cand = version_match.group(1)
    
    return cand


def get_repo_version(repo_path, default=-1):
    cand = get_repo_version_candidate(repo_path)
    if cand:
        pattern = r'\b(\d+\.\d+)\b'
        matches = re.findall(pattern, cand)
        if matches:
            cand = matches[0]
        else:
            cand = None
    return cand if cand else default