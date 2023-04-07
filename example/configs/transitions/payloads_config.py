from pybotterfly.bot.transitions.payloads import Payloads
from configs.config import BASE_CONFIG
from lib import pages
from lib.stages import General

payloads = Payloads(
    config=BASE_CONFIG # [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
)

# adds words to 'words to shorten' list
payloads.add_words_to_shorten(
    word=["words", "to", "shorten", "go", "third", "page"]
)

# when the user is on the second page
payloads.add_reference(
    path="type:default/action:go_to_third_page", # :str. Trigger to run an FSM based on existing references
    src=General.second, # :str. ‘Path’ will run FSM only if user is on this stage
    dst=pages.third_page, # :Coroutine. The destination of this payload transition 
)

# adding the 'error_return'. When user's input is not added to 'payloads'
payloads.add_error_return(
    error_return=pages.error_page # :Coroutine. The destination of error payload transition 
)

# compiles payloads
payloads.compile()
