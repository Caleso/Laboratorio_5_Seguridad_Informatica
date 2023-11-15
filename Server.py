#LABORATORIO_3
#NOMBRES: CATALINA LEDESMA

import socket
import pyDes

# Encripta DES
def encrypt_des(key, data):
    des = pyDes.des(key, pyDes.CBC, b'\0\0\0\0\0\0\0\0', pad=None, padmode=pyDes.PAD_PKCS5)
    ciphertext = des.encrypt(data)
    return ciphertext

# Desencripta DES
def decrypt_des(key, ciphertext):
    des = pyDes.des(key, pyDes.CBC, b'\0\0\0\0\0\0\0\0', pad=None, padmode=pyDes.PAD_PKCS5)
    data = des.decrypt(ciphertext)
    return data

def main():
    with open('mensajeentrada.txt', 'rb') as file:
        mensaje_original = file.read()

    # Diffie-Hellman
    valor_p = 173
    valor_q = 50
    valor_a = int(input("Ingrese valor A secreto: "))
    valor_ax = str((valor_q ** valor_a) % valor_p)

    # Conexion
    host = "localhost"
    puerto = 8000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, puerto))
    server_socket.listen(1)
    print(f"Servidor en espera en {host}:{puerto}")
    client_socket, addr = server_socket.accept()
    print(f"Cliente conectado desde {addr}")

    # Recibe valor Ax y envia Bx
    client_socket.send(valor_ax.encode(encoding="ascii", errors="ignore"))
    valor_bx = int(client_socket.recv(1024).decode())

    # Calcula la clave compartida
    clave_compartida = str((valor_bx ** valor_a) % valor_p).zfill(8).encode()

    # Encripta el mensaje con la clave compartida y lo envía al cliente
    mensaje_encriptado = encrypt_des(clave_compartida, mensaje_original)
    client_socket.send(mensaje_encriptado)
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()






