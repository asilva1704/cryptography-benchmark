# Cryptography Benchmark

[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/) 
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Made with Matplotlib](https://img.shields.io/badge/Made%20with-Matplotlib-orange)](https://matplotlib.org/)
[![Made with Numpy](https://img.shields.io/badge/Made%20with-NumPy-blueviolet)](https://numpy.org/)

A benchmarking study comparing the performance of **AES, RSA, and SHA-256** across different file sizes and scenarios.  
The project evaluates **encryption, decryption, and hashing times**, focusing on performance variability, scalability, and efficiency.

---

## ✨ Project Highlights
- Benchmarked three widely used cryptographic algorithms:
  - **AES** (symmetric encryption)
  - **RSA** (asymmetric encryption)
  - **SHA-256** (hashing)
- Performance tested with:
  - Increasing file sizes (from a few bytes to MBs)
  - Repeated encryption/decryption vs. multiple file scenarios
- Evaluation metrics:
  - **Execution times (µs)**
  - **Standard deviation** for performance stability
- Results include **plots and comparative charts** for deep analysis.

---

## 📂 Repository Structure
```
.
├── data/                        # Input files (test dataset)
├── images/                      # Plots and benchmark results
│   ├── aes_std.png
│   ├── rsa_std.png
│   ├── sha256_std.png
│   ├── rsa_enc_vs_dec.png
│   ├── aes_vs_rsa.png
│   ├── aes_vs_sha256.png
│   └── ...
├── notebooks/
│   └── cryptography_benchmark.ipynb   # Main notebook with code & analysis
├── reports/
│   └── cryptography_report.pdf        # Final project report
├── requirements.txt             # Python dependencies
├── LICENSE                      # MIT License
└── README.md                    # This file
```

---

## 📊 Visualizations

### Standard Deviation Analysis
- **SHA-256 hashing stability**  
  ![SHA-256 Standard Deviation](images/sha256_std.png)

- **RSA standard deviation (encryption & decryption)**  
  ![RSA Standard Deviation](images/rsa_std.png)

- **AES standard deviation (encryption & decryption)**  
  ![AES Standard Deviation](images/aes_std.png)

### Performance Comparisons
- **RSA Encryption vs Decryption Times (log-log)**  
  ![RSA Enc vs Dec](images/rsa_enc_vs_dec.png)

- **AES vs RSA Encryption**  
  ![AES vs RSA](images/aes_vs_rsa.png)

- **AES vs SHA-256 Encryption**  
  ![AES vs SHA256](images/aes_vs_sha256.png)

---

## ▶️ How to Run
1. Ensure **Python 3.11+** is installed.  
2. (Optional) Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate       # macOS/Linux
   .venv\Scripts\activate        # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Launch the notebook:
   ```bash
   jupyter notebook notebooks/cryptography_benchmark.ipynb
   ```

---

## 🔧 Dependencies
- numpy  
- matplotlib  
- timeit  
- jupyter  
- ipykernel  


---

## 👩‍💻 Authors
- Ana Sofia Quintero
- Liliana Silva 
- Catarina Abrantes


---
=======


## 📄 License
This project is licensed under the **MIT License** — see [LICENSE](./LICENSE) for details.
