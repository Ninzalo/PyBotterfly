[Back](https://github.com/Ninzalo/PyBotterfly)

## Keyboard creation

#### Instantiation of the class (Regular buttons)
An instance of Buttons class to create keyboard
```python
from pybotterfly.bot.returns.buttons import Buttons

keyboard = Buttons(
    config=BASE_CONFIG  # [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
)
```

#### Instantiation of the class (Inline buttons)
An instance of InlineButtons class to create keyboard
```python
from pybotterfly.bot.returns.buttons import InlineButtons

keyboard = InlineButtons(
    config=BASE_CONFIG  # [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
)
```

#### Adding buttons (Regular buttons)
You can add buttons with `keyboard.add_button` method
```python
keyboard.add_button(
    label="Button1",  # :str. The text of the button
    color="primary",  # :BaseConfig.BUTTONS_COLORS. The color of the button
)
```

#### Adding buttons (Inline buttons)
You can add buttons with `keyboard.add_button` method
```python
keyboard.add_button(
    label="Button1",  # :str. The text of the button
    color="primary",  # :BaseConfig.BUTTONS_COLORS. The color of the button
    payload={
        "type": "default",
        "action": "go_to_third_page",
        "data": 123,
        "plus": 111,
    }  # payload argument is required for Inline_buttons
)
```

#### Switching to the new line
You can add a new line with `keyboard.add_line` method
```python
keyboard.add_line()  # Your next button will be on a new row
```

#### Keyboard compilation
Compiles the keyboard
```python
keyboard.confirm()  # Compiles the keyboard. You can't use keyboard without using this method
```

#### [Example usage](https://github.com/Ninzalo/PyBotterfly/blob/master/example/lib/keyboards.py)
```shell
example/lib/keyboards.py
```


## Pages creation

#### Page function creation
Every page coroutine should include `user_messenger_id`, `user_messenger`, `message` arguments
```python
async def page(
    user_messenger_id: int,  # :int. User id to send the message
    user_messenger: str,  # :str. Represents one of the added messengers to which the user belongs
    message: str,  # :str. Received message from user
) -> Returns:
    ...
```

#### Instantiation of the class
An instance of Returns class to create pages
```python
from pybotterfly.bot.returns.message import Returns

return_cls = Returns()
```

#### Adding return
The answer on the user's input
```python
await return_cls.add_return(
    user_messenger_id=user_messenger_id,  # :int. User id to send the message
    user_messenger=user_messenger,  # :str. Represents one of the added messengers to which the user belongs
    text=text,  #:str. Text of the message (page)
    keyboard=keyboard,  # [Optional] :Buttons. An instance of preconfigured Buttons class. You are not able to add this argument if your keyboard is the instance of InlineButtons class
    # inline_keyboard=keyboard,  # [Optional] :InlineButtons. An instance of preconfigured InlineButtons class. You are not able to add this argument if your keyboard is the instance of Buttons class
)
```
Note: You can add multiple returns at once

#### [Example usage](https://github.com/Ninzalo/PyBotterfly/blob/master/example/lib/pages.py)
```shell
example/lib/pages.py
```


[Back](https://github.com/Ninzalo/PyBotterfly)
