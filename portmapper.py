# This script will scan through all subdirectories and find all the files that are named docker-compose.yml
# It will then read the file and look for the name and ports of the containers
# It will then create a file called ports.md in the same directory where script is run
# It will then write the name and ports of the containers to the ports.md file

import os
import re

# This function will check if the line is in number:number format, and then return the number


def check_port(line):
    port = re.search(r'\d+:\d+', line)
    # Check line if its in a 'number:number #tstring' format
    if port:
        # Return the first number
        return port.group(0).split(':')[0]
    else:
        return -1
# This function will read the docker-compose.yml file and find the name and ports of the containers


def read_docker_compose_file(file):
    # Open the docker-compose.yml file
    with open(file, 'r') as f:
        # Read the file
        lines = f.readlines()
        # Create a dict to store the name and ports of the containers
        containers = {}

        # Store the current service name being processed
        current_service = None
        # Track indentation level to know when we're inside a service
        in_services = False
        service_indent = 0
        
        index = 0

        # Loop through each line in the file
        while index < len(lines):
            line = lines[index]
            stripped_line = line.lstrip()
            current_indent = len(line) - len(stripped_line)
            
            # Check if we're in the services section
            if stripped_line.startswith('services:'):
                in_services = True
                service_indent = current_indent
                index += 1
                continue
            
            # If we're in services section, identify service names
            if in_services and current_indent == service_indent + 2 and stripped_line and not stripped_line.startswith('-') and ':' in stripped_line:
                # This is a service definition (e.g., "web:", "database:")
                service_name = stripped_line.split(':')[0].strip()
                # Only consider this a service if it's not a known property
                if service_name not in ['image', 'ports', 'container_name', 'environment', 'volumes', 'networks', 'depends_on', 'restart', 'command', 'version']:
                    current_service = service_name
                    if current_service not in containers:
                        containers[current_service] = {}
            
            # If we have a current service, look for container_name or ports
            if current_service:
                # Check for container_name
                if 'container_name:' in stripped_line:
                    splitLine = stripped_line.split(':', 1)
                    if len(splitLine) > 1:
                        container_name = splitLine[1].strip()
                        # Remove surrounding quotes if present
                        if (container_name.startswith('"') and container_name.endswith('"')) or \
                           (container_name.startswith("'") and container_name.endswith("'")):
                            container_name = container_name[1:-1]
                        containers[current_service]['container_name'] = container_name
                
                # Check for ports
                if stripped_line.startswith('ports:'):
                    # Move to the next line to read port values
                    index += 1
                    if index >= len(lines):
                        break
                    
                    # Create a list to store the ports
                    ports = []
                    
                    # Loop through the next lines if the next line contains a port
                    while index < len(lines):
                        line = lines[index]
                        port_value = check_port(line)
                        if port_value != -1:
                            ports.append(port_value)
                            index += 1
                        else:
                            # No more ports, exit the loop
                            break
                    
                    # Add the list of ports to the service
                    containers[current_service]['ports'] = ports
                    # Continue from current index (already incremented in loop)
                    continue
            
            index += 1

    # Return the dict with service data
    return containers


# This function will write the name and ports of the containers to the ports.md file
def write_ports_file(stacks):
    # Open the ports.md file
    with open('ports.md', 'w') as f:
        for stack in stacks:
            for service_name in stacks[stack]:
                service = stacks[stack][service_name]
                # Check if service has ports
                if 'ports' in service:
                    # Use container_name if available, otherwise use service name
                    display_name = service.get('container_name', service_name)
                    # Write the name and the ports to the ports.md file
                    f.write('## ' + display_name + '\n')
                    for port in service['ports']:
                        f.write(' - ' + port + '\n')
                    f.write('\n')


# This function will find all the docker-compose.yml files in the subdirectories


def find_docker_compose_files():
    # Create a list to store the docker-compose.yml files
    files = []
    # Loop through each directory in the current directory
    for directory in os.listdir():
        # If the directory is a subdirectory
        if os.path.isdir(directory):
            # Loop through each file in the subdirectory
            for file in os.listdir(directory):
                # If the file is named docker-compose.yml
                if file == 'docker-compose.yml':
                    # Add the file to the list
                    files.append(directory + '/' + file)
    # Return the list of docker-compose.yml files
    return files

# This function will run the other functions


def main():
    print('Finding docker-compose.yml files...')
    # Create a list to store the name and ports of the containers
    containers = {}
    # Find all the docker-compose.yml files in the subdirectories
    files = find_docker_compose_files()
    # Loop through each docker-compose.yml file
    index = 0
    for file in files:
        # Read the file and find the name and ports of the containers
        containers[index] = read_docker_compose_file(file)
        index += 1
    # Write the name and ports of the containers to the ports.md file
    write_ports_file(containers)
    print('Done')


# Run the main function
main()
