import re
import multiprocessing

def extract_ips(chunk):
    ip_pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    extracted_ips = []

    for line in chunk:
        try:
            ip = ip_pattern.search(line).group()
            extracted_ips.append(ip)
        except AttributeError:
            pass

    return extracted_ips

def main():
    chunk_size = 1000  # Adjust this based on your system's memory and performance
    pool_size = min(2, multiprocessing.cpu_count())  # Use the number of available CPU cores (up to 2)

    with open("output.txt") as h:
        lines = h.readlines()

    with multiprocessing.Pool(pool_size) as pool:
        chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]
        extracted_results = pool.map(extract_ips, chunks)

    with open("combo.txt", "a+") as h:
        for ips in extracted_results:
            h.writelines(ip + "\n" for ip in ips)

if __name__ == "__main__":
    main()
