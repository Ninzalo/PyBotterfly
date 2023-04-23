from pybotterfly.bot.transitions.payloads import Payloads
from configs.config import BASE_CONFIG
from lib import pages
from lib.stages import General


payloads = Payloads(
    config=BASE_CONFIG  # [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
)

# when the user is on the second page
payloads.add_payload(
    payload="type:default/action:go_to_third_page/data:/plus:",  # :str. Trigger to run an FSM based on existing references
    from_stage=General.second,  # :str. ‘Path’ will run FSM only if user is on this stage
    to_stage=pages.third_page,  # :Coroutine. The destination of this payload transition
)

# adding the error payload. When user's input is not added to 'payloads'
payloads.add_error_payload(
    payload="type:error_input",  # :str. Trigger to run an FSM based on existing references
    to_stage=pages.error_page,  # :Coroutine. The destination of error payload transition
)

# automatically shortens all payloads
payloads.apply_rules()

# compiles payloads
payloads.compile()
