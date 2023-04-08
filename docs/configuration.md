[Back](https://github.com/Ninzalo/PyBotterfly)

## Payload transitions configuration

#### Instantiation of the class
An instance of Payloads class to add payload transitions to Finite State Machine
```python
from pybotterfly.bot.transitions.payloads import Payloads

payloads = Payloads(
    config=BASE_CONFIG # [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
)
```

#### Add words to shorten
Messengers can’t handle more than specific amount of bytes in payloads. We should compress the data of the payload with `papayloads.add_words_to_shorten` method. Not recommended to add words with the same first letter). 
‘words’ -> ‘w’, ‘to’ -> ‘t’, ‘shorten’ -> ‘s’.
```python
payloads.add_words_to_shorten(
    word=["words", "to", "shorten"] # :str | List[str]
)
```

#### Add payload reference
You can add payload transitions reference with `payloads.add_reference` method. This payload transition will be automatically added to the list of payload transitions
```python
payloads.add_reference(
    path='type:default/action:go_to_second_page', # :str. Trigger to run an FSM
    src=“USER_CURRENT_STAGE”, # :str. ‘Path’ will run FSM only if user is on this stage
    dst=page_coroutine, # :Coroutine. The destination of this payload transition 
)
```

#### Add payload
You can add payload transitions with `payload.add_payload` method. New payload transition will be based on the existing reference
```python
payloads.add_payload(
    path='type:default/action:go_to_third_page', # :str. Trigger to run an FSM based on existing references
    src=“USER_CURRENT_STAGE”, # :str. ‘Path’ will run FSM only if user is on this stage
    dst=page_coroutine, # :Coroutine. The destination of this payload transition 
)
```

#### Payload transition error return 
You can add the 'error_return' with `payloads.add_error_return` method. When user's input is not added to payload transitions
```python
payloads.add_error_return(
    error_return=error_page_coroutine # :Coroutine. The destination of error payload transition 
)
```

#### Payload transitions compilation
This will make payload transitions be available in the FSM
```python
transitions.compile()
```

#### [Example usage](https://github.com/Ninzalo/PyBotterfly/blob/master/example/configs/transitions/payloads_config.py)
```shell
example/configs/transitions/payloads_config.py
```


## Transitions configuration

#### Instantiation of the class
An instance of Transitions class to add transitions to Finite State Machine
```python
from pybotterfly.bot.transitions.transitions import Transitions

transitions = Transitions(
    payloads=payloads, # Payload transitions of Payloads class
    config=BASE_CONFIG, # [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
)
```

#### Adding transitions
You can add transitions with `transitions.add_transition` method
```python
transitions.add_transition(
    trigger="start", # :str. Trigger to run an FSM
    src=“USER_CURRENT_STAGE”, # :str. ‘Trigger’ will run FSM only if user is on this stage
    dst=page_coroutine, # :Coroutine. The destination of this transition 
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

message_handler = MessageHandler(
    user_stage_getter=get_user_stage_func, # :Coroutine. Function to get user’s stage. Should contain ‘user_messenger_id’ and ‘user_messenger’ args.
    transitions=transitions, # Transitions of Transitions class
    base_config=BASE_CONFIG, # [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
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
    config=BASE_CONFIG # [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
)
```

#### Adding messengers
You can divide messages from different messengers with `messengers.register_messenger` method.
```python
messengers.register_messenger(
    trigger="tg", # :str. The variable by which the separation occurs
    reply_func=DefaultTgReplier(
        tg_bot=bot, # An instance of preconfigured TG Bot
        config=BASE_CONFIG # [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
    ).tg_answer, # : Coroutine. A function that sends message to the user
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

## Scripts to run

#### Server
Build your backend server
```python
from pybotterfly.runners.server import run_server

run_server(
    messengers=messengers,  # :MessengersDivision. An instance of preconfigured MessengersDivision class
    message_handler=message_handler,  # :MessageHandler. An instance of preconfigured MessageHandler class
    local_ip=LOCAL_IP,  # :str. Your local ip
    local_port=LOCAL_PORT,  # :int. Your local port
    base_config=BASE_CONFIG,  # [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
)
```

[Example usage](https://github.com/Ninzalo/PyBotterfly/blob/master/example/server.py)

#### Default TG client
Starting TG client
```python

from pybotterfly.runners.tg_client import start_tg_client

start_tg_client(
    dispatcher=dp, # Your preconfigured TG Dispatcher
    handler_ip=LOCAL_IP, # :str. Your local ip
    handler_port=LOCAL_PORT, # :int. Your local port
    base_config=BASE_CONFIG, # [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
)
```

Running test
```python
from pybotterfly.runners.tg_client import run_test

run_test(
    test_id=TEST_ID_TG, # :int. You TG id for testing
    messages_amount=30, # :int. Amount of test messages
    dispatcher=dp, # Your preconfigured TG Dispatcher
    handler_ip=LOCAL_IP, # :str. Your local ip
    handler_port=LOCAL_PORT, # :int. Your local port
    base_config=BASE_CONFIG, # [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
)
```

[Example usage](https://github.com/Ninzalo/PyBotterfly/blob/master/example/tg_client.py)

#### Default VK client
Starting VK client
```python
from pybotterfly.runners.vk_client import start_vk_client, run_test

start_vk_client(
    handler=bot, # Your preconfigured VK Bot
    handler_ip=LOCAL_IP, # :str. Your local ip
    handler_port=LOCAL_PORT, # :int. Your local port
    base_config=BASE_CONFIG, # [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
)
```

Running test
```python
run_test(
    test_id=TEST_ID_VK, # :int. You VK id for testing
    messages_amount=30, # :int. Amount of test messages
    handler=bot, # Your preconfigured VK Bot
    handler_ip=LOCAL_IP, # :str. Your local ip
    handler_port=LOCAL_PORT, # :int. Your local port
    base_config=BASE_CONFIG, # [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
)
```

[Example usage](https://github.com/Ninzalo/PyBotterfly/blob/master/example/vk_client.py)

#### YOU CAN REPLACE EXISTING DEFAULT CLIENTS WITH YOUR OWN 


[Back](https://github.com/Ninzalo/PyBotterfly)
