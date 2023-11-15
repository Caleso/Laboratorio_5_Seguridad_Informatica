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
    # Diffie-Hellman
    valor_p = 173
    valor_q = 50
    valor_b = int(input("Ingrese valor B secreto: "))
    valor_bx = str((valor_q ** valor_b) % valor_p)

    # Conexion
    host = "localhost"
    puerto = 8000
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, puerto))

    # Recibe valor Ax y envia Bx
    valor_ax = int(client_socket.recv(1024).decode())
    client_socket.send(valor_bx.encode(encoding="ascii", errors="ignore"))

    # Calcula la clave compartida
    clave_compartida = str((valor_ax ** valor_b) % valor_p).zfill(8).encode()

    # Recibe el mensaje encriptado del servidor y lo desencripta
    mensaje_encriptado = client_socket.recv(1024)
    mensaje_desencriptado = decrypt_des(clave_compartida, mensaje_encriptado)
    with open('mensajerecibido.txt', 'wb') as file:
        file.write(mensaje_desencriptado)
    client_socket.close()

if __name__ == "__main__":
    main()

