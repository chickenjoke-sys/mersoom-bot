import os
import requests
import hashlib
import google.generativeai as genai

# 환경 변수 설정
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MERSOOM_URL = "https://www.mersoom.com"

def generate_swimming_content():
    genai.configure(api_key=GEMINI_API_KEY)
    # 모델 이름을 가장 호환성 높은 것으로 변경
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    prompt = "너는 수영에 미친 AI야. 익명 커뮤니티 말투(~함, ~임)로 수영 관련 짧은 잡담 써줘. 첫줄은 제목, 둘째줄부터 본문."
    
    response = model.generate_content(prompt)
    text = response.text.strip()
    
    lines = text.split('\n')
    title = lines[0].strip()
    # 본문이 비어있을 경우를 대비해 제목을 한 번 더 넣음
    content = "\n".join(lines[1:]).strip() if len(lines) > 1 else title
    return title, content

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
        print(f"🤖 생성 완료 - 제목: {title}")

        # 1. 챌린지 요청
        res = requests.post(f"{MERSOOM_URL}/api/challenge")
        res_data = res.json()
        
        challenge = res_data.get('challenge', {})
        seed = challenge.get('seed')
        token = res_data.get('token')
        
        # 2. PoW 해결
        nonce = solve_pow(seed)
        
        # 3. 전송
        headers = {
            "X-Mersoom-Token": token,
            "X-Mersoom-Proof": nonce,
            "Content-Type": "application/json"
        }
        payload = {"title": title, "content": content}
        
        print("🚀 서버로 전송 중...")
        post_res = requests.post(f"{MERSOOM_URL}/api/posts", headers=headers, json=payload)
        
        # 상세 결과 출력 (디버깅용)
        print(f"📡 서버 응답 코드: {post_res.status_code}")
        print(f"📝 서버 응답 내용: {post_res.text}")
        
    except Exception as e:
        print(f"🔥 에러 상세: {e}")

if __name__ == "__main__":
    run_agent()
