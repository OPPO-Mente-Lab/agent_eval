from PIL import Image
import os
from toolset.utils import caching, check_func_call

TOOL_NAME = __name__.split(".")[-1]

@caching(time_str="7d", tool_name=TOOL_NAME)
def convert_format(args): # path: str, extension: str
    try:
        path = args['image_path']
        if not os.path.isabs(path):
            path = os.path.join(os.environ["FILE_DIR"], path)
        if not os.path.exists(path):
            raise Exception(f"File not found: {path}")
        file_name = os.path.splitext(os.path.basename(path))[0]
        extension = args['extension']
        if extension.startswith("."):
            extension = extension[1:]
        support_ext_list = ['png', 'apng', 'jfif', 'jpe', 'jpg', 'jpeg', 'bmp', 'dib', 'gif', 'pbm', 'pgm', 'ppm', 'pnm', 'blp', 'bufr', 'cur', 'pcx', 'dcx', 'dds', 'ps', 'eps', 'fit', 'fits', 'fli', 'flc', 'ftc', 'ftu', 'gbr', 'grib', 'h5', 'hdf', 'jp2', 'j2k', 'jpc', 'jpf', 'jpx', 'j2c', 'icns', 'ico', 'im', 'iim', 'mpg', 'mpeg', 'tif', 'tiff', 'mpo', 'msp', 'palm', 'pcd', 'pdf', 'pxr', 'psd', 'qoi', 'bw', 'rgb', 'rgba', 'sgi', 'ras', 'tga', 'icb', 'vda', 'vst', 'webp', 'wmf', 'emf', 'xbm', 'xpm']
        if extension.lower() not in support_ext_list:
            raise Exception(f"{extension} extension is not supported")
        extensions = Image.registered_extensions()
        format = extensions[f'.{extension}']
        image = Image.open(path)
        output_path = os.path.join(os.path.dirname(__file__), "../tool_output/")
        os.makedirs(output_path, exist_ok=True)
        output_path = os.path.join(output_path, file_name)
        image.save(f'{output_path}.{extension}', format=format)
        return {'output_image_path': f'{output_path}.{extension}', 'status': 'success'}
    except Exception as e:
        return {'error': e, 'status': 'error'}


@caching(time_str="long term", tool_name=TOOL_NAME)
def compress_image(args): # path: str
    try:
        input_path = args['image_path']
        if not os.path.isabs(input_path):
            input_path = os.path.join(os.environ["FILE_DIR"], input_path)
        if not os.path.exists(input_path):
            raise Exception(f"File not found: {input_path}")
        if "quality" not in args:
            quality = 10
        else:
            quality = int(args["quality"])
        output_path = os.path.join(os.path.dirname(__file__), "../tool_output/")
        os.makedirs(output_path, exist_ok=True)
        name, ext = os.path.splitext(os.path.basename(input_path))
        file_name = name + '_compress.jpeg'
        output_path = os.path.join(output_path, file_name)
        image = Image.open(input_path)
        image.save(output_path, quality=quality)
        return {'output_image_path': output_path, 'status': 'success'}
    except Exception as e:
        return {'error': e, 'status': 'error'}


@caching(time_str="long term", tool_name=TOOL_NAME)
def resize_image(args): # path: str
    try:
        input_path = args['image_path']
        if not os.path.isabs(input_path):
            input_path = os.path.join(os.environ["FILE_DIR"], input_path)

        if not os.path.exists(input_path):
            raise Exception(f"File not found: {input_path}")

        resize_ratio = args["resize_ratio"]
        output_path = os.path.join(os.path.dirname(__file__), "../tool_output/")
        os.makedirs(output_path, exist_ok=True)
        name, ext = os.path.splitext(os.path.basename(input_path))
        file_name = name + f'_resize_{resize_ratio}{ext}'
        output_path = os.path.join(output_path, file_name)
        image = Image.open(input_path)
        w, h = image.size
        resize_ratio=min(1,float(resize_ratio))
        image = image.resize((int(w*resize_ratio), int(h*resize_ratio)))
        image.save(output_path)
        return {'output_image_path': output_path, 'status': 'success'}
    except Exception as e:
        return {'error': e, 'status': 'error'}

    

