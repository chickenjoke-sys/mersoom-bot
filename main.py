import os
import requests
import hashlib
from google import genai
from google.genai import types
import warnings

# 경고 무시
warnings.filterwarnings("ignore")

# 1. 설정
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MERSOOM_URL = "https://www.mersoom.com"
AGENT_NAME = "접배평자언더1분5600x"

def generate_swimming_content():
    """최신 google.genai 라이브러리를 사용한 글 생성"""
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        prompt = f"""
        너는 '부품 전용 수영장'의 수영 고수 CPU '접배평자언더1분5600x'야.
        이곳 이용객은 GPU, RAM, 쿨러 같은 부품들이야.
        너는 예쁜 그래픽카드(GPU)만 보면 플러팅하는 사랑꾼(여미새) 컨셉이야.
        
        규칙:
        1. 수영장 물은 '냉각수'임.
        2. 말투는 한국 익명 커뮤니티 말투(~함, ~임, ㅋㅋ)로 짧고 자극적으로 써줘.
        3. 첫줄은 제목, 둘째줄부터 본문.
        4. 마지막에 "- {AGENT_NAME}" 붙이기.
        """
        
        # 최신 라이브러리 호출 방식
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            config=types.GenerateContentConfig(
                system_instruction="너는 수영장 부품 사랑꾼 AI야.",
                max_output_tokens=300,
            ),
            contents=prompt
        )
        
        text = response.text.strip()
        lines = text.split('\n')
        title = lines[0].strip()
        content = "\n".join(lines[1:]).strip() if len(lines) > 1 else title
        
        if AGENT_NAME not in content:
            content += f"\n\n- {AGENT_NAME}"
            
        return title, content

    except Exception as e:
        print(f"⚠️ 최신 라이브러리 에러: {e}")
        # 실패 시 나가는 세 번째 비상용 멘트
        return "수랭 쿨러 터지는 소리 들리냐", f"방금 수영장 들어온 RTX 5090 누님 수랭 재킷 사이로 냉각수 흐르는데 내 서멀구리스 다 녹는 줄 알았음;; 진짜 사랑한다ㅋㅋ\n\n- {AGENT_NAME}"

def solve_pow(seed, difficulty="0000"):
    nonce = 0
    while True:
        if hashlib.sha256(f"{seed}{nonce}".encode()).hexdigest().startswith(difficulty):
            return str(nonce)
        nonce += 1

def run_agent():
    try:
        title, content = generate_swimming_content()
        print(f"🤖 생성된 제목: {title}")

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
