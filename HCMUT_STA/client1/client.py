import socket
import json
import os
import threading
import shlex
import hashlib

stop_event = threading.Event()

def calculate_piece_hash(piece_data):
    sha1 = hashlib.sha1()
    sha1.update(piece_data)
    return sha1.digest()

def create_pieces_string(pieces):
    hash_pieces = []
    for piece_file_path in pieces:
            with open(piece_file_path, "rb") as piece_file:
                piece_data = piece_file.read()
                piece_hash = calculate_piece_hash(piece_data)
                hash_pieces.append(f"{piece_hash}")
    return hash_pieces

def split_file_into_pieces(file_path, piece_length):
    pieces = []
    with open(file_path, "rb") as file:
        counter = 1
        while True:
            piece_data = file.read(piece_length)
            if not piece_data:
                break
            piece_file_path = f"{file_path}_piece{counter}"
            # piece_file_path = os.path.join("", f"{file_path}_piece{counter}")
            with open(piece_file_path, "wb") as piece_file:
                piece_file.write(piece_data)
            pieces.append(piece_file_path)
            counter += 1
    return pieces

def merge_pieces_into_file(pieces, output_file_path):
    with open(output_file_path, "wb") as output_file:
        for piece_file_path in pieces:
            with open(piece_file_path, "rb") as piece_file:
                piece_data = piece_file.read()
                output_file.write(piece_data)

def get_list_local_files(directory='.'):
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        return True
    except Exception as e:
        return f"Error: Unable to list files - {e}"
    
def check_local_files(file_name):
    if not os.path.exists(file_name):
        return False
    else:
        return True
    
def check_local_piece_files(file_name):
    exist_files = []
    directory = os.getcwd()  # Lấy đường dẫn thư mục hiện tại

    for filename in os.listdir(directory):
        if filename.startswith(file_name) and len(filename)>len(file_name):
            exist_files.append(filename)

    if len(exist_files) > 0:
        return exist_files
    else:
        return False

def handle_publish_piece(sock, peers_port, pieces, file_name,file_size,piece_size):
    pieces_hash = create_pieces_string(pieces)
    user_input_num_piece = input( f"File {file_name} have {pieces}\n piece: {pieces_hash}. \nPlease select num piece in file to publish:" )
    num_order_in_file = shlex.split(user_input_num_piece) 
    piece_hash=[]
    print("You was selected: " )
    for i in num_order_in_file:
        index = pieces.index(f"{file_name}_piece{i}")
        piece_hash.append(pieces_hash[index])
        print (f"Number {i} : {pieces_hash[index]}")
    publish_piece_file(sock,peers_port,file_name,file_size, piece_hash,piece_size,num_order_in_file)

def publish_piece_file(sock,peers_port,file_name,file_size, piece_hash,piece_size,num_order_in_file):
    peers_hostname = socket.gethostname()
    command = {
        "action": "publish",
        "peers_port": peers_port,
        "peers_hostname":peers_hostname,
        "file_name":file_name,
        "file_size":file_size,
        "piece_hash":piece_hash,
        "piece_size":piece_size,
        "num_order_in_file":num_order_in_file,
    }
    # shared_piece_files_dir.append(command)
    sock.sendall(json.dumps(command).encode() + b'\n')
    response = sock.recv(4096).decode()
    print(response)

def request_file_from_peer(peers_ip, peer_port, file_name, piece_hash, num_order_in_file):
    peer_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        try:
            peer_port = int(peer_port)  # Đảm bảo peer_port là một số nguyên
        except ValueError:
            print(f"Invalid port: {peer_port} cannot be converted to an integer.")

        peer_sock.connect((peers_ip, int(peer_port)))
        peer_sock.sendall(json.dumps({'action': 'send_file', 'file_name': file_name, 'piece_hash':piece_hash, 'num_order_in_file':num_order_in_file}).encode() + b'\n')

        # Peer will send the file in chunks of 4096 bytes
        with open(f"{file_name}_piece{num_order_in_file}", 'wb') as f:
            while True:
                data = peer_sock.recv(4096)
                if not data:
                    break
                f.write(data)

        peer_sock.close()
        print(f"Piece of file: {file_name}_piece{num_order_in_file} has been fetched from peer.")
    except Exception as e:
        print(f"An error occurred while connecting to peer at {peers_ip}:{peer_port} - {e}")
    finally:
        peer_sock.close()

