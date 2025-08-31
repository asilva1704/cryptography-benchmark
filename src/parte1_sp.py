import os
import timeit
import numpy as np
import hashlib
import pandas as pd 
import timeit
import os
from statistics import mean, stdev
import matplotlib.pyplot as plt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric import rsa, padding as rsa_padding
from cryptography.hazmat.primitives import hashes

# Função para gerar ficheiros aleatórios
def generate_random_file(file_sizes, n_files):
    for size in file_sizes:
        for i in range(n_files):
            file_name = f"random_{size}_{i}.txt"  # Garante que o nome do ficheiro é correto
            with open(file_name, "wb") as file:
                file.write(os.urandom(size))  # Gera conteúdo aleatório
# Benchmark genérico (usado por AES e SHA)
def benchmark_algorithm(func, input_data, iterations=100, warmup=5, drop_pct=0.05):
    for _ in range(warmup):
        func(input_data)
    timings = []
    for _ in range(iterations):
        start = timeit.default_timer()
        func(input_data)
        end = timeit.default_timer()
        timings.append((end - start) * 1e6)  # tempo em microssegundos
    k = int(len(timings) * drop_pct)
    trimmed = sorted(timings)[k:-k] if k > 0 else timings
    return mean(trimmed), stdev(trimmed)

from cryptography.hazmat.primitives.asymmetric import rsa, padding as rsa_padding

def generate_rsa_keypair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private_key, private_key.public_key()

def rsa_encrypt_benchmark(size, iterations=1000, warmup=10, drop_pct=0.05):
    priv, pub = generate_rsa_keypair()
    input_fixed = b'\x00' * size

    # Warm-up
    for _ in range(warmup):
        pub.encrypt(input_fixed, rsa_padding.PKCS1v15())

    fixed_times, random_times = [], []
    for _ in range(iterations):
        # 1 ficheiro
        start = timeit.default_timer()
        pub.encrypt(input_fixed, rsa_padding.PKCS1v15())
        end = timeit.default_timer()
        fixed_times.append((end - start) * 1e6)

        # múltiplos ficheiros
        rand_input = os.urandom(size)
        start = timeit.default_timer()
        pub.encrypt(rand_input, rsa_padding.PKCS1v15())
        end = timeit.default_timer()
        random_times.append((end - start) * 1e6)

    def trim(values):
        k = int(len(values) * drop_pct)
        return sorted(values)[k:-k] if k > 0 else values

    return {
        'Tamanho (bytes)': size,
        'Média - 1 ficheiro': mean(trim(fixed_times)),
        'Desvio - 1 ficheiro': stdev(trim(fixed_times)),
        'Média - 500 ficheiros': mean(trim(random_times)),
        'Desvio - 500 ficheiros': stdev(trim(random_times))
    }

def rsa_decrypt_benchmark(size, iterations=1000, warmup=10, drop_pct=0.05):
    priv, pub = generate_rsa_keypair()
    input_fixed = b'\x00' * size

    for _ in range(warmup):
        enc = pub.encrypt(input_fixed, rsa_padding.PKCS1v15())
        priv.decrypt(enc, rsa_padding.PKCS1v15())

    fixed_times, random_times = [], []
    for _ in range(iterations):
        enc = pub.encrypt(input_fixed, rsa_padding.PKCS1v15())
        start = timeit.default_timer()
        priv.decrypt(enc, rsa_padding.PKCS1v15())
        end = timeit.default_timer()
        fixed_times.append((end - start) * 1e6)

        rand_input = os.urandom(size)
        enc = pub.encrypt(rand_input, rsa_padding.PKCS1v15())
        start = timeit.default_timer()
        priv.decrypt(enc, rsa_padding.PKCS1v15())
        end = timeit.default_timer()
        random_times.append((end - start) * 1e6)

    def trim(values):
        k = int(len(values) * drop_pct)
        return sorted(values)[k:-k] if k > 0 else values

    return {
        'Tamanho (bytes)': size,
        'Média - 1 ficheiro': mean(trim(fixed_times)),
        'Desvio - 1 ficheiro': stdev(trim(fixed_times)),
        'Média - 500 ficheiros': mean(trim(random_times)),
        'Desvio - 500 ficheiros': stdev(trim(random_times))
    }


