# Cryptography Benchmark

## 📌 Overview
This project benchmarks three fundamental cryptographic algorithms — **AES, RSA, and SHA-256** — implemented in Python.  
The goal is to evaluate their **performance, scalability, and stability** under different conditions, providing valuable insights into symmetric encryption, asymmetric encryption, and hashing.  

This repository contains both the **source code** and the **final academic report**, making it a practical and theoretical reference for cryptography and information security.

---

## ✨ Features
- **AES (Advanced Encryption Standard)**: Encryption and decryption using CBC mode with PKCS7 padding.
- **RSA (Rivest–Shamir–Adleman)**: Public-key encryption/decryption with OAEP padding (2048-bit keys).
- **SHA-256**: Secure Hash Algorithm for data integrity verification.
- **Performance analysis**: Execution time measured with microsecond precision.
- **Statistical analysis**: Outlier removal, averages, and standard deviation.
- **Visualization**: Clear and comparative plots using Matplotlib.

---

## 📂 Project Structure
```
cryptography-benchmark/
├── src/                       # Python source code
│   ├── parte1_sp.py           # AES, RSA, SHA-256 benchmarks
│   └── parte2_sp.py           # Data analysis & visualization
│
├── report/
│   └── RelatorioFINAL.pdf     # Full academic report
│
├── images/                    # Graphs used in README & report
│   ├── aes_encryption_vs_decryption.png
│   ├── rsa_encryption_vs_decryption.png
│   ├── sha256_hash.png
│   ├── comparison_aes_rsa.png
│   ├── comparison_aes_sha.png
│   └── rsa_enc_vs_dec.png
│
├── requirements.txt           # Dependencies
├── README.md                  # Project documentation
└── LICENSE                    # MIT License
```

---

## ⚙️ Requirements
- Python 3.11+  
- Packages listed in `requirements.txt`

Main libraries:
- `cryptography`
- `hashlib`
- `numpy`
- `pandas`
- `matplotlib`

Install dependencies with:
```bash
pip install -r requirements.txt
```

---

## 🚀 Installation & Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/cryptography-benchmark.git
   cd cryptography-benchmark
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run benchmarks (AES, RSA, SHA-256):
   ```bash
   python src/parte1_sp.py
   ```

4. Run analysis & generate plots:
   ```bash
   python src/parte2_sp.py
   ```

Results will be displayed in the terminal and exported to plots inside the `images/` folder.


## 📄 Report
The full academic report is available here:  
📑 [RelatorioFINAL.pdf](report/RelatorioFINAL.pdf)

---

## 📜 License
This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 👩‍💻 Author
Developed by Liliana Silva, Catarina Abrantes and Ana Sofia Quintero, as part of the *Security and Privacy* course at the University of Porto.  
Showcasing expertise in **cryptography, performance analysis, and secure software development**.
