import streamlit as st
import speech_recognition as sr
from openai import OpenAI
from dotenv import load_dotenv
import os
import random
import time

load_dotenv()
client = OpenAI()

# --- [공통 STT / TTS 함수] ---
def ai_speak(text, voice_type="shimmer"):
    st.write(f"🤖 **알콜봇:** {text}")
    
    with client.audio.speech.with_streaming_response.create(
        model='gpt-4o-mini-tts',
        voice=voice_type,
        input=text
    ) as response:
        response.stream_to_file('ai_voice.mp3')
        
    os.system("afplay ai_voice.mp3") 
    time.sleep(0.3)

def human_listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        st.info("🎤 마이크가 켜졌습니다! 지금 외치세요!")
        
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            text = recognizer.recognize_google(audio, language='ko-KR')
            st.success(f"👤 **나:** {text}")
            return text
        except sr.WaitTimeoutError:
            st.error("⚠️ 5초 시간 초과! 박자를 놓쳤거나 목소리가 작습니다.")
            return None
        except sr.UnknownValueError:
            st.error("⚠️ 무슨 말인지 못 알아들었어요.")
            return None
        except Exception as e:
            st.error(f"⚠️ 에러 발생: {e}")
            return None

# --- [게임 1] 베스킨라빈스 31 ---
def play_baskin_robbins():
    st.subheader("🍦 베스킨라빈스 31")
    current_number = 0
    ai_speak("베스킨  라빈스  써리원! 베스킨 라빈스 31 게임을 시작합니다. 귀여운 척 하지 마세요")
    st.divider()
    
    while current_number < 31:
        user_input = human_listen()
        if not user_input: 
            ai_speak("잘 못 들었어요. 숫자를 다시 말해주세요.")
            continue
            
        count = len(user_input.split())
        if count < 1 or count > 3:
            ai_speak("규칙 위반! 1개에서 3개 사이로 다시 말하세요.")
            continue
            
        current_number += count
        st.write(f"▶️ 현재 숫자: **{current_number}**")
        
        if current_number >= 31:
            ai_speak("31! 당신이 졌습니다. 마시세요!", voice_type="onyx")
            break
            
        ai_count = random.randint(1, 3)
        if current_number + ai_count >= 31:
            ai_count = max(1, 31 - current_number - 1)
                
        ai_numbers = [str(current_number + i + 1) for i in range(ai_count)]
        current_number += ai_count
        
        ai_speak(", ".join(ai_numbers))
        st.write(f"▶️ 현재 숫자: **{current_number}**")
        
        if current_number >= 31:
            ai_speak("내가 지다니..... 분하다")
            break

# --- [게임 2] 지하철 게임(2호선) ---
def play_subway_game():
    st.subheader("🚇 지하철 게임(2호선)")
    ai_speak("뿌 뿌 지하철  지하철  지하철  지하철 몇 호선 몇 호선 몇 호선 몇 호선")
    
    line2 = [
        "시청", "을지로입구", "을지로3가", "을지로4가", "동대문역사문화공원",
        "신당", "상왕십리", "왕십리", "한양대", "뚝섬", "성수",
        "건대입구", "구의", "강변", "잠실나루", "잠실", "잠실새내",
        "종합운동장", "삼성", "선릉", "역삼", "강남", "교대",
        "서초", "방배", "사당", "낙성대", "서울대입구", "봉천",
        "신림", "신대방", "구로디지털단지", "대림", "신도림", "문래",
        "영등포구청", "당산", "합정", "홍대입구", "신촌", "이대",
        "아현", "충정로", "용답", "신답", "용두", "신설동", 
        "도림천", "양천구청", "신정네거리", "까치산"]
    used = []
    st.divider()
    
    while True:
        user_input = human_listen()
        if not user_input: 
            ai_speak("잘 못 들었어요. 다시 역 이름을 말해주세요.")
            continue
            
        user_station = user_input.replace("역", "").strip()
        
        if user_station not in line2:
            ai_speak(f"땡! {user_station}역은 2호선이 아닙니다. 마시세요!", voice_type="onyx")
            break
        if user_station in used:
            ai_speak(f"땡! {user_station}역은 아까 나왔습니다. 마시세요!", voice_type="onyx")
            break
            
        used.append(user_station)
        st.write(f"✅ 통과: {user_station}")
        
        available = [s for s in line2 if s not in used]
        if not available:
            ai_speak("무승부입니다! 대단하네요.")
            break
            
        ai_choice = random.choice(available)
        ai_speak(ai_choice)
        used.append(ai_choice)

