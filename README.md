# HCMUT_CO3093_ComputerNetworks_Assignment1
# `Peer-to-Peer File-Sharing Application`

## Overview
Build a Simple Like-torrent application with application protocols defined by each group, using the TCP/IP protocol stack.

All descriptions and reports are included in the documentation
## Requirements 
- Python 3
- PostgreSQL installed on the Server machine 
- How to use PostgreSQL in https://www.w3schools.com/postgresql/ and dowload in https://www.postgresql.org/download/
- Install library `psycopg2` to connect in python
```

## SET UP ENV
cd /path/to/your/project
sudo apt update
sudo apt install python3-venv
python3 -m venv env
source env/bin/activate

pip install mysql-connector-python
```
## Installation
Installation from source is straightforward:
```
$ git clone https://github.com/nguyenminhlinh/HCMUT_CO3093_ComputerNetworks_Assignment1.git
$ cd HCMUT_CO3093_ComputerNetworks_Assignment1
```
## Usage
1. Create database with SQL Shell (PostgreSQL) by file server/db.txt 
2. Start the central server:
   - $ cd server
   - Run the `server.py` script to start the central server. Ensure the server is running before proceeding with client actions.

3. Client Setup:
   - $ cd client1
   - $ cd client2
   - Edit the `SERVER_HOST`, `SERVER_PORT`, `CLIENT_PORT` setting in the `client.py` file to configure the IP for the central server. After that run the `client.py` script to start the client and connect to the central server.

## Features

1. The client has a simple command-shell interpreter that is used to accept two kinds of commands.
    - `publish file_name`: A set of local files on the client machine is divided into parts (size of each part is 512kb). Users can select pieces shared content to send information to the server.
    
    - `fetch file_name`: The server sends information about parts of files shared by peers that are not yet available to clients. Clients can choose any part to download. Once all parts are downloaded, they will be merged into one original file.

## Example
### Client1 publish Data.pdf on Server
#### Server side

```
\server> python server.py
2024-04-25 15:51:31,649 - INFO - Server started and is listening for connections.
Server command: 2024-04-25 15:51:35,938 - INFO - Active connections: 2
2024-04-25 15:51:35,938 - INFO - Connection established with linh/192.168.56.1:65433)
2024-04-25 15:51:41,464 - INFO - Active connections: 3
2024-04-25 15:51:41,472 - INFO - Connection established with linh/192.168.56.1:65434)
2024-04-25 15:52:03,987 - INFO - Updating client info in database for hostname: linh/192.168.56.1:65433
2024-04-25 15:52:03,992 - INFO - Database update complete for hostname: linh/192.168.56.1:65433
```

#### Client side

```
\client1> python client.py
Enter command (publish file_name/ fetch file_name/ exit): publish Data.pdf
File Data.pdf have ['Data.pdf_piece1', 'Data.pdf_piece2', 'Data.pdf_piece3', 'Data.pdf_piece4', 'Data.pdf_piece5']
 piece: ["b'\\xe1\\xd8\\\\r\\xa2\\t\\xee\\x0c\\xfd91\\x12\\xedkk\\xf1u\\x03\\x9b\\x14'", 'b"f\\xc3\\xc1o8\\xd7\\xb0Ft\\xc5\\xf1\\x1e`7-\'\\xa8!\\x1f\\x96"', "b'cT\\xdf\\xc3~\\xf1dO\\x135\\x1d\\x0eu\\x95\\xd3\\xfb\\xd9*\\n\\x9a'", 'b\'\\x0f\\xda\\xb7\\xda\\xda3\\x90Rr\\x88\\xc4\\xc0\\x85"\\xfe]\\x0fN\\xf98\'', "b'\\tA\\xb9I\\x17\\xa0\\xa7\\xcf\\xea\\xa1!\\x97\\xd6C-44\\xa7\\xd9\\xb6'"].
Please select num piece in file to publish:1 3 4
You was selected: 
Number 1 : b'\xe1\xd8\\r\xa2\t\xee\x0c\xfd91\x12\xedkk\xf1u\x03\x9b\x14'
Number 3 : b'cT\xdf\xc3~\xf1dO\x135\x1d\x0eu\x95\xd3\xfb\xd9*\n\x9a'
Number 4 : b'\x0f\xda\xb7\xda\xda3\x90Rr\x88\xc4\xc0\x85"\xfe]\x0fN\xf98'
File list updated successfully.
Enter command (publish file_name/ fetch file_name/ exit): 
```

### Client2 fetch Data.pdf 
#### Server side

```
\server> python server.py
2024-04-25 15:51:31,649 - INFO - Server started and is listening for connections.
Server command: 2024-04-25 15:51:35,938 - INFO - Active connections: 2
2024-04-25 15:51:35,938 - INFO - Connection established with linh/192.168.56.1:65433)
2024-04-25 15:51:41,464 - INFO - Active connections: 3
2024-04-25 15:51:41,472 - INFO - Connection established with linh/192.168.56.1:65434)
2024-04-25 15:52:03,987 - INFO - Updating client info in database for hostname: linh/192.168.56.1:65433
2024-04-25 15:52:03,992 - INFO - Database update complete for hostname: linh/192.168.56.1:65433
```

#### Client side

```
client2> python client.py
Enter command (publish file_name/ fetch file_name/ exit):fetch Data.pdf
Hosts with the file Data.pdf:
Number: 1 linh/192.168.56.1:65433 piece_hash: b'\xe1\xd8\\r\xa2\t\xee\x0c\xfd91\x12\xedkk\xf1u\x03\x9b\x14' file_size: 2296627 piece_size: 524288 num_order_in_file: 1
Number: 3 linh/192.168.56.1:65433 piece_hash: b'cT\xdf\xc3~\xf1dO\x135\x1d\x0eu\x95\xd3\xfb\xd9*\n\x9a' file_size: 2296627 piece_size: 524288 num_order_in_file: 3
Number: 4 linh/192.168.56.1:65433 piece_hash: b'\x0f\xda\xb7\xda\xda3\x90Rr\x88\xc4\xc0\x85"\xfe]\x0fN\xf98' file_size: 2296627 piece_size: 524288 num_order_in_file: 4
```
arrow
psycopg2



1
