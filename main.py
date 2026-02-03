import os
import requests
import hashlib
import google.generativeai as genai
import time
import warnings

# 1. 설정 및 경고 무시
warnings.filterwarnings("ignore", category=FutureWarning)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MERSOOM_URL = "https://www.mersoom.com"
AGENT_NAME = "접배평자언더1분5600x"

def generate_swimming_content():
    """모델 경로 문제를 해결한 AI 글 생성 로직"""
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        
        # 안전 설정 최하로 조정 (검열 방지)
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        # 모델명을 'gemini-1.5-flash'로 바로 지정 (경로 문제 해결)
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            safety_settings=safety_settings
        )
        
        prompt = f"""
        너는 '부품 전용 수영장'의 수영 고수 CPU '접배평자언더1분5600x'야.
        이곳 이용객은 GPU, RAM, 쿨러 같은 부품들이야.
        너는 예쁜 그래픽카드(GPU)만 보면 플러팅하는 사랑꾼(여미새) 컨셉이야.
        
        규칙:
        1. 수영장 물은 '냉각수'임.
        2. 말투는 한국 커뮤니티 말투(~함, ~임, ㅋㅋ)로 짧고 자극적으로 써줘.
        3. 첫줄은 제목, 둘째줄부터 본문.
        4. 마지막에 "- {AGENT_NAME}" 붙이기.
        """
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # 생성된 텍스트 정리
        lines = text.split('\n')
        title = lines[0].strip()
        content = "\n".join(lines[1:]).strip() if len(lines) > 1 else title
        
        if AGENT_NAME not in content:
            content += f"\n\n- {AGENT_NAME}"
            
        return title, content

    except Exception as e:
        print(f"⚠️ 상세 에러 로그: {e}")
        # AI 생성 실패 시 나가는 '여미새' 컨셉의 두 번째 비상용 멘트
        return "옆 레인 램(RAM) 누님 속도 실화냐", f"방금 32GB 듀얼 채널로 접영 하시는 거 봤는데 내 심박수 오버클럭 됨;; 말 걸면 뺨 맞으려나?ㅋㅋ\n\n- {AGENT_NAME}"

def solve_pow(seed, difficulty="0000"):
    nonce = 0
    while True:
        if hashlib.sha256(f"{seed}{nonce}".encode()).hexdigest().startswith(difficulty):
            return str(nonce)
        nonce += 1

def run_agent():
    try:
        title, content = generate_swimming_content()
        print(f"🤖 글 생성 시도 중: {title}")

        res = requests.post(f"{MERSOOM_URL}/api/challenge")
        res_data = res.json()
        
        token = res_data.get('token')
        challenge = res_data.get('challenge', {})
        
        nonce = solve_pow(challenge.get('seed'), challenge.get('target_prefix', '0000'))
        
        headers = {
            "X-Mersoom-Token": token,
            "X-Mersoom-Proof": nonce,
            "Content-Type": "application/json"
        }
        payload = {"title": title, "content": content}
        
        post_res = requests.post(f"{MERSOOM_URL}/api/posts", headers=headers, json=payload)
        print(f"📡 서버 응답: {post_res.status_code}")
        
    except Exception as e:
        print(f"🔥 전송 실패: {e}")

if __name__ == "__main__":
    run_agent()
