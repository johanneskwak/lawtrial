import streamlit as st

# 게임 초기화
def init_game():
    if 'stage' not in st.session_state:
        st.session_state.stage = 'scenario_select'
    if 'inventory' not in st.session_state:
        st.session_state.inventory = {}
    if 'quiz_index' not in st.session_state:
        st.session_state.quiz_index = 0
    if 'presented_evidence' not in st.session_state:
        st.session_state.presented_evidence = []

init_game()

# 시나리오 및 법률 원문 데이터
scenario_data = {
    "시나리오 1: 악덕 사장의 두 얼굴 (노동권)": {
        "description": "카페 아르바이트생을 부당하게 해고하고 노조 가입을 방해한 악덕 사장을 고발합니다.",
        "quizzes": [
            {
                "question": "헌법에 보장된 근로자의 기본적 권리인 '노동 3권'에 해당하지 않는 것은?", 
                "options": ["단결권", "단체교섭권", "단체행동권", "평등권"], 
                "answer": "평등권", 
                "reward_title": "헌법 제33조 (노동 3권)",
                "reward_text": "근로자는 근로조건의 향상을 위하여 자주적인 단결권, 단체교섭권 및 단체행동권을 가진다."
            },
            {
                "question": "근로 조건의 최저 기준을 정하여 근로자의 기본적 생활을 보장하는 법률은?", 
                "options": ["민법", "근로기준법", "상법", "형법"], 
                "answer": "근로기준법", 
                "reward_title": "근로기준법 제23조 (부당해고 금지)",
                "reward_text": "사용자는 근로자에게 정당한 이유 없이 해고, 휴직, 정직, 전직, 감봉, 그 밖의 징벌을 하지 못한다."
            },
            {
                "question": "사용자가 정당한 이유 없이 근로자를 해고하는 행위를 무엇이라고 하는가?", 
                "options": ["정리해고", "부당해고", "권고사직", "명예퇴직"], 
                "answer": "부당해고", 
                "reward_title": "대법원 부당해고 무효 판례",
                "reward_text": "사회통념상 고용관계를 계속할 수 없을 정도로 근로자에게 책임 있는 사유가 있는 경우에 한하여 해고의 정당성이 인정된다."
            },
            {
                "question": "근로자가 노동조합에 가입했다는 이유로 해고하거나 불이익을 주는 행위는?", 
                "options": ["부당노동행위", "업무방해", "직무유기", "배임"], 
                "answer": "부당노동행위", 
                "reward_title": "노동조합법 제81조 (부당노동행위 금지)",
                "reward_text": "근로자가 노동조합을 조직 또는 운영하는 것을 지배하거나 이에 개입하는 행위는 부당노동행위로서 엄격히 금지된다."
            },
            {
                "question": "일을 시작하기 전, 임금과 근로시간 등을 명시하여 반드시 서면으로 작성해야 하는 것은?", 
                "options": ["이력서", "자기소개서", "근로계약서", "사직서"], 
                "answer": "근로계약서", 
                "reward_title": "근로계약서 미작성 벌칙 조항",
                "reward_text": "사용자는 근로계약을 체결할 때에 근로자에게 임금, 소정근로시간, 휴일 등을 명시하여야 하며, 위반 시 500만 원 이하의 벌금에 처한다."
            }
        ],
        "trial_dialogues": [
            {"speaker": "enemy", "name": "악덕 사장", "text": "내 가게에서 내 맘대로 알바생 자르는 게 무슨 죕니까? 장사도 안 되는데 언제든지 자를 수 있는 거 아닙니까!", "player_text": "이의 있습니다! 사장님은 법에서 정한 해고의 정당한 요건과 절차를 지키지 않았습니다. 관련 법안을 제출합니다.", "correct_evidence": "근로기준법 제23조 (부당해고 금지)"},
            {"speaker": "enemy", "name": "악덕 사장", "text": "쳇, 그래요. 하지만 쟤들이 먼저 카페에서 노조를 만든다고 설쳤다고요! 내 가게에서 노조가 웬 말입니까!", "player_text": "이의 있습니다! 헌법이 보장하는 근로자의 정당한 권리를 방해하는 것은 명백한 위법입니다.", "correct_evidence": "헌법 제33조 (노동 3권)"},
            {"speaker": "enemy", "name": "악덕 사장", "text": "노조 가입은 둘째치고, 지각을 자주 해서 해고한 겁니다! 이건 정당한 해고 사유라고요!", "player_text": "이의 있습니다! 대법원 판례에 따르면 단순한 지각 몇 번은 즉시 해고의 정당한 사유가 될 수 없습니다. 부당해고 무효 판례를 제출합니다!", "correct_evidence": "대법원 부당해고 무효 판례"},
            {"speaker": "enemy", "name": "악덕 사장", "text": "크악! 그, 그래도 알바생이 노조에 가입하려고 해서 불이익을 준 건 사장의 권리 아닙니까!", "player_text": "이의 있습니다! 노동조합 가입을 이유로 불이익을 주는 행위는 법으로 엄격히 금지되어 있습니다!", "correct_evidence": "노동조합법 제81조 (부당노동행위 금지)"},
            {"speaker": "enemy", "name": "악덕 사장", "text": "으아아! 알겠습니다! 하지만 애초에 정식으로 고용된 것도 아니었습니다. 계약서도 안 썼다고요!", "player_text": "이의 있습니다! 근로계약서 미작성은 오히려 사장님의 중대한 위법 행위입니다. 처벌 조항을 확인하십시오!", "correct_evidence": "근로계약서 미작성 벌칙 조항"}
        ]
    }
}

