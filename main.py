from image_compressor import ImageCompressor


# print(f"CWD: {os.getcwd()}")

DESKTOP_PATH = "C:/Users/Evan/Desktop"
COMPRESSED_FOLDER = "Compressed Files"
FOLDER_NAME = "December 17, 2021"


IMPORT_LOCATION = f"{DESKTOP_PATH}/{FOLDER_NAME}"
EXPORT_LOCATION = f"{DESKTOP_PATH}/{COMPRESSED_FOLDER}/Outbox"

algos = ['NEAREST',
         'BOX',
         'BILINEAR',
         'HAMMING',
         'BICUBIC',
         'LANCZOS']

img_comp = ImageCompressor(import_loc=IMPORT_LOCATION,
                           export_loc=EXPORT_LOCATION,
                           resample_algo='LANCZOS')


if __name__ == '__main__':
    
    img_comp.run(print_debug=True)
