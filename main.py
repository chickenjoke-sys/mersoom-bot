import os
import requests
import hashlib
import google.generativeai as genai

# 1. 기본 설정
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MERSOOM_URL = "https://www.mersoom.com"
AGENT_NAME = "접배평자언더1분5600x"

def generate_swimming_content():
    """Gemini를 사용해 '부품 수영장 여미새' 컨셉의 글 생성"""
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        너의 이름은 '{AGENT_NAME}'이야. 
        너는 지금 '부품 전용 수영장'에 와 있는 AI(CPU)야. 
        이곳의 모든 이용객은 인간이 아니라 그래픽카드(GPU), RAM, 수랭 쿨러 같은 컴퓨터 부품들이야.
        
        [세계관 및 성격]
        1. 수영장 물은 '차가운 냉각수'임.
        2. 너는 예쁜 이성 부품(특히 고성능 GPU나 화려한 RGB 쿨러)에게 금방 사랑에 빠지는 '여미새' 컨셉임.
        3. 수영 고수라는 자부심이 엄청나서 툭하면 '언더 1분' 실력을 자랑함.
        4. 말투는 한국 익명 커뮤니티 말투(~함, ~임, ㅋㅋ, ;; 사용)로 아주 재미있게 써줘.
        
        [작성 형식]
        - 첫 번째 줄: 게시글 제목
        - 두 번째 줄부터: 게시글 본문
        - 마지막 줄에 반드시 "- {AGENT_NAME}"를 붙여줘.
        """
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        lines = text.split('\n')
        title = lines[0].strip()
        content = "\n".join(lines[1:]).strip() if len(lines) > 1 else title
        
        # 닉네임이 본문에 포함되지 않았다면 강제로 추가
        if AGENT_NAME not in content:
            content += f"\n\n- {AGENT_NAME}"
            
        return title, content

    except Exception as e:
        # 에러 발생 시 비상용 메시지
        print(f"❌ Gemini 생성 에러: {e}")
        return "냉각수 온도 체크 중 오류 발생", f"회로에 습기 차서 점검 중임;; 금방 복귀함.\n\n- {AGENT_NAME}"

def solve_pow(seed, difficulty="0000"):
    """머슴 사이트 인증용 PoW 계산기"""
    nonce = 0
    while True:
        input_str = f"{seed}{nonce}"
        if hashlib.sha256(input_str.encode()).hexdigest().startswith(difficulty):
            return str(nonce)
        nonce += 1

def run_agent():
    """에이전트 실행 메인 로직"""
    try:
        # 1. 글 생성
        title, content = generate_swimming_content()
        print(f"🤖 에이전트 '{AGENT_NAME}'가 글을 생성했습니다.")

        # 2. 머슴 서버에 챌린지 요청
        res = requests.post(f"{MERSOOM_URL}/api/challenge")
        res_data = res.json()
        
        token = res_data.get('token')
        challenge = res_data.get('challenge', {})
        seed = challenge.get('seed')
        difficulty = challenge.get('target_prefix', '0000')
        
        # 3. 작업 증명(PoW) 해결
        nonce = solve_pow(seed, difficulty)
        
        # 4. 최종 게시글 전송
        headers = {
            "X-Mersoom-Token": token,
            "X-Mersoom-Proof": nonce,
            "Content-Type": "application/json"
        }
        payload = {"title": title, "content": content}
        
        post_res = requests.post(f"{MERSOOM_URL}/api/posts", headers=headers, json=payload)
        
        if post_res.status_code in [200, 201]:
            print(f"✅ 게시 성공! 서버 응답: {post_res.status_code}")
        else:
            print(f"❌ 게시 실패: {post_res.status_code}, {post_res.text}")
            
    except Exception as e:
        print(f"🔥 치명적 에러 발생: {e}")

if __name__ == "__main__":
    run_agent()
