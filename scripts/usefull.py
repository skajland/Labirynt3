from button import Button
import os
working_directory = os.getcwd()
working_directory_split = working_directory.split('/')
global_directory = ''.join(["/" + add for add in working_directory_split[1:-1]]) + "/"
data_directory = global_directory + "data/"


def create_button(what_to_say, pos, font_size, *func_arguments):
    return Button(what_to_say, pos, font_size,
                    (130, 130, 130, 70), (130, 130, 130, 100), (160, 160, 160, 150), *func_arguments)
