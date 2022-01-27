"""
    The module for our ImageCompressor class.
"""
import os

from PIL import Image


# ----------------------------------------------------------------------------

class ImageCompressor:

    ALGOS_LIST = ['NEAREST', 'BOX', 'BILINEAR',
                  'HAMMING', 'BICUBIC', 'LANCZOS']

    def __init__(self,
                 import_loc: str,
                 export_loc: str,
                 resample_algo: str = 'LANCZOS'):
        self.__import_loc = import_loc
        self.__export_loc = export_loc
        self.__algo = resample_algo
        self.__files_list = self.__get_files_list(import_loc)
        # Additional statistical instance variables:
        self.total_compressed_size = 0
        self.total_uncompressed_size = 0
        self.percentage_compressed = 0.0

    def __get_files_list(self, import_from: str):
        """Helper method for finding the files at the provided import_loc
        and validating the location exists.

        Parameter
        ---------
        import_from: str
            A path to a directory of image files to import and compress.
        
        Returns
        -------
        list
            The list of file names at the specified import location.
        """
        # Validate the import path exists:
        if not os.path.exists(import_from):
            raise PathError(f"Import path does not exist: {import_from}")

        # [CASE] Path is to file:
        if os.path.isfile(import_from):
            print("Import path specified is not a directory! ")
            return []

        # [CASE] Path is to a directory:
        elif os.path.isdir(import_from):
            return [file for file in os.listdir(import_from)]

        return None

    def __select_algo(self):
        """Helper function for mapping the specified algo string with the
        correct algo constant from the PIL package.

        Returns
        -------
            int
        """
        mapping = {
            'NEAREST':  Image.NEAREST,
            'BOX':      Image.BOX,
            'BILINEAR': Image.BILINEAR,
            'HAMMING':  Image.HAMMING,
            'BICUBIC':  Image.BICUBIC,
            'LANCZOS':  Image.LANCZOS,
        }
        try:
            return mapping[self.__algo]
        except KeyError:
            print(f"NO SUCH RESAMPLE ALGORITHM: {self.__algo}")
        except Exception as e:
            print(e)
        # If mapping fails, use the default value as fallback:
        return Image.LANCZOS

    def run(self, print_debug: bool = False):
        """Compresses the image files based on the class configuration.

        Parameters
        ----------
        print_debug: bool, optional (default: False)
            Whether or not to print debug messages to the console.
        """
        for file in self.__files_list:
            # Construct file path:
            filepath = os.path.join(self.__import_loc, file)
            if not os.path.exists(filepath):
                print("An invalid file path was encountered while trying " +
                      f"to compress the image files. ({file})")
                return
            
            img = Image.open(filepath)
            dims = img.size

            # Determine storage size of uncompressed image:
            uncompressed_bytes = os.path.getsize(filepath)
            # Add the results to the total uncompressed stat:
            self.total_uncompressed_size += uncompressed_bytes

            # Use resize() to resample our image using the algo specified:
            re_img = img.resize(dims, resample=self.__select_algo())

            # Construct the export file path:
            new_filepath = os.path.join(self.__export_loc, file)

            # Save our new file to this path:
            if not os.path.exists(self.__export_loc):
                try: 
                    os.mkdir(self.__export_loc)
                except OSError as error: 
                    print(error)

            # Save our refactored image to its new location:
            re_img.save(new_filepath)

            # Now add the new file's storage size to the total stat:
            compressed_bytes = os.path.getsize(new_filepath)
            self.total_compressed_size += compressed_bytes

            if print_debug:
                # Calc MBs:
                before = self.__to_MB(uncompressed_bytes)
                after = self.__to_MB(compressed_bytes)
                perc = ((before - after) / before) * 100
                perc_rounded = round(perc, 2)
                before_round = round(before, 2)
                after_round = round(after, 2)
                log_str = f"\nFile: {file} | Size: {dims} | " +\
                          f"{before_round}MB => {after_round}MB " +\
                          f"({perc_rounded}%) "
                print(log_str)

        # Calc overall stats:
        stats_dict = {
            'total_files': len(self.__files_list),
            'percentage_compressed': round(self.__calc_percentage(), 2),
            'total_compressed_size': self.total_compressed_size,
            'total_uncompressed_size': self.total_uncompressed_size,
            'resample_algorithm': self.__algo, 
            'import_from': self.__import_loc,
            'export_to': self.__export_loc,
        }

        if print_debug:
            print("\n ----------------------------------------------- ")
            print(stats_dict)
  
        # Return the overall stats collected:
        return stats_dict
            
    def __calc_percentage(self):
        comp = self.total_compressed_size
        uncomp = self.total_uncompressed_size
        return  (uncomp - comp)/ uncomp
        
    @staticmethod
    def __to_MB(bytes_size: int):
        return bytes_size / (1024 * 1024)

    @staticmethod
    def get_resample_algos():
        __str = "The following are valid choices for resample algorithms: "
        for algo in self.ALGOS_LIST:
            __str += f"\n{algo}"
        print(__str)
