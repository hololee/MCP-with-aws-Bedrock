
1. install [`uv`](https://github.com/astral-sh/uv)

```
curl -LsSf https://astral.sh/uv/install.sh | sh
uv self update
```

2. set python env

```
pyenv install 3.11
uv venv --python 3.11
uv sync
```

3. set aws

```
aws sso login --profile {alpha}
```

4. run

```
uv run python src/main.py
```
