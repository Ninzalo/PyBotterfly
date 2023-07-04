from configs.config import BASE_CONFIG
from pybotterfly.bot.transitions.transitions import Transitions
from configs.transitions.payloads_config import payloads
from lib import pages
from lib.stages import General

transitions = Transitions(
    config=BASE_CONFIG,  # :BaseConfig. [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
    payloads=payloads,  # Payload transitions of Payloads class
)

# adding the 'error_return'. When user's input is not added to 'transitions'
transitions.add_error_return(
    error_func=pages.error_page  # :Coroutine. The destination of error transition
)

# when the user is not in database
# first message in chat to start the bot ('Начать' button in VK or '/start' command in TG)
transitions.add_transition(
    trigger="/start",  # : str. Is a default start input for TG. Trigger to run an FSM
    from_stage=General.start,  # :str. ‘Trigger’ will run FSM only if user is on this stage
    to_stage=pages.first_page,  # :Coroutine. The destination of this transition
    to_stage_id=General.first,  # :str. [Optional] specify a stage ID to go to. Changes user's stage ID in database
    # access_level="user",  # :str|List[str]. [Optional] specify access level of the page. Users with another access level will not be able to access the page. Defaults to ["any"]
    # to_access_level="admin",  # :str. [Optional] specify access level of the page. Defaults to None
)
transitions.add_transition(
    trigger="Начать",
    from_stage=General.start,
    to_stage=pages.first_page,
    to_stage_id=General.first,
)

# when the user is on the first page
transitions.add_transition(
    trigger="start",
    from_stage=General.first,
    to_stage=pages.second_page,
    to_stage_id=General.second,
    access_level=["user", "admin"],
)

# when the user is on the third page
transitions.add_transition(
    trigger="go to previous",
    from_stage=General.third,
    to_stage=pages.second_page,
    to_stage_id=General.second,
)
transitions.add_transition(
    trigger="go to beginning",
    from_stage=General.third,
    to_stage=pages.first_page,
    to_stage_id=General.first,
)
transitions.add_transition(
    trigger="go to next",
    from_stage=General.third,
    to_stage=pages.fourth_page,
    to_stage_id=General.fourth,
    access_level="user",
)

# when the user is on the fourth page
transitions.add_transition(
    trigger="Admin",
    from_stage=General.fourth,
    to_stage=pages.fourth_admin_page,
    to_access_level="admin",
)
transitions.add_transition(
    trigger="Go back",
    from_stage=General.fourth,
    to_stage=pages.third_page,
    to_stage_id=General.third,
)

# when the user is on the fifth page
transitions.add_transition(
    trigger="Go to beginning",
    from_stage=General.fifth,
    to_stage=pages.first_page,
    to_stage_id=General.first,
)
transitions.add_transition(
    trigger="User",
    from_stage=General.fifth,
    to_stage=pages.first_page,
    to_stage_id=General.first,
    to_access_level="user",
)

# compiles transitions
transitions.compile()
