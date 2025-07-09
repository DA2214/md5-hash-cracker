import itertools
import hashlib
import time
import subprocess
import shutil
from pathlib import Path

# List of all printable ASCII characters
ASCII = [chr(i) for i in range(32, 127)]

# Locates the Hashcat executable in the system PATH
HASHCAT_CMD = shutil.which('hashcat')

# Finds Hashcat's directory to set working directory
HASHCAT_DIRECTORY = str(Path(HASHCAT_CMD).parent)

# Reads hashes from filename (hashes.txt)
def read_hashes(filename):
    hashes = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            h = line.strip()
            if h:
                hashes.append(h)
    return hashes

# Uses Hashcat in GPU-mask mode to crack an MD5 hashed password of a given length using the ASCII characters
def hashcat_gpu_helper(target, length, charset):
    mask = '?1' * length
    custom = ''.join(charset)
    cmd = [
        HASHCAT_CMD,
        '-a', '3',                      # Brute-force attack mode
        '-m', '0',                      # MD5 hash mode
        f'--custom-charset1={custom}',  # Custom charset for ASCII (defined at the top)
        target,                         # Target hash
        mask,                           # Mask for the password length
        '--quiet', '--show'             # hides unnecessary output and shows results when there's a match
    ]

    # Runs the Hashcat command and captures its output
    result = subprocess.run(
        cmd,
        cwd=HASHCAT_DIRECTORY,
        capture_output=True,
        text=True
    )

    # Parses the Hashcat output to find the cracked password
    for line in result.stdout.splitlines():
        if line.startswith(target + ':'):
            return line.split(':', 1)[1]
    return None

# Brute-forces the parsed hashes, lengths 1-2 are cracked in Python, lengths 3-8 are cracked using the GPU
def brute_force_crack(hashes, min_length=1, max_length=8):
    for target in hashes:
        start = time.perf_counter()
        password = None
        for length in range(min_length, max_length + 1):
            if length <= 2:
                for combo in itertools.product(ASCII, repeat=length):
                    attempt = ''.join(combo)
                    if hashlib.md5(attempt.encode('utf-8')).hexdigest() == target:
                        password = attempt
                        break
            else:
                password = hashcat_gpu_helper(target, length, ASCII)
            if password:
                break
        end = time.perf_counter()
        total_time = round(end - start, 6)
        total_str = format(total_time, ".6f")
        print(password, total_str, sep="\t")

# Main function to read hashes and brute force them
def main():
    hashes = read_hashes('hashes.txt')
    brute_force_crack(hashes, min_length=1, max_length=8)

main()
