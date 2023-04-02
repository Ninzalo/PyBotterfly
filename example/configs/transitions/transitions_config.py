from configs.config import BASE_CONFIG
from pybotterfly.bot.transitions.transitions import Transitions
from configs.transitions.payloads_config import payloads
from lib import pages
from lib.stages import General

transitions = Transitions(config=BASE_CONFIG, payloads=payloads)

# adding the 'error_return'. When user's input is not added to 'transitions'
transitions.add_error_return(error_func=pages.error_page)

# when the user is not in database
# first message in chat to start a bot ('Начать' button in VK or '/start' command in TG)
transitions.add_transition(
    trigger="/start",  # is a default start input for TG
    src=General.start,
    dst=pages.first_page,
)
transitions.add_transition(
    trigger="Начать",  # is a default start input for VK
    src=General.start,
    dst=pages.first_page,
)

# when the user is on the first page
transitions.add_transition(
    trigger="start",
    src=General.first,
    dst=pages.second_page,
)

# when the user is on the third page
transitions.add_transition(
    trigger="go to previous",
    src=General.third,
    dst=pages.second_page,
)
transitions.add_transition(
    trigger="go to beginning",
    src=General.third,
    dst=pages.first_page,
)

# compiles transitions
transitions.compile()
