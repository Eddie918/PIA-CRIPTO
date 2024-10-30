import streamlit as st
import numpy as np
import random
import string

# Funciones para RSA
def mcd(a, b):
    while b:
        a, b = b, a % b
    return a

def is_num_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def generar_num_primo():
    while True:
        num = np.random.randint(2, 10000)
        if is_num_prime(num):
            return num

def generar_claves():
    p = generar_num_primo()
    q = generar_num_primo()
    while p == q:
        p = generar_num_primo()
    
    n = p * q
    phi = (p-1) * (q-1)
    
    e = 65537 if mcd(65537, phi) == 1 else 3
    while mcd(e, phi) != 1:
        e = random.randrange(2, phi)
    
    d = pow(e, -1, phi)
    return ((e, n), (d, n))

def encrypt_message(message, public_key):
    e, n = public_key
    return [pow(ord(char), e, n) for char in message]

def decrypt_message(encrypted_message, private_key):
    d, n = private_key
    return ''.join([chr(pow(char, d, n)) for char in encrypted_message])

#Cifrado Cesar
def cifrado_cesar(message, shift):
    alphabet = string.ascii_lowercase + string.ascii_uppercase
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet, shifted_alphabet)
    return message.translate(table)

def descifrado_cesar(message, shift):
    return cifrado_cesar(message, -shift)
    
    

# Configuración de la página en Streamlit
st.set_page_config(page_title="Proyecto Integrador de Criptografía", page_icon="🔐", layout="centered")

# Estilos personalizados con fondo claro
st.markdown("""
    <style>
        .main {
            background-color: #000000;
            color: #FFFFFF;
            padding: 20px;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            width: 100%;
            height: 50px;
            font-size: 18px;
            border-radius: 8px;
            margin: 5px 0;
        }
        h1, h2, .stTextInput, .stTextArea, .stText, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #FFFFFF; /* Cambia el color del texto a blanco para mayor visibilidad */
        }
        pre {
            background-color: #333333;
            color: #FFFFFF;
            padding: 10px;
            border-radius: 8px;
        }
    </style>
    """, unsafe_allow_html=True) 

# Título y bienvenida
st.title("Proyecto de Criptografía")
st.write("Bienvenido al menú principal. Selecciona una opción para continuar:")

# Inicializar el estado de la sesión si no existe
if 'opcion' not in st.session_state:
    st.session_state['opcion'] = None

if "public_key" not in st.session_state or "private_key" not in st.session_state:
    st.session_state["public_key"], st.session_state["private_key"] = generar_claves()

# Menú principal
st.header("Menú Principal")
col1, col2 = st.columns(2)

with col1:
    if st.button("Encriptar con RSA"):
        st.session_state["opcion"] = "rsa_encriptar"
    if st.button("Desencriptar con RSA"):
        st.session_state["opcion"] = "rsa_desencriptar"
    if st.button("Encriptar con Cifrado César"):
        st.session_state["opcion"] = "cesar_encriptar"

with col2:
    if st.button("Desencriptar con Cifrado César"):
        st.session_state["opcion"] = "cesar_desencriptar"
    if st.button("Información del Autor"):
        st.session_state["opcion"] = "autor"
    if st.button("Imprimir Código Fuente"):
        st.session_state["opcion"] = "codigo_fuente"

# Contenido según la opción seleccionada
if st.session_state["opcion"] == "rsa_encriptar":
    st.subheader("Encriptar Mensaje con RSA")
    st.write("Clave pública (e, n):", st.session_state["public_key"])
    message = st.text_input("Ingrese el mensaje que desea encriptar")
    if st.button("Encriptar Mensaje"):
        if message:
            encrypted_message = encrypt_message(message, st.session_state["public_key"])
            st.session_state['encrypted_message'] = encrypted_message
            st.write("Mensaje encriptado:", ', '.join(map(str, encrypted_message)))

elif st.session_state["opcion"] == "rsa_desencriptar":
    st.subheader("Desencriptar Mensaje con RSA")
    if 'encrypted_message' in st.session_state:
        encrypted_input = st.text_input("Mensaje encriptado (lista de números)", value=str(st.session_state['encrypted_message']))
        if st.button("Desencriptar"):
            try:
                encrypted_list = eval(encrypted_input)
                decrypted_message = decrypt_message(encrypted_list, st.session_state["private_key"])
                st.write("Mensaje desencriptado:", decrypted_message)
            except Exception as e:
                st.error(f"Error al desencriptar. Asegúrate de que el formato del mensaje encriptado sea correcto. Detalles: {e}")
    else:
        st.write("No hay mensaje encriptado disponible. Primero encripta un mensaje.")

elif st.session_state["opcion"] == "cesar_encriptar":
    st.subheader("Encriptar Mensaje con Cifrado César")
    message = st.text_input("Ingrese el mensaje que desea encriptar")
    shift = st.number_input("Ingrese el desplazamiento (número de posiciones)", min_value=1, max_value=25, value=3)
    if st.button("Encriptar Mensaje César"):
        encrypted_message = cifrado_cesar(message, shift)
        st.write("Mensaje encriptado:", encrypted_message)
        

elif st.session_state["opcion"] == "cesar_desencriptar":
    st.subheader("Desencriptar Mensaje con Cifrado César")
    encrypted_message = st.text_input("Ingrese el mensaje encriptado")
    shift = st.number_input("Ingrese el desplazamiento (número de posiciones)", min_value=1, max_value=25, value=3)
    if st.button("Desencriptar Mensaje César"):
        decrypted_message = descifrado_cesar(encrypted_message, shift)
        st.write("Mensaje desencriptado:", decrypted_message)

elif st.session_state["opcion"] == "autor":
    st.subheader("Información del Autor")
    st.write("Nombre: Saúl Edwin Arias Trejo")
    st.write("Correo: saul.ariast@uanl.edu.mx")
    st.write("Este proyecto fue desarrollado como parte del curso de Criptografía y Seguridad en la Información. Incluye los dos metodos que mas me gustaron que fueron el metodo de cifrado Cesar y el algoritmo de encriptación RSA.")
    st.write("Este proyecto incluye métodos de encriptación RSA y Cifrado César.")

elif st.session_state["opcion"] == "codigo_fuente":
    st.subheader("Código Fuente")
    st.code(open(__file__).read(), language='python')
