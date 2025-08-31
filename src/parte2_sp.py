import time
import numpy as np
import matplotlib.pyplot as plt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as rsa_padding
from cryptography.hazmat.backends import default_backend
import secrets

# ------------------------- Configurações -------------------------
AES_SHA_SIZES = [8, 64, 512, 4096, 32768, 262144, 2097152]
RSA_SIZES = [2, 4, 8, 16, 32, 64, 128]

REPS_SAME_FILE = 100
backend = default_backend()

# ------------------------- Funções auxiliares -------------------------
def generate_random_bytes(size):
    return secrets.token_bytes(size)

def time_function_fixed(func, fixed_args):
    times = []
    for _ in range(REPS_SAME_FILE):
        start = time.perf_counter()
        func(*fixed_args)
        end = time.perf_counter()
        times.append((end - start) * 1e6)  # microsegundos
    median = np.median(times)
    std = np.std(times)
    return median, std

# ------------------------- AES -------------------------
def aes_encrypt_only(data):
    key = secrets.token_bytes(32)
    iv = secrets.token_bytes(16)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    _ = encryptor.update(padded_data) + encryptor.finalize()

# ------------------------- RSA -------------------------
def rsa_encrypt_only(public_key, data):
    return public_key.encrypt(
        data,
        rsa_padding.OAEP(
            mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def rsa_decrypt_only(private_key, ciphertext):
    return private_key.decrypt(
        ciphertext,
        rsa_padding.OAEP(
            mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

# ------------------------- SHA -------------------------
def sha_digest(data):
    digest = hashes.Hash(hashes.SHA256(), backend=backend)
    digest.update(data)
    result = digest.finalize()

# ------------------------- Benchmarks -------------------------
def benchmark_fixed(sizes, operation):
    means = []
    stds = []
    for size in sizes:
        data = generate_random_bytes(size)
        median_time, std_time = time_function_fixed(operation, (data,))
        means.append(median_time)
        stds.append(std_time)
    return means, stds

def benchmark_rsa_separated_fixed(sizes):
    enc_means, enc_stds = [], []
    dec_means, dec_stds = [], []

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=backend
    )
    public_key = private_key.public_key()

    for size in sizes:
        data = generate_random_bytes(size)
        ciphertext = rsa_encrypt_only(public_key, data)

        median_enc, std_enc = time_function_fixed(rsa_encrypt_only, (public_key, data))
        median_dec, std_dec = time_function_fixed(rsa_decrypt_only, (private_key, ciphertext))

        enc_means.append(median_enc)
        enc_stds.append(std_enc)
        dec_means.append(median_dec)
        dec_stds.append(std_dec)

    return enc_means, enc_stds, dec_means, dec_stds

# ------------------------- Gráficos -------------------------
def plot_graph_loglog(title, sizes_list, means_list, labels, filename):
    plt.figure()
    for sizes, means, label in zip(sizes_list, means_list, labels):
        plt.plot(sizes, means, '-o', label=label)
    plt.xlabel('Tamanho do ficheiro (bytes)')
    plt.ylabel('Tempo médio (μs)')
    plt.title(title)
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()

# ------------------------- Execução dos Benchmarks -------------------------
print("Benchmarking AES...")
aes_enc_means, aes_enc_stds = benchmark_fixed(AES_SHA_SIZES, aes_encrypt_only)

print("Benchmarking RSA...")
rsa_enc_means, rsa_enc_stds, rsa_dec_means, rsa_dec_stds = benchmark_rsa_separated_fixed(RSA_SIZES)

print("Benchmarking SHA...")
sha_means, sha_stds = benchmark_fixed(AES_SHA_SIZES, sha_digest)

# ------------------------- Geração dos Gráficos -------------------------

# AES vs RSA (log-log)
plot_graph_loglog("AES vs RSA Encryption Times (log-log)",
                  [AES_SHA_SIZES, RSA_SIZES],
                  [aes_enc_means, rsa_enc_means],
                  ["AES Encriptação", "RSA Encriptação"],
                  "aes_vs_rsa_loglog.png")

# AES vs SHA (log-log)
plot_graph_loglog("AES vs SHA-256 Encryption Times (log-log)",
                  [AES_SHA_SIZES, AES_SHA_SIZES],
                  [aes_enc_means, sha_means],
                  ["AES Encriptação", "SHA-256"],
                  "aes_vs_sha_loglog.png")

# RSA Encriptação vs Decriptação (log-log)
plot_graph_loglog("RSA Encryption vs Decryption Times (log-log)",
                  [RSA_SIZES, RSA_SIZES],
                  [rsa_enc_means, rsa_dec_means],
                  ["RSA Encriptação", "RSA Decriptação"],
                  "rsa_enc_vs_dec_loglog.png")
