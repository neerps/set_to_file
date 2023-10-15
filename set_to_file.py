#!/usr/bin/env python3
# +=====================================================================================================================
# MIT License

# Copyright (c) 2023 Igor Fomin （范诚奕）

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# +=====================================================================================================================
import logging
import os.path
import yaml
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
# +=====================================================================================================================
def fill_set_from_file(set_to_fill, file_path, logger):
    try:
        with open(file_path, 'r') as file_hd:
            for line in file_hd:
                try:
                    line_to_write = line.rstrip()
                    set_to_fill.add(line_to_write)
                    logger.debug(f"Read item: {line_to_write} from file {file_path}")
                except ValueError:
                    print("Failed to load item from file to internal buffer")
    except OSError:
        print("Cannot open", file_path)

def fill_set_from_user(set_to_fill, loop_break_string, logger):
    item_from_user = ""
    while item_from_user != loop_break_string:
        item_from_user = input(f"Please, enter a single item to add ('{loop_break_string}' to stop): ")
        logger.debug(f"Read item: {item_from_user} from user")
        if item_from_user != loop_break_string:
            try:
                set_to_fill.add(item_from_user)
            except ValueError:
                print("Failed to add item from user")
    print("Stop user input")

def load_config_from_file(config_file_path):
    try:
        with open(config_file_path, 'r') as config_file:
            config = yaml.load(config_file, Loader=yaml.SafeLoader)
    except OSError:
        print("Cannot open configuration file", config_file_path)
    return config

def write_set_to_file(set_to_write, file_path, logger):
    try:
        with open(file_path, 'w') as file_hd:
            for elem in set_to_write:
                try:
                    file_hd.write(elem)
                    file_hd.write("\n")
                    logger.debug(f"Write item: {elem} to file {file_path}")
                except OSError:
                    print("Cannot write to a file", file_path)
    except OSError:
        print("cannot open", file_path)
# +=====================================================================================================================
script_logger = logging.getLogger(__name__)
script_logger.setLevel(logging.DEBUG)

logger_hd = logging.FileHandler(f"{__name__}.log", mode='w')
logger_fmt = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

logger_hd.setFormatter(logger_fmt)
script_logger.addHandler(logger_hd)

script_config_file_path = "set_to_file_conf.yaml"
script_config = load_config_from_file(script_config_file_path)

operating_mode = script_config["operating_mode"]
script_logger.debug(f"Operating mode: {operating_mode}")
if operating_mode != "user" and operating_mode != "file":
    raise NameError("Operating_mode should be 'user' or 'mode")
if operating_mode == "file":
    input_file_path = script_config["input_file_path"]
    script_logger.debug(f"Input file name: {input_file_path}")
output_file_path = script_config["output_file_path"]
script_logger.debug(f"Output file name: {output_file_path}")

items_set = set()
# If output file doesn't exist, there is nothing to try to open.
# But for existing file it's important to read-in previous items from a set before the overwrite.
if (os.path.isfile(output_file_path)):
    fill_set_from_file(items_set, output_file_path, script_logger)

if operating_mode == "user":
    loop_break_string = "break"
    fill_set_from_user(items_set, loop_break_string, script_logger)

if operating_mode == "file":
    fill_set_from_file(items_set, input_file_path, script_logger)

sorted_set = sorted(items_set)

write_set_to_file(sorted_set, output_file_path, script_logger)
# +=====================================================================================================================
