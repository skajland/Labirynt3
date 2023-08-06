from button import Button


def create_button(what_to_say, pos, font_size, *func_arguments):
    return Button(what_to_say, pos, font_size,
                    (130, 130, 130, 70), (130, 130, 130, 100), (160, 160, 160, 150), *func_arguments)
