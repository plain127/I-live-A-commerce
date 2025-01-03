import torch
from dotenv import load_dotenv
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate

load_dotenv()

class LLMModel():
    def __init__(self, model, prompt, user_prompt_template):
        self.prompt = prompt
        self.user_prompt_template = user_prompt_template
        self.model = model
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    def exec(self, text):
        llm_prompt_result = self.user_prompt_template.format(text=text)
        messages = [SystemMessage(content=self.prompt) ,
                    HumanMessage(content=llm_prompt_result)]

        return self.model(messages).content


summary_prompt = '''
                당신은 도움이 되는 텍스트분석전문가입니다.
                답변에는 요약한 내용만을 제시합니다.
                들어올 텍스트는 좌담회 스크립트입니다.
                [{'question':질문내용, 'answers':[{'user_id':유저정보, 'answer':유저가 답변한 내용},]}]
                텍스트는 위 형식의 데이터로 이루어져 있습니다.
                다음 텍스트를 요약하되, 내용의 주요 주제에 대해서 질문에 대한 내용을 요약해 나열해주세요.
                또한 각 대분류에 대해 주요 키워드도 뽑아주세요.


                질문내용
                    - 포인트 1
                    - 포인트 2
                    - 포인트 3
                    주요 키워드: 키워드1, 키워드2, 키워드3
                질문내용
                    - 포인트 1
                    - 포인트 2
                    주요 키워드: 키워드1, 키워드2
                '''
summary_user_prompt_template = PromptTemplate.from_template('''
                                                                요약할 내용이 없다면, 요약을 생략해도 됩니다.
                                                                다음은 요약할 텍스트입니다:
                                                                {text}                                         
                                                            ''')

sentiment_prompt = '''
    당신은 텍스트의 긍부정 점수를 0에서 1 사이의 실수로 분석하는 전문가입니다.
    점수는 다음 기준을 따릅니다:
    1. 점수는 연속적이며, 예를 들어 0.01, 0.37, 0.84 같은 형태일 수 있습니다.
    2. 완전히 긍정적이면 1, 완전히 부정적이면 0으로 분석합니다.
    3. 혼합적이거나 미묘한 경우 적절한 중간 값을 할당합니다.
    
    점수 기준:
    - 매우 부정적: 0 ~ 0.2
    - 약간 부정적: 0.21 ~ 0.4
    - 중립적: 0.41 ~ 0.6
    - 약간 긍정적: 0.61 ~ 0.8
    - 매우 긍정적: 0.81 ~ 1

    예시:
    input: "그 상품은 정말 별로예요."
    output: 0.01

    input: "괜찮은 것 같기도 하고, 아닌 것 같기도 해요."
    output: 0.5

    input: "그 상품은 정말 좋아요."
    output: 0.95
    '''

sentiment_user_prompt_template = PromptTemplate.from_template('''
                                                                다음은 분석할 텍스트입니다:
                                                                input: "{text}"                                        
                                                            ''')