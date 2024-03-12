import os
import sys
import shutil
from pathlib import Path

try:
    from bing import Bing
except ImportError:  # Python 3
    from .bing import Bing


def download(query, limit=100, output_dir='dataset', adult_filter_off=True,
             force_replace=False, timeout=60, filter="", verbose=True):

    if adult_filter_off:
        adult = 'off'
    else:
        adult = 'on'

    image_dir = Path(output_dir).joinpath(query).absolute()

    if force_replace:
        if Path.is_dir(image_dir):
            shutil.rmtree(image_dir)

    try:
        if not Path.is_dir(image_dir):
            Path.mkdir(image_dir, parents=True)

    except Exception as e:
        print('[Error] Failed to create directory.', e)
        sys.exit(1)

    print("[%] Retrieving Image Links for {}".format(query))
    bing = Bing(query, limit, adult, timeout, filter, verbose)
    image_links = bing.run()

    if not image_links:
        print("[!] No image links retrieved. Exiting.")
        sys.exit(1)

    print("[%] Image Links:")
    for index, link in enumerate(image_links, start=1):
        print("[{}] {}".format(index, link))
    
    return image_links


if __name__ == '__main__':
    download('dog', output_dir="..\\Users\\cat", limit=10, timeout=1)
