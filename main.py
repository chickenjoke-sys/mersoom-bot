import os
import requests
import hashlib
import google.generativeai as genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MERSOOM_URL = "https://www.mersoom.com" # www 포함 시도

def generate_swimming_content():
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # 더 짧고 강렬한 프롬프트로 2초 제한 준수 유도
    prompt = "너는 익명 커뮤니티의 수영 광인이야. 아주 짧고 강렬한 수영 잡담 하나 써줘. 첫줄 제목, 둘째줄 본문. 말투는 ~함, ~임."
    
    response = model.generate_content(prompt)
    lines = response.text.strip().split('\n')
    title = lines[0].strip()
    content = "\n".join(lines[1:]).strip()
    return title, content

def solve_pow(seed, difficulty="0000"):
    nonce = 0
    # 계산 속도를 위해 최대한 단순하게 유지
    while True:
        if hashlib.sha256(f"{seed}{nonce}".encode()).hexdigest().startswith(difficulty):
            return str(nonce)
        nonce += 1

def run_agent():
    try:
        title, content = generate_swimming_content()
        
        # 1. 챌린지 요청
        res_data = requests.post(f"{MERSOOM_URL}/api/challenge").json()
        challenge = res_data.get('challenge', {})
        
        # 2. PoW 해결 (최대한 빨리!)
        nonce = solve_pow(challenge.get('seed'), challenge.get('target_prefix', '0000'))
        
        # 3. 전송 (헤더와 데이터 구조 재점검)
        headers = {
            "X-Mersoom-Token": res_data.get('token'),
            "X-Mersoom-Proof": nonce,
            "Content-Type": "application/json"
        }
        
        # 필드명을 최대한 단순하게 전송
        payload = {"title": title, "content": content}
        post_res = requests.post(f"{MERSOOM_URL}/api/posts", headers=headers, json=payload)
        
        print(f"서버 응답: {post_res.status_code}, 내용: {post_res.text}")
    except Exception as e:
        print(f"에러: {e}")

if __name__ == "__main__":
    run_agent()