# Lista com tamanhos dos ficheiros a serem criados (ajustados conforme solicitado)
all_file_sizes_aes = [8, 64, 512, 4096, 32768, 262144, 2097152] 
all_file_sizes_rsa = [2, 4, 8, 16, 32, 64, 128]
all_file_sizes_sha = [8, 64, 512, 4096, 32768, 262144, 2097152]

n_files = 500  # Número de ficheiros por tamanho
generate_random_file(all_file_sizes_aes, n_files)  # Gera os ficheiros para AES
generate_random_file(all_file_sizes_rsa, n_files)  # Gera os ficheiros para RSA
generate_random_file(all_file_sizes_sha, n_files)  # Gera os ficheiros para SHA

# Função para calcular os tempos de encriptação e desencriptação com AES
def aes_encrypt_decrypt(file_sizes, n):
    aes_enc_times = []
    aes_dec_times = []

    for size in file_sizes:
        sum_enc = 0
        sum_dec = 0
        for id in range(n):
            file_name = f"random_{size}_{id}.txt"  # Nome correto do ficheiro
            key = os.urandom(32)  # 32 bytes = 256 bits
            iv = os.urandom(16)  # Vetor de inicialização

            # Leitura do ficheiro
            with open(file_name, "rb") as file:
                data = file.read()

            # Adicionar padding
            padder = padding.PKCS7(algorithms.AES.block_size).padder()
            padded_data = padder.update(data) + padder.finalize()

            # Criação do objeto Cipher com o algoritmo AES e o modo CBC
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
            encryptor = cipher.encryptor()
            decryptor = cipher.decryptor()

            # Encriptação
            start_e = timeit.default_timer()
            ct = encryptor.update(padded_data) + encryptor.finalize()  # Ciphertext
            end_e = timeit.default_timer()
            encryption_time = (end_e - start_e) * 1000000  # em microssegundos
            sum_enc += encryption_time

            # Desencriptação
            start_d = timeit.default_timer()
            pt = decryptor.update(ct) + decryptor.finalize()  # Ciphertext
            end_d = timeit.default_timer()
            decryption_time = (end_d - start_d) * 1000000  # em microssegundos
            sum_dec += decryption_time

        mean_enc = sum_enc / n
        mean_dec = sum_dec / n
        aes_enc_times.append(mean_enc)
        aes_dec_times.append(mean_dec)

    return aes_enc_times, aes_dec_times

