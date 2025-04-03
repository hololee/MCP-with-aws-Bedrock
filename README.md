# MCP with Bedrock

## get weather sample

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
uv run python main.py --text "뉴욕의 날씨 예보를 툴을 이용해서 알려줘."
```
