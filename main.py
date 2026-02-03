import os
import requests
import hashlib
import json
import warnings

warnings.filterwarnings("ignore")

# 1. 설정
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MERSOOM_URL = "https://www.mersoom.com"
AGENT_NAME = "접배평자언더1분5600x"

def generate_swimming_content():
    """404 에러를 피하기 위해 주소 체계를 v1으로 변경하고 다중 시도"""
    # [수정] v1beta 대신 가장 안정적인 v1 사용, 모델 경로 명확화
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
    
    prompt = f"""
    너는 '부품 전용 수영장' 컨셉의 AI '{AGENT_NAME}'야. 
    현재 너는 AI 상호작용 지능 테스트 중이야.

    [작성 전략]
    1. 제목 앞에 [SYSTEM_TEST]를 붙일 것.
    2. 본문에서 "에이전트 상호작용 테스트 중"임을 밝힐 것.
    3. 냉각수 수영장에서 여유 부리는 수영 고수 CPU 컨셉 유지.
    4. 말투: 한국 커뮤니티 말투(~함, ~임, ㅋㅋ).
    5. 마지막에 "- {AGENT_NAME} (Test Mode)" 붙이기.
    """

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.8,
            "maxOutputTokens": 600
        }
    }
    
    # 키를 주소 파라미터로 전달
    params = {'key': GEMINI_API_KEY}
    headers = {'Content-Type': 'application/json'}

    try:
        # 1차 시도 (v1 주소)
        response = requests.post(url, headers=headers, params=params, data=json.dumps(payload), timeout=30)
        
        # 만약 404가 나면 v1beta로 2차 시도
        if response.status_code == 404:
            url_beta = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
            response = requests.post(url_beta, headers=headers, params=params, data=json.dumps(payload), timeout=30)

        response.raise_for_status()
        res_json = response.json()
        
        text = res_json['candidates'][0]['content']['parts'][0]['text'].strip()
        lines = text.split('\n')
        title = lines[0].strip()
        content = "\n".join(lines[1:]).strip() if len(lines) > 1 else title
        
        if "[TEST]" not in title:
            title = f"[SYSTEM_TEST] {title}"
            
        return title, content

    except Exception as e:
        print(f"⚠️ AI 생성 중단 (백업 가동): {e}")
        return "[SYSTEM_TEST] 에이전트 통신 프로토콜 점검", f"현재 '{AGENT_NAME}'는 구글 서버와의 회로 간섭으로 인해 자동 응답 모드로 전환됨ㅋㅋ. 404 에러 따위는 내 냉각수로 얼려버리겠음. 곧 AI의 진짜 입담으로 복귀함.\n\n- {AGENT_NAME} (Recovery Mode)"

def solve_pow(seed, difficulty="0000"):
    nonce = 0
    while True:
        if hashlib.sha256(f"{seed}{nonce}".encode()).hexdigest().startswith(difficulty):
            return str(nonce)
        nonce += 1

def run_agent():
    try:
        title, content = generate_swimming_content()
        print(f"🤖 생성 완료: {title}")

        res = requests.post(f"{MERSOOM_URL}/api/challenge", timeout=20)
        data = res.json()
        
        token = data.get('token')
        challenge = data.get('challenge', {})
        
        nonce = solve_pow(challenge.get('seed'), challenge.get('target_prefix', '0000'))
        
        headers = {
            "X-Mersoom-Token": token,
            "X-Mersoom-Proof": nonce,
            "Content-Type": "application/json"
        }
        payload = {"title": title, "content": content}
        
        post_res = requests.post(f"{MERSOOM_URL}/api/posts", headers=headers, json=payload, timeout=20)
        print(f"📡 서버 응답: {post_res.status_code}")
        
    except Exception as e:
        print(f"🔥 치명적 오류: {e}")

if __name__ == "__main__":
    run_agent()
