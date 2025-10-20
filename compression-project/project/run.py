import os

algorithms = ["huffman", "sf", "lz77", "lzw"]
input_file = "FILE.txt"
output_folder = "files"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(output_folder):
    file_path = os.path.join(output_folder, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"Obrisan fajl: {filename}")

for algo in algorithms:
    print(f"\n ============ {algo.upper()} ============")
    compressed_file = f"{output_folder}/{algo}_compressed.txt"
    decompressed_file = f"{output_folder}/{algo}_decompressed.txt"

    os.system(f"python main.py --encode {algo} --infile {input_file} --outfile {compressed_file}")
    os.system(f"python main.py --decode {algo} --infile {compressed_file} --outfile {decompressed_file}")
    os.system(f"python main.py --compare {input_file} {compressed_file} {decompressed_file}")
