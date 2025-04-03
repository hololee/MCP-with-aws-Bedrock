import boto3


class CSVAgent:
    def __init__(
        self,
        region="ap-northeast-2",
        modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
        system_prompt="You are a helpful assistant that can answer questions and help with tasks.",
    ):
        self.region = region
        self.modelId = modelId
        self.system_prompt = system_prompt

        boto3.setup_default_session(profile_name='alpha')
        self.client = boto3.client('bedrock-runtime', region_name=self.region)

        # 대화 기록
        self.messages = []

    async def invoke(self, message):

        content = [{'text': message}]

        self.messages.append(
            {
                "role": "user",
                "content": content,
            }
        )

        response = self.client.converse(
            modelId=self.modelId,
            messages=self.messages,
            system=[{"text": self.system_prompt}],
            inferenceConfig={
                "maxTokens": 8192,
                "temperature": 0.7,
            },
        )

        self.messages.append(response["output"]["message"])

        return response


class CSVTool:
    def __init__(self):
        pass

    def get_tools(self):
        pass
