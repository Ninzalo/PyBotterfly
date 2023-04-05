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
Messengers can’t handle more than specific amount of bytes in payloads. We should compress the data of the payload. (Not recommended to add words with the same first letter). 
‘words’ -> ‘w’, ‘to’ -> ‘t’, ‘shorten’ -> ‘s’.
```python
payloads.add_words_to_shorten(
    word=["words", "to", "shorten"]
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
You can add the 'error_return'. When user's input is not added to payload transitions
```python
payloads.add_error_return(
    error_return=error_page_coroutine # :Coroutine. The destination of error payload transition 
)
```

#### Payloads transitions compilation
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
    payloads=payloads, # specify your payloads transitions of Payloads class
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
You can add the 'error_return'. When user's input is not added to transitions
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


#### [Example usage](https://github.com/Ninzalo/PyBotterfly/blob/master/example/configs/transitions/transitions_config.py):
```shell
example/configs/transitions/transitions_config.py
```


## Message handler configuration

```python
from pybotterfly.message_handler.message_handler import MessageHandler

message_handler = MessageHandler(
    user_stage_getter=get_user_stage_func, # specify your coroutine to get user’s stage. Should contain ‘user_messenger_id’ and ‘user_messenger’ args.
    transitions=transitions, # specify your transitions of Transitions class
    base_config=BASE_CONFIG, # [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
)
```

#### [Example usage](https://github.com/Ninzalo/PyBotterfly/blob/master/example/configs/message_handler/message_handler_config.py): 
```shell
example/configs/message_handler/message_handler_config.py
```
