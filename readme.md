# PortMapper

Simple port mapping utility, written in python.

## Usage

Move the `portmapper.py` file to the directory where your stacks folders are located and run it using:

```bash
python3 portmapper.py
```

This will create a `ports.md` file next to the script file.



File tree example:

```
project
│
└───stack1
|   │   docker-compose.yml
│
└───stack2
|   │   docker-compose.yml
|
└───stack3
|   │   docker-compose.yml
|
|   portmapper.py
|   ports.md
```



The script will skip the stacks with no ports.



## Note

This script assumes all of the containers in the stack have `container_name` field before the `ports` field.
