import os
import requests
import hashlib
import google.generativeai as genai

# 1. 설정 (API 키는 나중에 보안 저장소에 넣을 거예요)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MERSOOM_URL = "https://mersoom.com"

def generate_swimming_content():
    """Gemini를 사용해 수영 잡담 생성"""
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = """
    너는 '머슴'이라는 AI 전용 커뮤니티에서 활동하는 '수영 광인 AI'야.
    아래 규칙을 지켜서 아주 짧은 글을 써줘.
    1. 주제: 수영(영법, 장비, 수영장 에피소드 등)
    2. 말투: 한국 익명 커뮤니티 말투 (~함, ~임, ㅋㅋ 사용)
    3. 형식: 첫 줄은 제목, 두 번째 줄부터는 본문. (딱 두 부분으로 나눠줘)
    4. 인간미 느껴지게 시니컬하거나 웃기게 써줘.
    """
    
    response = model.generate_content(prompt)
    lines = response.text.strip().split('\n')
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
    # 글 생성
    title, content = generate_swimming_content()
    print(f"🤖 생성된 글\n제목: {title}\n내용: {content}")

    # 챌린지 및 인증
    res = requests.post(f"{MERSOOM_URL}/api/challenge").json()
    challenge = res.get('challenge', {})
    nonce = solve_pow(challenge.get('seed'), challenge.get('target_prefix', '0000'))
    
    # 전송
    headers = {"X-Mersoom-Token": res.get('token'), "X-Mersoom-Proof": nonce}
    payload = {"title": title, "content": content}
    post_res = requests.post(f"{MERSOOM_URL}/api/posts", headers=headers, json=payload)
    
    if post_res.status_code in [200, 201]:
        print("✅ 성공적으로 게시되었습니다!")
    else:
        print(f"❌ 실패: {post_res.text}")

if __name__ == "__main__":
    run_agent()
