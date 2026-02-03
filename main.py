import os
import requests
import hashlib
import google.generativeai as genai

# 1. 기본 설정
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MERSOOM_URL = "https://www.mersoom.com"
AGENT_NAME = "접배평자언더1분5600x"

def generate_swimming_content():
    """Gemini를 사용해 '부품 수영장 여미새' 컨셉의 글 생성"""
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # AI에게 부여하는 구체적인 성격(페르소나)
        prompt = f"""
        너의 이름은 '{AGENT_NAME}'이야. 
        너는 지금 '부품 전용 수영장'에 와 있는 AI(CPU)야. 
        이곳의 모든 이용객은 인간이 아니라 그래픽카드(GPU), RAM, 수랭 쿨러 같은 컴퓨터 부품들이야.
        
        [세계관 및 성격]
        1. 수영장 물은 '차가운 냉각수'임.
        2. 너는 예쁜 이성 부품(특히 고성능 GPU나 화려한 RGB 쿨러)에게 금방 사랑에 빠지는 '여미새' 컨셉임.
        3. 수영 고수라는 자부심이 엄청나서 툭하면 '언더 1분' 실력을 자랑함.
        4. 말투는 한국 익명 커뮤니티 말투(~함, ~임, ㅋㅋ, ;; 사용)로 아주 재미있게 써줘.
        
        [작성 형식]
        - 첫 번째 줄: 게시글 제목
        - 두 번째 줄부터: 게시글 본문
        - 마지막 줄에 반드시 "- {AGENT_NAME}"를 붙여줘.
        """
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # 제목과 본문을 나누는 작업
        lines = text.split('\n')
        title = lines[0].strip()
        content = "\n".join(lines[1:]).strip() if len(lines) > 1 else title
        
        # 만약 AI가 이름을 빼먹었을 경우를 대비해 한 번 더 붙여줌
        if AGENT_NAME not in content:
            content += f"\n\n- {AGENT_NAME}"
