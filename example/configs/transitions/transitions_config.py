from pybotterfly.bot.transitions.transitions import Transitions, FileTrigger

from configs.config import BASE_CONFIG
from configs.logger import logger
from configs.transitions.payloads_config import payloads
from lib import pages
from lib.stages import General

transitions = Transitions(
    payloads=payloads,  # :Payloads. [Optional] Payload transitions of Payloads class
    config=BASE_CONFIG,  # :BaseConfig. [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
    logger=logger,  # :BaseLogger. [Optional] specify your logger of BaseLogger class if there are any changes
)

# adding the 'error_return'. When user's input is not added to 'transitions'
transitions.add_error_return(
    error_func=pages.error_page  # :Coroutine. The destination of error transition
)

# when the user is not in database
# first message in chat to start the bot ('Начать' button in VK or '/start' command in TG)
transitions.add_transition(
    trigger="/start",  # : str|FileTrigger|None. Is a default start input for TG. Trigger to run an FSM
    from_stage=General.start,  # :str. ‘Trigger’ will run FSM only if user is on this stage
    to_stage=pages.first_page,  # :Coroutine. The destination of this transition
    # [Optional]
    to_stage_id=General.first,  # :str. [Optional] specify a stage ID to go to. Changes user's stage ID in database
    # access_level="user",  # :str|List[str]. [Optional] specify required access level of the page. Users with another access level will not be able to access the page. Defaults to ["any"]
    # to_access_level="admin",  # :str. [Optional] specify new user's access level after transition. Defaults to None
)
transitions.add_transition(
    trigger="Начать",
    from_stage=General.start,
    to_stage=pages.first_page,
    to_stage_id=General.first,
)

# when the user is on the first page
transitions.add_transition(
    trigger="Start",
    from_stage=General.first,
    to_stage=pages.second_page,
    to_stage_id=General.second,
)

# when the user is on the fourth page
transitions.add_transition(
    trigger="Admin",
    from_stage=General.fourth,
    to_stage=pages.fourth_page,
    to_access_level="admin",
)
transitions.add_transition(
    trigger="Next",
    from_stage=General.fourth,
    to_stage=pages.fifth_page,
    to_stage_id=General.fifth,
    access_level="admin",
)
transitions.add_transition(
    trigger="Back",
    from_stage=General.fourth,
    to_stage=pages.third_before_page,
    to_stage_id=General.third,
    access_level=["user", "admin"],
    to_access_level="user",
)

# when the user is on the fifth page
transitions.add_transition(
    trigger=FileTrigger(
        extensions=[
            ".png",
            ".jpg",
            ".jpeg",
        ],  # :BaseConfig.ALLOWED_FILE_EXTENSIONS | List[BaseConfig.ALLOWED_FILE_EXTENSIONS]. File extension to be handled
        temporary=True,  # :bool. [Optional] if True, the file will not be saved in the database
    ),
    from_stage=General.fifth,
    to_stage=pages.sixth_page,
    to_stage_id=General.sixth,
    access_level="admin",
)
transitions.add_transition(
    trigger="Skip",
    from_stage=General.fifth,
    to_stage=pages.sixth_page,
    to_stage_id=General.sixth,
    access_level="admin",
)
transitions.add_transition(
    trigger="Back",
    from_stage=General.fifth,
    to_stage=pages.fourth_page,
    to_stage_id=General.fourth,
    access_level="admin",
    to_access_level="user",
)

# when the user is on the sixth page
transitions.add_transition(
    trigger=FileTrigger(
        extensions=[
            ".xls",
            ".xlsx",
            ".docx",
            ".pdf",
        ],  # :BaseConfig.ALLOWED_FILE_EXTENSIONS | List[BaseConfig.ALLOWED_FILE_EXTENSIONS]. File extension to be handled
        temporary=True,  # :bool. [Optional] if True, the file will not be saved in the database
    ),
    from_stage=General.sixth,
    to_stage=pages.seventh_page,
    to_stage_id=General.seventh,
    access_level="admin",
)
transitions.add_transition(
    trigger="Skip",
    from_stage=General.sixth,
    to_stage=pages.seventh_page,
    to_stage_id=General.seventh,
    access_level="admin",
)
transitions.add_transition(
    trigger="Back",
    from_stage=General.sixth,
    to_stage=pages.fifth_page,
    to_stage_id=General.fifth,
    access_level="admin",
)

# when the user is on the seventh page
transitions.add_transition(
    trigger="Restart",
    from_stage=General.seventh,
    to_stage=pages.first_page,
    to_stage_id=General.first,
    access_level="admin",
    to_access_level="user",
)
transitions.add_transition(
    trigger="Back",
    from_stage=General.seventh,
    to_stage=pages.sixth_page,
    to_stage_id=General.sixth,
    access_level="admin",
)


# compiles transitions
transitions.compile()