# Função para encriptar e desencriptar com RSA 1 file
def rsa_encrypt_decrypt_1file(file_sizes, n_repeats=30, private_key=None):
    rsa_enc_times = []
    rsa_dec_times = []

    if private_key is None:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

    public_key = private_key.public_key()

    for size in file_sizes:
        file_name = f"random_{size}_0.txt"  # Usar sempre o mesmo ficheiro
        with open(file_name, "rb") as file:
            data = file.read()

        enc_times = []
        dec_times = []

        for _ in range(n_repeats):
            # Encrypt
            start_e = timeit.default_timer()
            ct = public_key.encrypt(
                data,
                rsa_padding.OAEP(
                    mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            end_e = timeit.default_timer()
            enc_times.append((end_e - start_e) * 1e6)

            # Decrypt
            start_d = timeit.default_timer()
            private_key.decrypt(
                ct,
                rsa_padding.OAEP(
                    mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            end_d = timeit.default_timer()
            dec_times.append((end_d - start_d) * 1e6)

        # Usar mediana OU média sem extremos para suavizar
        enc_mean = np.mean(sorted(enc_times)[2:-2])  # remove os 2 maiores e 2 menores
        dec_mean = np.mean(sorted(dec_times)[2:-2])

        rsa_enc_times.append(enc_mean)
        rsa_dec_times.append(dec_mean)

    return rsa_enc_times, rsa_dec_times

rsa_enc_smooth, rsa_dec_smooth = rsa_encrypt_decrypt_1file(all_file_sizes_rsa, n_repeats=30)


# Função para encriptar e desencriptar com RSA multi files

def rsa_encrypt_decrypt_multifiles(file_sizes, n_files_per_size=50, private_key=None):
    rsa_enc_times = []
    rsa_dec_times = []

    if private_key is None:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

    public_key = private_key.public_key()

    for size in file_sizes:
        enc_times = []
        dec_times = []

        for id in range(n_files_per_size):
            file_name = f"random_{size}_{id}.txt"
            with open(file_name, "rb") as file:
                data = file.read()

            # Encryption
            start_e = timeit.default_timer()
            ct = public_key.encrypt(
                data,
                rsa_padding.OAEP(
                    mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            end_e = timeit.default_timer()
            enc_times.append((end_e - start_e) * 1e6)

            # Decryption
            start_d = timeit.default_timer()
            private_key.decrypt(
                ct,
                rsa_padding.OAEP(
                    mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            end_d = timeit.default_timer()
            dec_times.append((end_d - start_d) * 1e6)

        # Descartar extremos e fazer média
        enc_mean = np.mean(sorted(enc_times)[2:-2])
        dec_mean = np.mean(sorted(dec_times)[2:-2])

        rsa_enc_times.append(enc_mean)
        rsa_dec_times.append(dec_mean)

    return rsa_enc_times, rsa_dec_times

rsa_enc_multi, rsa_dec_multi = rsa_encrypt_decrypt_multifiles(all_file_sizes_rsa, n_files_per_size=50)


# Função para calcular os tempos de geração de hash com SHA-256

def sha256(file_sizes, num_files):
    sha_times = []
    for size in file_sizes:
        total_time = 0
        for _ in range(num_files):
            # Geração de ficheiro temporário
            data = os.urandom(size)

            # Função a ser medida
            def sha256_function():
                hashlib.sha256(data).digest()

            # Aquecimento para garantir estabilidade
            for _ in range(5):  # Aquecer 5 vezes antes de medir
                sha256_function()

            # Medir o tempo usando timeit
            time_taken = timeit.timeit(sha256_function, number=1)  # Executa 1 vez
            total_time += time_taken * 1e6  # Convertendo para microsegundos

        # Calcular a média do tempo
        average_time = total_time / num_files
        sha_times.append(average_time)
    return sha_times

# AES e SHA (mantêm igual)
aes_enc, aes_dec = aes_encrypt_decrypt(all_file_sizes_aes, 100)
sha_gen = sha256(all_file_sizes_sha, 100)



# Plot com as novas variáveis separadas
def plot_results(all_file_sizes_aes, aes_enc_1, aes_dec_1, aes_enc_multi, aes_dec_multi,
                 rsa_enc_1, rsa_dec_1, sha_gen,
                 file_sizes_rsa, rsa_enc_multi, rsa_dec_multi, aes_enc_1file, aes_dec_1file):

    # Gráfico AES - Encryption vs Decryption (1 ficheiro)
    plt.figure(figsize=(8, 6))
    plt.plot(all_file_sizes_aes, aes_enc_1, label="AES Encryption (1 file)", marker='o', linestyle='-', color='blue')
    plt.plot(all_file_sizes_aes, aes_dec_1, label="AES Decryption (1 file)", marker='o', linestyle='--', color='orange')
    plt.xlabel('File Size (bytes)')
    plt.ylabel('Time (microseconds)')
    plt.title('AES: Encryption vs Decryption (1 file)')
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Gráfico AES - Encryption vs Decryption (múltiplos ficheiros)
    plt.figure(figsize=(8, 6))
    plt.plot(all_file_sizes_aes, aes_enc_multi, label="AES Encryption (multiple files)", marker='o', linestyle='-', color='blue')
    plt.plot(all_file_sizes_aes, aes_dec_multi, label="AES Decryption (multiple files)", marker='o', linestyle='--', color='orange')
    plt.xlabel('File Size (bytes)')
    plt.ylabel('Time (microseconds)')
    plt.title('AES: Encryption vs Decryption (multiple files)')
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    #RSA - 1 file
    plt.figure(figsize=(8, 6))
    plt.plot(all_file_sizes_rsa, rsa_enc_smooth, label="RSA Encryption (1 file)", marker='o', linestyle='-', color='green')
    plt.plot(all_file_sizes_rsa, rsa_dec_smooth, label="RSA Decryption (1 file)", marker='o', linestyle='--', color='red')
    plt.xlabel('File Size (bytes)')
    plt.ylabel('Time (microseconds)')
    plt.title('RSA: Encryption vs Decryption (1 file)')
    plt.legend()
    plt.grid(True)
    plt.xscale('log')
    plt.yscale('log')
    plt.tight_layout()
    plt.show()

    #RSA - Multifiles
    
    plt.figure(figsize=(8, 6))
    plt.plot(all_file_sizes_rsa, rsa_enc_multi, label="RSA Encryption (multiple files)", marker='o', linestyle='-', color='green')
    plt.plot(all_file_sizes_rsa, rsa_dec_multi, label="RSA Decryption (multiple files)", marker='o', linestyle='--', color='red')
    plt.xlabel('File Size (bytes)')
    plt.ylabel('Time (microseconds)')
    plt.title('RSA: Encryption vs Decryption (Multiple Files)')
    plt.legend()
    plt.grid(True)
    plt.xscale('log')
    plt.yscale('log')
    plt.tight_layout()
    plt.show()
      
    #GRAFICO SHA-1 file
    plt.figure(figsize=(8, 6))
    plt.plot(all_file_sizes_aes, sha_gen_1file, label="SHA-256 (1 file)", marker='o', linestyle='-', color='purple')
    plt.xlabel('File Size (bytes)')
    plt.ylabel('Time (microseconds)')
    plt.title('SHA-256 Hash Generation - 1 File per Size')
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    #Grafico SHA-multiple files
    plt.figure(figsize=(8, 6))
    plt.plot(all_file_sizes_aes, sha_gen_multifile, label="SHA-256 (Multiple files)", marker='s', linestyle='--', color='orange')
    plt.xlabel('File Size (bytes)')
    plt.ylabel('Time (microseconds)')
    plt.title('SHA-256 Hash Generation - Multiple Files per Size')
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


    # Gráfico AES - Comparação completa (4 curvas)
    plt.figure(figsize=(10, 7))
    plt.plot(all_file_sizes_aes, aes_enc_1file, label="AES Encryption (1 file)", marker='o', linestyle='-', color='blue')
    plt.plot(all_file_sizes_aes, aes_enc, label="AES Encryption (multiple files)", marker='o', linestyle='--', color='darkblue')
    plt.plot(all_file_sizes_aes, aes_dec_1file, label="AES Decryption (1 file)", marker='o', linestyle='-', color='orange')
    plt.plot(all_file_sizes_aes, aes_dec, label="AES Decryption (multiple files)", marker='o', linestyle='--', color='darkorange')
    plt.xlabel('File Size (bytes)')
    plt.ylabel('Time (microseconds)')
    plt.title('AES: Encryption vs Decryption (1 file vs multiple files)')
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    #RSA - Comparação completa 
    plt.figure(figsize=(10, 7))

    # 1 File por tamanho
    plt.plot(all_file_sizes_rsa, rsa_enc_1, label="RSA Encryption (1 file)", marker='o', linestyle='-', color='blue')
    plt.plot(all_file_sizes_rsa, rsa_dec_1, label="RSA Decryption (1 file)", marker='o', linestyle='--', color='orange')

    # Multiple files (com suavização)
    plt.plot(all_file_sizes_rsa, rsa_enc_multi, label="RSA Encryption (multiple files)", marker='s', linestyle='-', color='green')
    plt.plot(all_file_sizes_rsa, rsa_dec_multi, label="RSA Decryption (multiple files)", marker='s', linestyle='--', color='red')

    plt.xlabel('File Size (bytes)')
    plt.ylabel('Time (microseconds)')
    plt.title('RSA: Encryption vs Decryption (1 File vs Multiple Files)')
    plt.legend()
    plt.grid(True)
    plt.xscale('log')
    plt.yscale('log')
    plt.tight_layout()
    plt.show()


    #Grafico SHA - Comparação de 1 file com multiple files
    plt.figure(figsize=(8, 6))
    plt.plot(all_file_sizes_aes, sha_gen_1file, label="SHA-256 (1 file)", marker='o', linestyle='-', color='purple')
    plt.plot(all_file_sizes_aes, sha_gen_multifile, label="SHA-256 (Multiple files)", marker='s', linestyle='--', color='orange')
    plt.xlabel('File Size (bytes)')
    plt.ylabel('Time (microseconds)')
    plt.title('SHA-256 Hash Generation: 1 File vs Multiple Files')
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# AES para 1 ficheiro por tamanho
aes_enc_1file, aes_dec_1file = aes_encrypt_decrypt(all_file_sizes_aes, 1)

# AES para 1 ficheiro por tamanho
aes_enc_1, aes_dec_1 = aes_encrypt_decrypt(all_file_sizes_aes, 1)

# AES para múltiplos ficheiros (já feito antes)
aes_enc_multi, aes_dec_multi = aes_enc, aes_dec


# SHA-256 para 1 ficheiro por tamanho
sha_gen_1file = sha256(all_file_sizes_aes, 1)

# SHA-256 para múltiplos ficheiros por tamanho
sha_gen_multifile = sha256(all_file_sizes_aes, 5)


plot_results(
    all_file_sizes_aes, aes_enc_1, aes_dec_1, aes_enc_multi, aes_dec_multi,
    rsa_enc_smooth, rsa_dec_smooth, sha_gen,
    all_file_sizes_rsa, rsa_enc_multi, rsa_dec_multi,aes_enc_1file, aes_dec_1file,

)


# Evita que a janela feche logo (especialmente no Windows)
input("Pressione Enter para sair...")


# Função atualizada com iterações adaptativas por tamanho

def rsa_encrypt_decrypt_1file(file_sizes, n_repeats_small=1000, n_repeats_large=500, threshold=32):
    rsa_enc_means = []
    rsa_dec_means = []

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    for size in file_sizes:
        n_repeats = n_repeats_small if size <= threshold else n_repeats_large
        input_data = b'\x00' * size
        encrypted_times = []
        decrypted_times = []

        for _ in range(n_repeats):
            start_enc = timeit.default_timer()
            encrypted_data = public_key.encrypt(input_data, rsa_padding.PKCS1v15())
            end_enc = timeit.default_timer()
            encrypted_times.append((end_enc - start_enc) * 1e6)

            start_dec = timeit.default_timer()
            decrypted_data = private_key.decrypt(encrypted_data, rsa_padding.PKCS1v15())
            end_dec = timeit.default_timer()
            decrypted_times.append((end_dec - start_dec) * 1e6)

        rsa_enc_means.append(np.mean(sorted(encrypted_times)[2:-2]))
        rsa_dec_means.append(np.mean(sorted(decrypted_times)[2:-2]))

    return rsa_enc_means, rsa_dec_means
