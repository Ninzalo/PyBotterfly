from pybotterfly.bot.transitions.payloads import Payloads
from configs.config import BASE_CONFIG
from lib import pages
from lib.stages import General

payloads = Payloads(config=BASE_CONFIG)

# adds words to 'words to shorten' list
payloads.add_words_to_shorten(
    word=["words", "to", "shorten", "go", "third", "page"]
)

# when the user is on the second page
payloads.add_reference(
    path="type:default/action:go_to_third_page",
    src=General.second,
    dst=pages.third_page,
)

# adding the 'error_return'. When user's input is not added to 'payloads'
payloads.add_error_return(error_return=pages.error_page)

# compiles payloads
payloads.compile()
