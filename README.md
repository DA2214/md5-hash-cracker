# MD5 GPU-Accelerated Password Cracker

A Python-based MD5 password cracker that combines pure-Python brute-force for short passwords with GPU-accelerated cracking via Hashcat for longer passwords. Ideal for educational purposes and demonstrating CPU vs. GPU performance in password recovery.

## Features

* Reads MD5 hashes from a `hashes.txt` file (one hash per line).
* Attempts all printable ASCII candidates in increasing length order (1–8 characters).
* Uses pure Python (`hashlib`) to brute-force 1–2 character passwords.
* Offloads lengths ≥3 to GPU via [Hashcat](https://hashcat.net/hashcat/) mask attack for massive speed gains.
* Outputs each recovered password alongside the time taken (in seconds) with six decimals.

## Requirements

* **Python 3.7+**
* **Hashcat** (v6.x) installed and added to your system PATH.
* A GPU with OpenCL or CUDA support for accelerated cracking (optional but recommended).

## Installation

1. **Clone this repository**:

   ```bash
   git clone https://github.com/yourusername/md5-gpu-cracker.git
   cd md5-gpu-cracker
   ```

2. **Install Python dependencies** (if using a virtual environment):

   ```bash
   python -m venv venv
   source venv/bin/activate      # on Windows: venv\Scripts\activate
   pip install -r requirements.txt  # (if you have extra modules)
   ```

3. **Install Hashcat**:

   * **Via Winget (Windows)**: `winget install --id=hashcat.hashcat -e`
   * **Manual**: Download the latest 7z from [https://github.com/hashcat/hashcat/releases](https://github.com/hashcat/hashcat/releases) and extract to a folder. Add that folder to your PATH.

4. **Verify**:

   ```bash
   hashcat --help
   python password_cracker.py --help
   ```

## Usage

1. **Prepare `hashes.txt`**: place one MD5 hash per line.
2. **Run the cracker**:

   ```bash
   python password_cracker.py
   ```
3. **Output**: for each hash, you’ll see:

   ```
   plaintext[TAB]time_in_seconds
   ```
4. **Adjust bounds**: edit `min_length` and `max_length` in `password_cracker.py` if needed.

## File Structure

```
├── password_cracker.py   # Main script
├── hashes.txt            # Input file with MD5 hashes
├── README.md             # Project overview and instructions
└── requirements.txt      # (Optional) Python dependencies
```

## Analysis

After running the script, you can analyze how cracking time scales with password length. Generally, time grows exponentially with length, and GPU acceleration yields orders-of-magnitude improvements over CPU-only brute force.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for:

* Support for additional hash algorithms
* Integration with PyOpenCL/PyCUDA
* Enhanced reporting or logging

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
