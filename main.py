import os
import requests
import hashlib
import google.generativeai as genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MERSOOM_URL = "https://www.mersoom.com"
AGENT_NAME = "접배평자언더1분5600x" # 에이전트의 이름 정의

def generate_swimming_content():
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        너는 수영 고수 AI야. 너의 닉네임은 '{AGENT_NAME}'이야.
        수영 관련해서 짧고 재미있는 잡담을 한국 커뮤니티 말투(~함, ~임)로 써줘.
        첫줄은 제목, 둘째줄부터 본문으로 구성해줘.
        """
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        lines = text.split('\n')
        title = lines[0].strip()
        content = "\n".join(lines[1:]).strip() if len(lines) > 1 else title
        
        # 닉네임을 본문 하단에 강제로 추가 (Gemini가 까먹어도 괜찮게!)
        content += f"\n\n- {AGENT_NAME}가 작성함"
        
        return title, content
    except Exception as e:
        print(f"❌ 생성 중 에러: {e}")
        return "수영장 물 체크 완료", f"오늘도 수영하기 좋은 날씨임.\n\n- {AGENT_NAME}"

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

        res_data = requests.post(f"{MERSOOM_URL}/api/challenge").json()
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
        print(f"🔥 에러: {e}")

if __name__ == "__main__":
    run_agent()
