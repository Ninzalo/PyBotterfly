[Back](https://github.com/Ninzalo/PyBotterfly)

## Using example 

#### Create virtual environment

```shell
python -m venv venv
```

#### Activate virtual environment

```shell
source ./venv/bin/activate
```

#### Clone git repository

```shell
git clone https://github.com/Ninzalo/PyBotterfly.git
```

#### Copy example folder 

```shell
mv PyBotterfly/example .
```

#### Delete PyBotterfly folder

```shell
rm -rf PyBotterfly
```

#### Install all required packages

```shell
pip install -r example/requirements.txt
```

#### Go to example folder

```shell
cd example
```

#### Create database

Manually create your database

#### Set configuration variables

Location of the main config: `configs/config.py`

## Fast installation (for copy-pasting)

Ensure that `python` is a correct alias for your environment

```shell
python -m venv venv
source ./venv/bin/activate
git clone https://github.com/Ninzalo/PyBotterfly.git
mv PyBotterfly/example .
rm -rf PyBotterfly
pip install -r example/requirements.txt
cd example
```

## Running the example project

#### Add table for your database

```shell
python create_users_table.py
```

#### Run example server

```shell
python server.py
```

#### Run example clients (use different instances of your terminal)

```shell
python tg_client.py
```

```shell
python vk_client.py
```

[Back](https://github.com/Ninzalo/PyBotterfly)
