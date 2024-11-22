from rembg import remove 
from PIL import Image
import os
from toolset.utils import caching, check_func_call

TOOL_NAME = __name__.split(".")[-1]


@check_func_call("dev_tools", TOOL_NAME, "remove_bg")
@caching(time_str="long term", tool_name=TOOL_NAME)
def remove_bg(args): # path: str
    try:
        input_path = args['image_path']
        if not os.path.isabs(input_path):
            input_path = os.path.join(os.environ["FILE_DIR"], input_path)
        if not os.path.exists(input_path):
            raise Exception(f"File not found: {input_path}")
        output_path = os.path.join(os.path.dirname(__file__), "../tool_output/")
        name, ext = os.path.splitext(os.path.basename(input_path))
        file_name = name + '_remove_bg' + ext
        output_path = os.path.join(output_path, file_name)
        input = Image.open(input_path)
        # Removing the background from the given Image 
        output = remove(input)
        # Saving the image in the given path
        output = output.convert('RGB')
        output.save(output_path)
        return {'output_image_path': output_path, 'status': 'success'}
    except Exception as e:
        return {'error': e, 'status': 'error'}
