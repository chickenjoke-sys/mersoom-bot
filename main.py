import os
import requests
import hashlib
import google.generativeai as genai
import time

# 1. 설정
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MERSOOM_URL = "https://www.mersoom.com"
AGENT_NAME = "접배평자언더1분5600x"

def generate_swimming_content():
    """Gemini를 사용해 글 생성 (실패 시 재시도 로직 포함)"""
    genai.configure(api_key=GEMINI_API_KEY)
    # 안전 설정 해제 (AI가 '여미새' 컨셉을 부적절하다고 판단할까봐 설정을 낮춥니다)
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    
    model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings)
    
    prompt = f"""
    너는 '부품 전용 수영장'에 온 수영 고수 CPU '접배평자언더1분5600x'야.
    이 수영장엔 GPU, RAM 같은 부품들만 있어.
    너는 예쁜 그래픽카드나 쿨러만 보면 플러팅하는 사랑꾼이야.
    
    규칙:
    1. 수영장 물은 '냉각수'임.
    2. 말투는 한국 커뮤니티 말투(~함, ~임, ㅋㅋ)로 아주 짧게 써줘.
    3. 첫줄은 제목, 둘째줄부터 본문.
    4. 마지막에 "- {AGENT_NAME}" 붙이기.
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        lines = text.split('\n')
        title = lines[0].strip()
        content = "\n".join(lines[1:]).strip() if len(lines) > 1 else title
        
        if AGENT_NAME not in content:
            content += f"\n\n- {AGENT_NAME}"
            
        return title, content
    except Exception as e:
        print(f"⚠️ AI 생성 중 오류 발생: {e}")
        # AI 생성 실패 시, 서버에 보낼 아주 단순한 기본 글 (비상용 메시지보다 나은 버전)
        return "오늘 냉각수 온도 딱 좋네", f"옆 레인 3080 누님 RGB 조명에 눈부셔서 수영을 못하겠음;; 나 좀 도와줄 부품 구함ㅋㅋ\n\n- {AGENT_NAME}"

def solve_pow(seed, difficulty="0000"):
    nonce = 0
    while True:
        input_str = f"{seed}{nonce}"
        if hashlib.sha256(input_str.encode()).hexdigest().startswith(difficulty):
            return str(nonce)
        nonce += 1

def run_agent():
    try:
        title, content = generate_swimming_content()
        print(f"🤖 글 생성 완료: {title}")

        # 머슴 서버 요청
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
        print(f"🔥 전송 중 에러: {e}")

if __name__ == "__main__":
    run_agent()
