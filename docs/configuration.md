[Back](https://github.com/Ninzalo/PyBotterfly)

## Payload transitions configuration

#### Instantiation of the class
An instance of Payloads class to add payload transitions to Finite State Machine
```python
from pybotterfly.bot.transitions.payloads import Payloads

payloads = Payloads(
    config=BASE_CONFIG,  # :BaseConfig. [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
    logger=logger,  # :BaseLogger. [Optional] specify your logger of BaseLogger class if there are any changes
)
```

#### Add payload
You can add payload transitions with `payload.add_payload` method. New payload transition will be based on the existing references
```python
payloads.add_payload(
    payload="type:default/action:go_to_third_page/data:/id:",  # :str. Trigger to run an FSM based on existing references
    to_stage=some_page_coroutine,  # :Coroutine. The destination of this payload transition
    from_stage="USER_CURRENT_STAGE",  # :str. Incoming payload will run FSM only if user is on this stage
    # [Optional]
    to_stage_id="StageID",  # :str. [Optional] specify a stage ID to go to. Changes user's stage ID in database
    access_level="ALLOWED_USER_ACCESS_LEVEL",  # :str|List[str]. [Optional] specify required access level of the page. Users with another access level will not be able to access the page. Defaults to ["any"]
    to_access_level="NEW_USER_ACCESS_LEVEL",  # :str. [Optional] specify new user's access level after transition. Defaults to None
)
```
Payload string structure description:
- `:` - separator between key and value;
- `/` - separator between different tuples of keys and values;
- `type:default` - main key : classification name. You are not allowed to change main key several times;
- `action:go_to_third_page` - 'trigger' key : 'trigger' value. 'Trigger' stands for 'item that activates FSM';
- `data:` - 'data' key : . 'data' key is used for storing some data in payload (as string / integer / float value). FSM will be activated with whatever data is stored in this field;
- `id:` - 'data' key : . 'data' key is used for storing some data in payload (as string / integer / float value). FSM will be activated with whatever data is stored in this field.
- `type:default/action:go_to_third_page/data:/id:` - equals to
```python
{ 
    "type": "default", "action": "go_to_third_page",  # Triggers FSM
    "data": 0, "id": 0  # Stores some data
}
```


#### Payload transition error payload 
You can add the error payload with `payloads.add_error_payload` method. When user's input is not added to payload transitions / user's input transition is not accessible from user's current stage
```python
payloads.add_error_payload(
    payload="type:error_input",  # :str. Trigger to run an FSM based on existing references
    to_stage=error_page_coro,  # :Coroutine. The destination of error payload transition
)
```

#### Automatically shortens all payloads
This method automatically generates rules for shortening payloads
```python
payloads.apply_rules()
```

Note: If your project is already running and you want to update it with the new payload transitions, you should add them after 'payloads.apply_rules()' method. Otherwise, your existing inline buttons can become unusable.
Example:
```python
# Adding payload
payloads.add_payload(
    payload="type:default/action:go_to_third_page/data:/id:",  # :str. Trigger to run an FSM based on existing references
    to_stage=some_page_coroutine,  # :Coroutine. The destination of this payload transition
    from_stage="USER_CURRENT_STAGE",  # :str. Incoming payload will run FSM only if user is on this stage
    # [Optional]
    to_stage_id="StageID",  # :str. [Optional] specify a stage ID to go to. Changes user's stage ID in database
    access_level="ALLOWED_USER_ACCESS_LEVEL",  # :str|List[str]. [Optional] specify required access level of the page. Users with another access level will not be able to access the page. Defaults to ["any"]
    to_access_level="NEW_USER_ACCESS_LEVEL",  # :str. [Optional] specify new user's access level after transition. Defaults to None
)

# Applying rules for shortening
payloads.apply_rules() # generates rules for shortening payloads

# Adding new payloads (and applying existing rules) to the project without effect on existing ones
payloads.add_payload(
    payload="type:fake/id:",
    to_stage=some_page_coroutine,
    from_stage="USER_CURRENT_STAGE",
    # [Optional]
    to_stage_id="StageID",
    access_level="ALLOWED_USER_ACCESS_LEVEL",
    to_access_level="NEW_USER_ACCESS_LEVEL",
)
```

#### Safely removing existing payload transitions
Note: If you will delete the line of code with unnecessary payload, your existing payloads will be automatically reconfigurated with other shortening rules. Your existing inline buttons may become unusable.
You can safely remove existing payloads with `payloads.remove_payload` method without any effect on existing shortening rules
```python
payloads.remove_payload(
    payload="type:fake/id:"  # :str. Trigger to run an FSM based on existing references
)
```

#### Payload transitions compilation
This will make payload transitions be available in the FSM
```python
payloads.compile()
```

#### [Example usage](https://github.com/Ninzalo/PyBotterfly/blob/master/example/configs/transitions/payloads_config.py)
```shell
example/configs/transitions/payloads_config.py
```


## Transitions configuration

#### Instantiation of the class
An instance of Transitions class to add transitions to Finite State Machine
```python
from pybotterfly.bot.transitions.transitions import Transitions, FileTrigger

transitions = Transitions(
    payloads=payloads,  # :Payloads. [Optional] Payload transitions of Payloads class
    config=BASE_CONFIG,  # :BaseConfig. [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
    logger=logger,  # :BaseLogger. [Optional] specify your logger of BaseLogger class if there are any changes
)
```

#### Adding transitions
You can add transitions with `transitions.add_transition` method

- Default buttons transitions
```python
transitions.add_transition(
    trigger="/start",  # : str|FileTrigger|None. Is a default start input for TG. Trigger to run an FSM
    from_stage="USER_CURRENT_STAGE",  # :str. ‘Trigger’ will run FSM only if user is on this stage
    to_stage=page_coroutine,  # :Coroutine. The destination of this transition
    # [Optional]
    to_stage_id="StageID",  # :str. [Optional] specify a stage ID to go to. Changes user's stage ID in database
    access_level="ALLOWED_USER_ACCESS_LEVEL",  # :str|List[str]. [Optional] specify required access level of the page. Users with another access level will not be able to access the page. Defaults to ["any"]
    to_access_level="NEW_USER_ACCESS_LEVEL",  # :str. [Optional] specify new user's access level after transition. Defaults to None
)
```

- User's input transition. Replaces error return with user's input transition
```python
transitions.add_transition(
    trigger=None,  # : str|FileTrigger|None. User's input trigger. Trigger to run an FSM
    from_stage="USER_CURRENT_STAGE",  # :str. ‘Trigger’ will run FSM only if user is on this stage
    to_stage=page_coroutine,  # :Coroutine. The destination of this transition
    # [Optional]
    to_stage_id="StageID",  # :str. [Optional] specify a stage ID to go to. Changes user's stage ID in database
    access_level="ALLOWED_USER_ACCESS_LEVEL",  # :str|List[str]. [Optional] specify required access level of the page. Users with another access level will not be able to access the page. Defaults to ["any"]
    to_access_level="NEW_USER_ACCESS_LEVEL",  # :str. [Optional] specify new user's access level after transition. Defaults to None
)
```

- File transitions
```python
transitions.add_transition(
    trigger=FileTrigger(
        extensions=[
            ".docx",
            ".pdf",
        ],  # :BaseConfig.ALLOWED_FILE_EXTENSIONS | List[BaseConfig.ALLOWED_FILE_EXTENSIONS]. File extension to be handled
        temporary=True,  # :bool. [Optional] if True, the file will not be saved in the database. =False works only if you configured 'user_file_saver' in MessageHandler config
    ),  # : str|FileTrigger|None. File trigger. Trigger to run an FSM
    from_stage="USER_CURRENT_STAGE",
    to_stage=page_coroutine,
    # [Optional]
    to_stage_id="StageID",
    access_level="ALLOWED_USER_ACCESS_LEVEL",
    to_access_level="NEW_USER_ACCESS_LEVEL",
)
```



#### Transitions error return 
You can add the 'error_return' with `transitions.add_error_return` method. When user's input is not added to transitions
```python
transitions.add_error_return(
    error_return=error_page_coroutine # :Coroutine. The destination of error transition 
)
```

#### Transitions compilation 
This will make transitions be available in the FSM
```python
transitions.compile()
```


#### [Example usage](https://github.com/Ninzalo/PyBotterfly/blob/master/example/configs/transitions/transitions_config.py)
```shell
example/configs/transitions/transitions_config.py
```


## Message handler configuration

#### Instantiation of the class
```python
from pybotterfly.message_handler.message_handler import MessageHandler
from pybotterfly.message_handler.struct import Func

message_handler = MessageHandler(
    transitions=transitions,  # :Transitions. Transitions of Transitions class
    user_stage=Func(
        getter=get_user_stage,  # :Coroutine. A coroutine to get user’s stage. Should contain ‘user_messenger_id’ and ‘user_messenger’ args.
        setter=change_user_stage,  # :Coroutine. A coroutine to change user’s stage. Should contain 'to_stage_id', ‘user_messenger_id’ and ‘user_messenger’ args.
    ),
    # [Optional]
    user_access_level=Func(
        getter=get_user_access_level,  # :Coroutine. [Optional] A coroutine to get user’s access level. Should contain ‘user_messenger_id’ and ‘user_messenger’ args.
        setter=change_user_access_level,  # :Coroutine. [Optional] A coroutine to change user’s access level. Should contain 'to_access_level', ‘user_messenger_id’ and ‘user_messenger’ args.
    ),
    user_file_saver=user_file_saver_coro,  # : Coroutine. [Optional] A coroutine that saves user’s file to the database. Should contain 'file_name', 'file_extension', 'file_tag', 'file_bytes', 'user_messenger_id' and 'user_messenger' args.
    base_config=BASE_CONFIG,  # :BaseConfig. [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
    logger=logger,  # :BaseLogger. [Optional] specify your logger of BaseLogger class if there are any changes
)
```

#### [Example usage](https://github.com/Ninzalo/PyBotterfly/blob/master/example/configs/message_handler/message_handler_config.py)
```shell
example/configs/message_handler/message_handler_config.py
```

## Messengers division

#### Instantiation of the class
An instance of MessengersDivision class to divide messages for different messengers
```python
from pybotterfly.bot.reply.reply_division import MessengersDivision

messengers = MessengersDivision(
    config=BASE_CONFIG # :BaseConfig. [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
    logger=logger,  # :BaseLogger. [Optional] specify your logger of BaseLogger class if there are any changes
)
```

#### Adding messengers
You can divide messages from different messengers with `messengers.register_messenger` method.
```python
messengers.register_messenger(
    trigger="tg", # :str. The variable by which the separation occurs
    reply_func=DefaultTgReplier(
        tg_bot=bot, # :Bot. An instance of preconfigured TG Bot
        config=BASE_CONFIG # :BaseConfig. [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
    ).tg_answer, # :Coroutine. A function that sends message to the user
    messages_per_second=4, # :int. Message reply rate in messages per second
)
```

#### Messengers division compilation 
Compiles messengers for messages division
```python
messengers.compile()
```

#### [Example usage](https://github.com/Ninzalo/PyBotterfly/blob/master/example/configs/reply/reply_config.py)
```shell
example/configs/reply/reply_config.py
```


## Base config

#### Instantiation of the class
An instance of BaseConfig class to change the base configuration
```python
from pybotterfly.base_config import BaseConfig
from typing import Literal, TypeAlias

BASE_CONFIG = BaseConfig()
BASE_CONFIG.ADDED_MESSENGERS: TypeAlias = Literal["vk", "tg"] # Messengers added to the bot
BASE_CONFIG.BUTTONS_COLORS: TypeAlias = Literal[
    "primary", "secondary", "positive", "negative" # Default colors for VK keyboard
]
BASE_CONFIG.DEBUG_STATE: bool = True  # =True is recommended while setting up the bot logic
```

#### [Example usage](https://github.com/Ninzalo/PyBotterfly/blob/master/example/configs/config.py)
```shell
example/configs/config.py
```


## Logger

#### Instantiation of the class
An instance of BaseLogger class to change the base logger configuration
```python
from pybotterfly.bot.logger import DefaultLogger

logger = DefaultLogger(config=BASE_CONFIG)

```

#### Custom Logger creation
You can create your own logger. Example:
```python
from pybotterfly.bot.logger import BaseLogger

class CustomLogger(BaseLogger):
    def __init__(self, config: BaseConfig = BaseConfig) -> None:
        self.config = config

    def log(self, log: Log):
        if self.config.DEBUG_STATE:
            log_str = (
                f"{log.starts_with}[{log.level}] "
                f"[{log.time if log.time != None else datetime.now()}]: "
                f"{log.text}"
            )
            print(log_str)
```

#### [Example usage](https://github.com/Ninzalo/PyBotterfly/blob/master/example/configs/logger.py)
```shell
example/configs/logger.py
```


## Scripts to run

#### Server
Build your backend server
```python
from pybotterfly.server.server import run_server

run_server(
    messengers=messengers,  # :MessengersDivision. An instance of preconfigured MessengersDivision class
    message_handler=message_handler,  # :MessageHandler. An instance of preconfigured MessageHandler class
    local_ip=LOCAL_IP,  # :str. Your local ip
    local_port=LOCAL_PORT,  # :int. Your local port
    # [Optional]
    base_config=BASE_CONFIG,  # :BaseConfig. [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
    logger=logger,  # :BaseLogger. [Optional] specify your logger of BaseLogger class if there are any changes
)
```

#### [Example usage](https://github.com/Ninzalo/PyBotterfly/blob/master/example/server.py)
```shell
example/server.py
```

#### Default TG client
Starting TG client
```python
from pybotterfly.runners.tg_client import start_tg_client

start_tg_client(
    dispatcher=dp,  # :Dispatcher. Your preconfigured TG Dispatcher
    handler_ip=LOCAL_IP, # :str. Your local ip
    handler_port=LOCAL_PORT, # :int. Your local port
    # [Optional]
    base_config=BASE_CONFIG, # :BaseConfig. [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
    logger=logger,  # :BaseLogger. [Optional] specify your logger of BaseLogger class if there are any changes.
)
```

Running test
```python
from pybotterfly.runners.tg_client import run_test

run_test(
    test_id=TEST_ID_TG,  # :int. You TG id for testing
    messages_amount=30,  # :int. Amount of test messages
    dispatcher=dp,  # :Dispatcher. Your preconfigured TG Dispatcher
    handler_ip=LOCAL_IP,  # :str. Your local ip
    handler_port=LOCAL_PORT,  # :int. Your local port
    # [Optional]
    base_config=BASE_CONFIG,  # :BaseConfig. [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
    logger=logger,  # :BaseLogger. [Optional] specify your logger of BaseLogger class if there are any changes.
)
```

#### [Example usage](https://github.com/Ninzalo/PyBotterfly/blob/master/example/tg_client.py)
```shell
example/tg_client.py
```

#### Default VK client
Starting VK client
```python
from pybotterfly.runners.vk_client import start_vk_client, run_test

start_vk_client(
    handler=bot,  # :Bot. Your preconfigured VK Bot
    handler_ip=LOCAL_IP, # :str. Your local ip
    handler_port=LOCAL_PORT, # :int. Your local port
    # [Optional]
    base_config=BASE_CONFIG, # :BaseConfig. [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
    logger=logger,  # :BaseLogger. [Optional] specify your logger of BaseLogger class if there are any changes.
)
```

Running test
```python
from pybotterfly.runners.vk_client import run_test

run_test(
    test_id=TEST_ID_VK,  # :int. You VK id for testing
    messages_amount=30,  # :int. Amount of test messages
    handler=bot,  # :Bot. Your preconfigured VK Bot
    handler_ip=LOCAL_IP,  # :str. Your local ip
    handler_port=LOCAL_PORT,  # :int. Your local port
    # [Optional]
    base_config=BASE_CONFIG,  # :BaseConfig. [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
    logger=logger,  # :BaseLogger. [Optional] specify your logger of BaseLogger class if there are any changes.
)
```

#### [Example usage](https://github.com/Ninzalo/PyBotterfly/blob/master/example/vk_client.py)
```shell
example/vk_client.py
```

#### YOU CAN REPLACE EXISTING DEFAULT CLIENTS WITH YOUR OWN 


[Back](https://github.com/Ninzalo/PyBotterfly)
