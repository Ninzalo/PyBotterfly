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
    payload="type:default/action:go_to_third_page/data:/plus:",  # :str. Trigger to run an FSM based on existing references
    to_stage=pages.third_page,  # :Coroutine. The destination of this payload transition
    to_stage_id=General.third,  # :str. [Optional] specify a stage ID to go to. Changes user's stage ID in database
    from_stage=General.second,  # :str. ‘Path’ will run FSM only if user is on this stage
    # access_level="user",  # :str|List[str]. [Optional] specify access level of the page. Users with another access level will not be able to access the page. Defaults to ["any"]
    # to_access_level="admin",  # :str. [Optional] specify access level of the page. Defaults to None
)

# adding fake payload for removing it later
payloads.add_payload(
    payload="type:fake/id:",
    to_stage=pages.third_page,
    to_stage_id=General.third,
    from_stage=General.second,
)

# automatically shortens all payloads
payloads.apply_rules()

# adding the secret payload
payloads.add_payload(
    payload="type:secret/action:go_to_secret_page",
    to_stage=pages.fifth_page,
    to_stage_id=General.fifth,
    from_stage=General.second,
    access_level="admin",
)

# safely removes payload without any effect on existing shortening rules
payloads.remove_payload(
    payload="type:fake/id:"  # :str. Trigger to run an FSM based on existing references
)

# compiles payloads
payloads.compile()
