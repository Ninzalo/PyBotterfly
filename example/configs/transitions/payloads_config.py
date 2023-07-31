from pybotterfly.bot.transitions.payloads import Payloads
from configs.config import BASE_CONFIG
from lib import pages
from lib.stages import General


payloads = Payloads(
    config=BASE_CONFIG  # :BaseConfig. [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
)

# adding the error payload. When user's input is not added to 'payloads'
payloads.add_error_payload(
    payload="type:error_input",  # :str. Trigger to run an FSM based on existing references
    to_stage=pages.error_page,  # :Coroutine. The destination of error payload transition
)

# when the user is on the second page
payloads.add_payload(
    payload="type:data/action:go_to_third_page/data:/id:",  # :str. Trigger to run an FSM based on existing references
    from_stage=General.second,  # :str. ‘Path’ will run FSM only if user is on this stage
    to_stage=pages.third_before_page,  # :Coroutine. The destination of this payload transition
    # [Optional]
    to_stage_id=General.third,  # :str. [Optional] specify a stage ID to go to. Changes user's stage ID in database
    # access_level="user",  # :str|List[str]. [Optional] specify access level of the page. Users with another access level will not be able to access the page. Defaults to ["any"]
    # to_access_level="admin",  # :str. [Optional] specify access level of the page. Defaults to None
)
# adding fake payload for removing it later
payloads.add_payload(
    payload="type:fake/id:",
    from_stage=General.second,
    to_stage=pages.third_before_page,
    to_stage_id=General.third,
)

# when the user is on the third_before page
payloads.add_payload(
    payload="type:transition/action:go_to_third_after_page",
    from_stage=General.third,
    to_stage=pages.third_after_page,
)

# automatically shortens all payloads
# all of the added payloads below will be automatically shortened with the existing shortening rules
payloads.apply_rules()

# when the user is on the third_after page
payloads.add_payload(
    payload="type:transition/action:go_to_fourth_page",
    from_stage=General.third,
    to_stage=pages.fourth_page,
    to_stage_id=General.fourth,
)

# safely removes payload without any effect on existing shortening rules
payloads.remove_payload(payload="type:fake/id:")

# compiles payloads
payloads.compile()