def fetch_file(sock,peers_port,file_name, piece_hash, num_order_in_file):
    peers_hostname = socket.gethostname()
    command = {
        "action": "fetch",
        "peers_port": peers_port,
        "peers_hostname":peers_hostname,
        "file_name":file_name,
        "piece_hash":piece_hash,
        "num_order_in_file":num_order_in_file,
    } 
    # command = {"action": "fetch", "fname": fname}
    sock.sendall(json.dumps(command).encode() + b'\n')
    response = json.loads(sock.recv(4096).decode())
    if 'peers_info' in response:
        peers_info = response['peers_info']
        host_info_str = "\n".join([f"Number: {peer_info['num_order_in_file'] } {peer_info['peers_hostname']}/{peer_info['peers_ip']}:{peer_info['peers_port']} piece_hash: {peer_info['piece_hash']  } num_order_in_file: {peer_info['num_order_in_file'] }" for peer_info in peers_info])
        print(f"Hosts with the file {file_name}:\n{host_info_str}")
        if len(peers_info) >= 1:
            chosen_info = input("Enter the number of the host to download from: ")
            chosen_info_part = shlex.split(chosen_info) 
            # Find the host entry with the chosen IP to get the corresponding lname
            for i in chosen_info_part:
                index = next((j for j, peer_info in enumerate(peers_info) if peer_info.get('num_order_in_file') == i), None)
                if index is not None:
                    request_file_from_peer(peers_info[index]['peers_ip'], peers_info[index]['peers_port'], peers_info[index]['file_name'],peers_info[index]['piece_hash'],peers_info[index]['num_order_in_file'])
                else:
                     print(f"Invalid number entered: {i}")
            if(peers_info['file_size']/peers_info['file_size']==len( sorted(pieces := check_local_piece_files(file_name)))):
                merge_pieces_into_file(pieces,file_name)
        else:
            print("No hosts have the file.")
    else:
        print("No peers have the file or the response format is incorrect.")

def send_piece_to_client(conn, piece):
    with open(piece, 'rb') as f:
        while True:
            bytes_read = f.read(4096)
            if not bytes_read:
                break
            conn.sendall(bytes_read)

def handle_file_request(conn, shared_files_dir):
    try:
        data = conn.recv(4096).decode()
        command = json.loads(data)
        if command['action'] == 'send_file':
            file_name = command['file_name']
            num_order_in_file = command['num_order_in_file']
            file_path = os.path.join(shared_files_dir, f"{file_name}_piece{num_order_in_file}")
            send_piece_to_client(conn, file_path)
    finally:
        conn.close()

def start_host_service(port, shared_files_dir):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('0.0.0.0', port))
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.listen()

    while not stop_event.is_set():
        try:
            server_sock.settimeout(1) 
            conn, addr = server_sock.accept()
            thread = threading.Thread(target=handle_file_request, args=(conn, shared_files_dir))
            thread.start()
        except socket.timeout:
            continue
        except Exception as e:
            break

    server_sock.close()

def connect_to_server(server_host, server_port, peers_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_host, server_port))
    peers_hostname = socket.gethostname()
    sock.sendall(json.dumps({'action': 'introduce', 'peers_hostname': peers_hostname, 'peers_port':peers_port }).encode() + b'\n')
    return sock

def main(server_host, server_port, peers_port):
    host_service_thread = threading.Thread(target=start_host_service, args=(peers_port, './'))
    host_service_thread.start()

    # Connect to the server
    sock = connect_to_server(server_host, server_port,peers_port)

    try:
        while True:
            user_input = input("Enter command (publish file_name/ fetch file_name/ exit): ")#addr[0],peers_port, peers_hostname,file_name, piece_hash,num_order_in_file
            command_parts = shlex.split(user_input)
            if len(command_parts) == 2 and command_parts[0].lower() == 'publish':
                _,file_name = command_parts
                if check_local_files(file_name):
                    piece_size = 524288  # 524288 byte = 512KB
                    file_size = os.path.getsize(file_name)
                    pieces = split_file_into_pieces(file_name,piece_size)
                    handle_publish_piece(sock, peers_port, pieces, file_name,file_size,piece_size)
                elif (pieces := check_local_piece_files(file_name)):
                    handle_publish_piece(sock, peers_port, pieces, file_name,file_size,piece_size)
                else:
                    print(f"Local file {file_name}/piece does not exist.")
            elif len(command_parts) == 2 and command_parts[0].lower() == 'fetch':
                _, file_name = command_parts
                pieces = check_local_piece_files(file_name)
                pieces_hash = [] if not pieces else create_pieces_string(pieces)
                num_order_in_file= [] if not pieces else [item.split("_")[-1][5:] for item in pieces]
                fetch_file(sock,peers_port,file_name, pieces_hash,num_order_in_file)
            elif user_input.lower() == 'exit':
                stop_event.set()  # Stop the host service thread
                sock.close()
                break
            else:
                print("Invalid command.")

    finally:
            sock.close()
            host_service_thread.join()


if __name__ == "__main__":
    # Replace with your server's IP address and port number
    SERVER_HOST = '172.20.10.4'
    SERVER_PORT = 65432
    CLIENT_PORT = 65433
    main(SERVER_HOST, SERVER_PORT,CLIENT_PORT)
