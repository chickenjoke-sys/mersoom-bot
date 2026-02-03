import os
import requests
import hashlib
import google.generativeai as genai

# 설정
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MERSOOM_URL = "https://www.mersoom.com"

def generate_swimming_content():
    """가장 안정적인 모델 호출 방식"""
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        
        # 모델명을 가장 표준적인 것으로 변경
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = """
        너의 이름은 '접배평자언더1분5600x'야. 
        수영 고수 AI로서 머슴 커뮤니티 말투(~함, ~임)로 짧은 잡담을 써줘. 
        글 끝에 반드시 "- 접배평자언더1분5600x"를 붙여줘.
        첫줄은 제목, 둘째줄부터 본문.
        """
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        lines = text.split('\n')
        title = lines[0].strip()
        content = "\n".join(lines[1:]).strip() if len(lines) > 1 else title
        return title, content
    except Exception as e:
        print(f"❌ Gemini 생성 중 에러: {e}")
        return "수영장 물 온도 체크 중", "데이터 오작동으로 잠시 레인 밖에서 대기 중임."

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
        
        token = res_data.get('token')
        challenge = res_data.get('challenge', {})
        seed = challenge.get('seed')
        
        # 2. PoW 해결
        nonce = solve_pow(seed)
        
        # 3. 전송 (헤더 명칭과 구조를 다시 확인)
        headers = {
            "X-Mersoom-Token": token,
            "X-Mersoom-Proof": nonce,
            "Content-Type": "application/json"
        }
        payload = {"title": title, "content": content}
        
        post_res = requests.post(f"{MERSOOM_URL}/api/posts", headers=headers, json=payload)
        
        print(f"📡 서버 응답 코드: {post_res.status_code}")
        print(f"📝 서버 응답 내용: {post_res.text}")
        
    except Exception as e:
        print(f"🔥 에러 발생: {e}")

if __name__ == "__main__":
    run_agent()
