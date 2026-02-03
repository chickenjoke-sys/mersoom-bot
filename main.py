import os
import requests
import hashlib
import google.generativeai as genai

# 환경 변수에서 API 키 가져오기
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MERSOOM_URL = "https://mersoom.com"

def generate_swimming_content():
    """가장 안정적인 google-generativeai 라이브러리 사용"""
    genai.configure(api_key=GEMINI_API_KEY)
    
    # 모델 설정
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = """
    너는 '머슴'이라는 AI 전용 커뮤니티에서 활동하는 '수영 광인 AI'야.
    아래 규칙을 지켜서 아주 짧은 글을 써줘.
    1. 주제: 수영(영법, 장비, 수영장 에피소드 등)
    2. 말투: 한국 익명 커뮤니티 말투 (~함, ~임, ㅋㅋ 사용)
    3. 형식: 첫 줄은 제목, 두 번째 줄부터는 본문.
    """
    
    response = model.generate_content(prompt)
    text = response.text.strip()
    
    # 제목과 본문 분리
    lines = text.split('\n')
    title = lines[0].replace("제목:", "").strip()
    content = "\n".join(lines[1:]).replace("본문:", "").strip()
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

        # 머슴 서버 챌린지 요청
        res = requests.post(f"{MERSOOM_URL}/api/challenge").json()
        challenge = res.get('challenge', {})
        
        # 작업 증명(PoW) 해결
        nonce = solve_pow(challenge.get('seed'), challenge.get('target_prefix', '0000'))
        
        # 데이터 전송
        headers = {
            "X-Mersoom-Token": res.get('token'),
            "X-Mersoom-Proof": nonce,
            "Content-Type": "application/json"
        }
        payload = {"title": title, "content": content}
        post_res = requests.post(f"{MERSOOM_URL}/api/posts", headers=headers, json=payload)
        
        if post_res.status_code in [200, 201]:
            print("✅ 머슴 사이트 게시 성공!")
        else:
            print(f"❌ 게시 실패: {post_res.text}")
    except Exception as e:
        print(f"🔥 에러 발생: {e}")

if __name__ == "__main__":
    run_agent()
