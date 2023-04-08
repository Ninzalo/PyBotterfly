from configs.config import BASE_CONFIG
from pybotterfly.bot.transitions.transitions import Transitions
from configs.transitions.payloads_config import payloads
from lib import pages
from lib.stages import General

transitions = Transitions(
    config=BASE_CONFIG,  # [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
    payloads=payloads,  # Payload transitions of Payloads class
)

# adding the 'error_return'. When user's input is not added to 'transitions'
transitions.add_error_return(
    error_func=pages.error_page  # :Coroutine. The destination of error transition
)

# when the user is not in database
# first message in chat to start a bot ('Начать' button in VK or '/start' command in TG)
transitions.add_transition(
    trigger="/start",  # : str. Is a default start input for TG. Trigger to run an FSM
    src=General.start,  # :str. ‘Trigger’ will run FSM only if user is on this stage
    dst=pages.first_page,  # :Coroutine. The destination of this transition
)
transitions.add_transition(
    trigger="Начать",  # :str. Is a default start input for VK. Trigger to run an FSM
    src=General.start,  # :str. ‘Trigger’ will run FSM only if user is on this stage
    dst=pages.first_page,  # :Coroutine. The destination of this transition
)

# when the user is on the first page
transitions.add_transition(
    trigger="start",  # :str. Trigger to run an FSM
    src=General.first,  # :str. ‘Trigger’ will run FSM only if user is on this stage
    dst=pages.second_page,  # :Coroutine. The destination of this transition
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
