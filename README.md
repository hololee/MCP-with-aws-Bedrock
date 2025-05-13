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

---

### SSE를 이용한 연결

test용 echo 서버 실행

```bash
uv run src/mcp_server/echo/app.py
```

cursor의 MCP를 다음과 같이 연결

```json
{
  "mcpServers": {
    "echo": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

>`mcp==1.8.1`을 보면 `mount_path`를 이용해서 대상을 지정할 수 있는데 cursor에서는 `/sse` 만 지원
>(이전  `mcp` 버전에서는 `mount_path` 지정 옵션이 없어서 아직 cursor의 미지원으로 생각중..)
