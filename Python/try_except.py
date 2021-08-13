from PIL import Image


try:
    # Normal execution
    pass
except Image.DecompressionBombError:
    # Known error
    pass
except Exception as e:
    print(f'====> Error: {e}')
