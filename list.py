from __future__ import print_function, unicode_literals

from pprint import pprint

from PyInquirer import prompt, Separator

from examples import custom_style_2


questions = [
    {
        'type': 'list',
        'name': 'option',
        'message': 'Choose an option?',
        'choices': [
            '1) Start sending emails',
            '2) Manual configuration for sending emails',
            '3) Show list of emails set',
            '4) Show all configuration set',
            '5) Exit program',
        ]
    }
]

answers = prompt(questions, style=custom_style_2)
pprint(answers)