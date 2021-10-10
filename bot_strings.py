bot_strings = {
    'help_bot_description': """/manual : guides you through the manual input system, which allow you to register your army by typing directly in the chat. Useful if you have only 1 or 2 types of units.\n\n/ocr : guides you through the image input system. Upload a image of your army, the bot will do the rest. Useful if you have a large variety of troops.\n\n/leaderboard : Allow you to see the 20 best commanders in the clan.\n\n/stats : See statistics about a player and his / her army.""",
    'manual_bot_description': """To manually register your army, follow the following pattern in a SINGLE MESSAGE:\n\n Your Commander Name(Your Max Army Size): Troop Name/Number, Troop Name/Number, ...\n\n And press Enter.""",
    'ocr_bot_description': """The OCR technology allow us to extract text from an image.\n\nTo register your army, you have to upload a cropped screenshot of your army that you can get by pressing ALT, and hovering your cursor over your army, when you\re on the map.\n\nThen, you have to attach your max troop size with your image, like shown in the image:\n\nAnd press Enter.""",
    'ocr_error': """Oops, looks like I can\'t read all the units properly. Please, try again with another image if you used the scan system, or check for typos in your message if you used manual input.""",
    'wrong_troop_size': """Attach a valid max troop size with your image (number between 5 and 95). Please retry.""",
    'troop_check': """Check if your max army size is between 5 and 95 (commander included) and the number of each troop you typed is correct.""",
    'manual_command_example': """Here is an example:\n"Gabagool(91): Imperial Palatine Guard/14, Vlandian Sharpshooter/49, Imperial Legionary/19" (without the quotation marks)""",
    'unknown_command': """Unknown command. Please type /commands to see the available commands."""
}


def construct_troop_size_error(nb_given: int):
    return f'The number you gave is inferior to the sum of all the troops I scanned ({nb_given + 1}, commander included). Please, retry.'