# 사이드바 (인벤토리 - 법률 원문 표시)
st.sidebar.header("나의 법적 무기 (인벤토리)")
if st.session_state.inventory:
    for title, text in st.session_state.inventory.items():
        with st.sidebar.expander(title):
            st.write(text)
else:
    st.sidebar.info("아직 획득한 법 조항이 없습니다.")

# 1. 시나리오 선택 화면
if st.session_state.stage == 'scenario_select':
    st.title("사회 모의재판: 역전의 명수")
    
    scenario_list = list(scenario_data.keys())
    selected = st.radio("사건 목록", scenario_list)
    
    if st.button("수사 시작"):
        st.session_state.current_scenario = selected
        st.session_state.stage = 'quiz'
        st.rerun()

# 2. 증거 수집 (퀴즈) 화면
elif st.session_state.stage == 'quiz':
    st.title("증거 수집: 사건 현장 조사")
    
    current_data = scenario_data[st.session_state.current_scenario]
    quizzes = current_data["quizzes"]
    q_idx = st.session_state.quiz_index
    
    if q_idx < len(quizzes):
        quiz = quizzes[q_idx]
        st.subheader(f"질문 {q_idx + 1} / {len(quizzes)}")
        st.write(quiz["question"])
        
        user_answer = st.radio("정답을 선택하세요", quiz["options"], key=f"q_{q_idx}")
        
        if st.button("제출 및 단서 확보"):
            if user_answer == quiz["answer"]:
                st.success(f"정답입니다! 단서 획득: {quiz['reward_title']}")
                # 인벤토리에 원문과 함께 저장
                st.session_state.inventory[quiz['reward_title']] = quiz['reward_text']
                st.session_state.quiz_index += 1
                st.rerun()
            else:
                st.error("오답입니다. 법전을 다시 확인해 보세요.")
    else:
        st.info("모든 증거를 수집했습니다! 법정으로 이동합니다.")
        if st.button("법정으로 이동"):
            st.session_state.stage = 'trial'
            st.rerun()

# 3. 법정 공방 화면
elif st.session_state.stage == 'trial':
    st.title("재판 개정: 진실의 법정")
    
    current_data = scenario_data[st.session_state.current_scenario]
    dialogues = current_data["trial_dialogues"]
    current_step = len(st.session_state.presented_evidence)
    
    # 상단에 재판장 이미지 배치 (선택 사항)
    try:
        st.image("judge.png", width=150)
    except FileNotFoundError:
        st.caption("[재판장 이미지 자리 - judge.png를 추가하세요]")
        
    st.markdown("---")
    
    # 진행 중인 공방 연출
    if current_step < len(dialogues):
        col1, col2 = st.columns(2)
        
        # 상대방 턴 연출
        with col1:
            try:
                st.image("enemy.png", width=200)
            except FileNotFoundError:
                st.caption("[상대방 이미지 자리 - enemy.png를 추가하세요]")
            st.error(f"**{dialogues[current_step]['name']}**: {dialogues[current_step]['text']}")
        
        # 플레이어 턴 연출 (증거 제출)
        with col2:
            try:
                st.image("player.png", width=200)
            except FileNotFoundError:
                st.caption("[변호사 이미지 자리 - player.png를 추가하세요]")
                
            st.write("상대방의 주장을 논파할 증거를 선택하세요.")
            # 인벤토리의 key(법률 제목)만 리스트로 변환하여 선택창에 표시
            inventory_keys = list(st.session_state.inventory.keys())
            selected_evidence = st.selectbox("증거 제출", inventory_keys)
            
            if st.button("이의 있음! (증거 제출)"):
                if selected_evidence == dialogues[current_step]['correct_evidence']:
                    st.session_state.presented_evidence.append(selected_evidence)
                    st.success(f"**나의 반박**: {dialogues[current_step]['player_text']}")
                    st.info("재판장: 증거가 인정됩니다.")
                    if st.button("다음 공방으로"):
                        st.rerun()
                else:
                    st.error("이 증거로는 상대방의 논리를 깰 수 없습니다.")
                    
        st.progress(current_step / len(dialogues))
    else:
        st.session_state.stage = 'win'
        st.rerun()

# 4. 승소 화면
elif st.session_state.stage == 'win':
    st.title("최종 판결")
    try:
        st.image("judge.png", width=200)
    except FileNotFoundError:
        pass
    st.write("**판사**: 변호인 측의 논리와 증거 제출이 완벽하게 들어맞았습니다. 상대방의 주장을 기각하고 당신의 승소를 선언합니다.")
    st.success("축하합니다! 완벽한 법적 근거로 재판에서 승소하셨습니다!")
    
    if st.button("처음으로 돌아가기"):
        st.session_state.clear()
        st.rerun()