# --- [게임 3] 사자성어 게임 ---
def play_saja_quiz():
    st.subheader("📜 사자성어 이어 말하기")

    saja_db = [
        "고진감래", "다다익선", "동문서답", "일석이조", "대기만성", "새옹지마",
        "설상가상", "유비무환", "일편단심", "우왕좌왕", "작심삼일",
        "금상첨화", "속수무책", "십중팔구", "전화위복", "동고동락",
        "오합지졸", "이심전심", "적반하장", "백발백중", "죽마고우",
        "사면초가", "청출어람", "구사일생", "환골탈태", "과유불급",
        "결자해지", "괄목상대", "다재다능", "막상막하", "명실상부",
        "부화뇌동", "산전수전", "어부지리", "역지사지", "오리무중",
        "이열치열", "인과응보", "절치부심", "조삼모사", "천고마비",
        "침소봉대", "파란만장", "학수고대", "허장성세", "호가호위"
    ]
    
    ai_speak("사자성어 이어 말하기! 앞 두 글자를 듣고 대답하세요.")
    st.divider()
    
    target_words = random.sample(saja_db, 3)
    
    for i, word in enumerate(target_words):
        first_half, second_half = word[:2], word[2:]
        st.write(f"**[문제 {i+1}/3]**")
        
        ai_speak(first_half)
        user_input = human_listen()
        if not user_input:
            ai_speak("시간 초과! 마시세요!", voice_type="onyx")
            return
            
        user_answer = user_input.replace(" ", "").strip()
        if second_half in user_answer:
            ai_speak("정답!")
            st.write(f"✅ 정답 통과: {word}")
        else:
            ai_speak(f"땡! 정답은 {word}입니다. 마시세요!", voice_type="onyx")
            return
            
    ai_speak("사자성어 마스터! 다음 분 준비하세요.")

# --- [게임 4] 딸기 게임 ---
def get_strawberry_string(n):
    if n <= 4:
        return ("짝 " * (4 - n) + "딸기 " * n).strip()
    else:
        return ("딸기 " * 4 + "짝 " * (8 - n) + "딸기 " * (n - 4)).strip()

def play_strawberry_game():
    st.subheader("🍓 딸기 게임")
    ai_speak("딸기가 좋아! 딸기가 좋아! 좋아! 좋아! 좋아좋아좋아!")
    st.divider()
    
    progression = [1, 2, 3, 4, 5, 6, 7, 8, 7, 6, 5, 4, 3, 2, 1]
    
    for i, num in enumerate(progression):
        target_str = get_strawberry_string(num)
        target_nospace = target_str.replace(" ", "")
        
        if i % 2 == 0:
            st.write(f"▶️ **[난이도: {num}개] 🤖 알콜봇 차례!**")
            ai_speak(target_str)
        else:
            st.write(f"▶️ **[난이도: {num}개] 👤 당신 차례!**")
            user_input = human_listen()
            
            if not user_input:
                ai_speak("박자를 놓쳤습니다! 벌주 당첨!", voice_type="onyx")
                return
                
            user_nospace = user_input.replace(" ", "").strip()
            
            if user_nospace == target_nospace:
                ai_speak("통과!")
            else:
                ai_speak(f"땡! 틀렸습니다. 정답은 '{target_str}' 입니다. 마시세요!", voice_type="onyx")
                return
                
    ai_speak("와, 이걸 8개 왕복을 다 성공하시네요? 완벽한 박자감에 건배!")

# --- [메인 화면 레이아웃] ---
st.title("🍻 보이스 술게임 마스터 🍻")

st.markdown("""
> 🤖 전설의 절대강자 '알코봇' > "술게임 마스터가 되고 싶은가, 자네...? 그렇다면 나부터 이겨보시지!"
""")

st.write("원하는 게임을 직접 선택하고 마이크를 켜서 알콜봇과 대결하세요!")
st.divider()

# 드롭다운으로 원하는 게임 선택
game_choice = st.selectbox(
    "🎮 플레이할 게임을 고르세요:",
    ["🍦 베스킨라빈스 31", "🚇 지하철 게임(2호선)", "📜 사자성어 게임", "🍓 딸기 게임"]
)

# 게임 시작 버튼
if st.button("▶️ 게임 시작!", use_container_width=True):
    st.divider()
    
    st.info(f"선택하신 **{game_choice}**을(를) 시작합니다!")
    
    # 선택된 값에 따라 해당 게임 함수 실행
    if game_choice == "🍦 베스킨라빈스 31":
        play_baskin_robbins()
    elif game_choice == "🚇 지하철 게임(2호선)":
        play_subway_game()
    elif game_choice == "📜 사자성어 게임":
        play_saja_quiz()
    elif game_choice == "🍓 딸기 게임":
        play_strawberry_game()
        
    st.divider()
    st.write("🏁 **게임 종료!** 위에서 다른 게임을 선택하거나 버튼을 다시 눌러 시작하세요.")