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
        # Create a list to store the name and ports of the containers
        containers = {
        }

        # Store the name of the container
        container_name = ''
        index = 0

        # Loop through each line in the file
        while index < len(lines):
            line = lines[index]
            # If the line contains the name of the container
            if 'container_name' in line:
                # Split the line by the colon
                splitLine = line.split(':')
                # Add the name of the container to the map
                containers[splitLine[1].strip()] = {}
                container_name = splitLine[1].strip()
                # print('Found container: ' + container_name +
                # ' line: ' + str(lines.index(line)))
            # If the line contains the ports of the container
            if 'ports' in line:
                # Move to the next line
                line = lines[index + 1]
                index += 1

                # Create a list to store the ports
                ports = []

                # Loop through the next lines if the next line contains a port
                while check_port(line) != -1:
                    # print(container_name + ' ' +
                    # check_port(line) + ' ' + str(lines.index(line)))
                    # Add the port to the list of ports
                    ports.append(check_port(line))
                    # Read the next line
                    line = lines[index + 1]
                    index += 1

                # Add the list of ports to the map
                containers[container_name]['ports'] = ports
            index += 1

    # Return the list of name and ports of the containers
    return containers


# This function will write the name and ports of the containers to the ports.md file
def write_ports_file(stacks):
    # Open the ports.md file
    with open('ports.md', 'w') as f:
        for stack in stacks:
            for container in stacks[stack]:
                # Check if container has ports
                if 'ports' in stacks[stack][container]:
                    # Write the name of the container and the ports to the ports.md file
                    f.write('## ' + container + '\n')
                    for port in stacks[stack][container]['ports']:
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
