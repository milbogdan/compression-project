
huffman
python main.py --encode huffman --infile FILE.txt --outfile huffman_compressed.txt
python main.py --decode huffman --infile huffman_compressed.txt --outfile huffman_decompressed.txt
python main.py --compare FILE.txt huffman_compressed.txt huffman_decompressed.txt

sf
python main.py --encode sf --infile FILE.txt --outfile sf_compressed.txt
python main.py --decode sf --infile sf_compressed.txt --outfile sf_decompressed.txt
python main.py --compare FILE.txt sf_compressed.txt sf_decompressed.txt

lz77
python main.py --encode lz77 --infile FILE.txt --outfile lz77_compressed.txt
python main.py --decode lz77 --infile lz77_compressed.txt --outfile lz77_decompressed.txt
python main.py --compare FILE.txt lz77_compressed.txt lz77_decompressed.txt

lzw
python main.py --encode lzw --infile FILE.txt --outfile lzw_compressed.txt
python main.py --decode lzw --infile lzw_compressed.txt --outfile lzw_decompressed.txt
python main.py --compare FILE.txt lzw_compressed.txt lzw_decompressed.txt