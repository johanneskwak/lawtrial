import streamlit as st

# 게임 초기화
def init_game():
    if 'stage' not in st.session_state:
        st.session_state.stage = 'scenario_select'
    if 'inventory' not in st.session_state:
        st.session_state.inventory = []
    if 'quiz_index' not in st.session_state:
        st.session_state.quiz_index = 0
    if 'presented_evidence' not in st.session_state:
        st.session_state.presented_evidence = []

init_game()

# 전체 시나리오 데이터 통합
scenario_data = {
    "시나리오 1: 악덕 사장의 두 얼굴 (노동권)": {
        "description": "카페 아르바이트생을 부당하게 해고하고 노조 가입을 방해한 악덕 사장을 고발합니다.",
        "quizzes": [
            {"question": "헌법에 보장된 근로자의 기본적 권리인 '노동 3권'에 해당하지 않는 것은?", "options": ["단결권", "단체교섭권", "단체행동권", "평등권"], "answer": "평등권", "reward": "헌법 제33조 (노동 3권)"},
            {"question": "근로 조건의 최저 기준을 정하여 근로자의 기본적 생활을 보장하는 법률은?", "options": ["민법", "근로기준법", "상법", "형법"], "answer": "근로기준법", "reward": "근로기준법 제23조 (부당해고 금지)"},
            {"question": "사용자가 정당한 이유 없이 근로자를 해고하는 행위를 무엇이라고 하는가?", "options": ["정리해고", "부당해고", "권고사직", "명예퇴직"], "answer": "부당해고", "reward": "대법원 부당해고 무효 판례"},
            {"question": "근로자가 노동조합에 가입했다는 이유로 해고하거나 불이익을 주는 행위는?", "options": ["부당노동행위", "업무방해", "직무유기", "배임"], "answer": "부당노동행위", "reward": "노동조합법 제81조 (부당노동행위 금지)"},
            {"question": "일을 시작하기 전, 임금과 근로시간 등을 명시하여 반드시 서면으로 작성해야 하는 것은?", "options": ["이력서", "자기소개서", "근로계약서", "사직서"], "answer": "근로계약서", "reward": "근로계약서 미작성 벌칙 조항"}
        ],
        "trial_dialogues": [
            {"enemy": "내 가게에서 내 맘대로 알바생 자르는 게 무슨 죕니까? 장사도 안 되는데 언제든지 자를 수 있는 거 아닙니까!", "player": "이의 있습니다! 사장님은 법에서 정한 해고의 정당한 요건과 절차를 지키지 않았습니다. 관련 법안을 제출합니다.", "correct_evidence": "근로기준법 제23조 (부당해고 금지)"},
            {"enemy": "쳇, 그래요. 하지만 쟤들이 먼저 카페에서 노조를 만든다고 설쳤다고요! 내 가게에서 노조가 웬 말입니까!", "player": "이의 있습니다! 헌법이 보장하는 근로자의 정당한 권리를 방해하는 것은 명백한 위법입니다.", "correct_evidence": "헌법 제33조 (노동 3권)"},
            {"enemy": "노조 가입은 둘째치고, 지각을 자주 해서 해고한 겁니다! 이건 정당한 해고 사유라고요!", "player": "이의 있습니다! 대법원 판례에 따르면 단순한 지각 몇 번은 즉시 해고의 정당한 사유가 될 수 없습니다. 부당해고 무효 판례를 제출합니다!", "correct_evidence": "대법원 부당해고 무효 판례"},
            {"enemy": "크악! 그, 그래도 알바생이 노조에 가입하려고 해서 불이익을 준 건 사장의 권리 아닙니까!", "player": "이의 있습니다! 노동조합 가입을 이유로 불이익을 주는 행위는 법으로 엄격히 금지되어 있습니다!", "correct_evidence": "노동조합법 제81조 (부당노동행위 금지)"},
            {"enemy": "으아아! 알겠습니다! 하지만 애초에 정식으로 고용된 것도 아니었습니다. 계약서도 안 썼다고요!", "player": "이의 있습니다! 근로계약서 미작성은 오히려 사장님의 중대한 위법 행위입니다. 처벌 조항을 확인하십시오!", "correct_evidence": "근로계약서 미작성 벌칙 조항"}
        ]
    },
    "시나리오 2: 음주운전 과실치사 (형사법)": {
        "description": "만취 상태로 운전하다 보행자를 사망에 이르게 하고도 책임을 회피하는 피고인을 단죄하십시오.",
        "quizzes": [
            {"question": "음주측정 결과나 현장 영상과 같이, 범죄 사실을 객관적으로 증명할 수 있는 자료를 무엇이라고 합니까?", "options": ["증명서", "증거", "판례", "영장"], "answer": "증거", "reward": "혈중알코올농도 0.18% 감정서"},
            {"question": "자신의 행위가 위법함을 알면서도 범죄를 저지른 것에 대해 법적으로 비난할 수 있는 상태를 뜻하는 말은?", "options": ["위법성", "구성요건", "책임", "정당방위"], "answer": "책임", "reward": "형법 제10조 제3항 (고의적 심신장애 유발)"},
            {"question": "경찰이 피의자를 체포할 때 범죄 사실의 요지, 변호인 선임권 등을 미리 알려주어야 하는 원칙은?", "options": ["무죄 추정의 원칙", "미란다 원칙", "일사부재리의 원칙", "죄형법정주의"], "answer": "미란다 원칙", "reward": "적법절차 준수 수사보고서"},
            {"question": "음주운전으로 사람을 다치게 하거나 사망에 이르게 한 경우 처벌을 대폭 강화하기 위해 제정된 법률은?", "options": ["도로교통법", "특가법", "민법", "경범죄처벌법"], "answer": "특가법", "reward": "특가법 제5조의11 (위험운전치사상)"},
            {"question": "모든 국민은 인간으로서의 존엄과 가치를 가지며, 국가는 이를 보장할 의무가 있다고 명시한 규범은?", "options": ["형법 제1조", "헌법 제10조", "민법 제1조", "근로기준법 제1조"], "answer": "헌법 제10조", "reward": "헌법 제10조 (인간의 존엄과 가치)"}
        ],
        "trial_dialogues": [
            {"enemy": "피고인: 판사님, 전 억울합니다! 회식에서 술을 너무 많이 마셔서 제가 운전대를 잡았는지조차 기억이 안 납니다. 심신상실 상태였다고요!", "player": "이의 있습니다! 형법에 따라, 위험 발생을 예견하고 자의로 심신장애를 유발한 자는 처벌을 피할 수 없습니다!", "correct_evidence": "형법 제10조 제3항 (고의적 심신장애 유발)"},
            {"enemy": "변호사: 큭...! 피고인이 이성을 잃을 정도로 만취했다는 객관적인 증거가 있습니까? 정황 진술뿐 아닙니까!", "player": "이의 있습니다! 사건 직후 확인된 과학적이고 명백한 증거 자료를 제출합니다. 면허 취소 수준을 아득히 넘겼습니다!", "correct_evidence": "혈중알코올농도 0.18% 감정서"},
            {"enemy": "피고인: 앗...! 그, 그건 경찰이 저를 강제로 끌고 가서 피를 뽑은 겁니다! 명백한 불법 수집 증거입니다!", "player": "이의 있습니다! 당시 경찰은 헌법에 명시된 피의자의 권리를 정확히 고지하고 절차를 지켰습니다. 공식 문서를 제출합니다!", "correct_evidence": "적법절차 준수 수사보고서"},
            {"enemy": "변호사: 크아악! 설사 그렇다 해도 살인의 고의는 없었습니다. 일반 교통사고처럼 과실치사로 처벌받아야 합니다!", "player": "이의 있습니다! 음주운전 사망 사고는 더 이상 단순 과실이 아닙니다. 엄격한 가중처벌 대상임을 증명하는 법률 조항을 제출합니다!", "correct_evidence": "특가법 제5조의11 (위험운전치사상)"},
            {"enemy": "피고인: 으아아아! 한 번의 실수였습니다! 저도 살아야 하지 않겠습니까! 저까지 감옥에서 평생을 썩어야 한단 말입니까!", "player": "이의 있습니다! 당신의 행동 때문에 누군가의 하나뿐인 생명이 사라졌습니다. 피해자의 존엄성을 짓밟은 죄, 절대 가벼울 수 없습니다!", "correct_evidence": "헌법 제10조 (인간의 존엄과 가치)"}
        ]
    },
    "시나리오 3: 학교폭력 사건 (소년법 및 불법행위 책임)": {
        "description": "동급생을 지속적으로 괴롭혀 비극적인 결과에 이르게 한 가해 학생들의 형사적, 민사적 책임을 묻습니다.",
        "quizzes": [
            {"question": "학교 내외에서 학생을 대상으로 발생하는 신체적, 정신적, 재산상 피해를 수반하는 행위를 무엇이라 하는가?", "options": ["명예훼손", "학교폭력", "특수폭행", "협박"], "answer": "학교폭력", "reward": "학교폭력예방 및 대책에 관한 법률"},
            {"question": "형벌의 대상이 되는 범죄를 저지른 만 14세 이상 만 19세 미만의 청소년을 무엇이라 하는가?", "options": ["촉법소년", "우범소년", "범죄소년", "보호소년"], "answer": "범죄소년", "reward": "형법 제9조 형사미성년자 연령 기준"},
            {"question": "다른 사람에게 고의 또는 과실로 위법하게 손해를 입힌 자가 그 손해를 물어주어야 하는 민사상 책임은?", "options": ["연대책임", "무과실책임", "불법행위로 인한 손해배상", "채무불이행"], "answer": "불법행위로 인한 손해배상", "reward": "민법 제750조 불법행위책임"},
            {"question": "미성년자가 타인에게 손해를 입혔을 때, 그 미성년자를 감독할 법정 의무가 있는 부모 등이 대신 지는 책임은?", "options": ["사용자 배상책임", "공작물 점유자 책임", "특수불법행위책임(감독자 책임)", "동물 점유자 책임"], "answer": "특수불법행위책임(감독자 책임)", "reward": "민법 제755조 감독자의 책임"},
            {"question": "정보통신망을 이용하여 사이버 공간에서 타인을 끈질기게 괴롭히거나 따돌리는 행위를 일컫는 말은?", "options": ["사이버 불링", "스미싱", "파밍", "보이스피싱"], "answer": "사이버 불링", "reward": "사이버 명예훼손 및 모욕죄 캡처본"}
        ],
        "trial_dialogues": [
            {"enemy": "가해 학생: 장난으로 몇 번 툭툭 친 것뿐이에요. 걔가 그렇게 예민하게 반응할 줄 몰랐다고요! 그게 무슨 범죄입니까?", "player": "이의 있습니다! 장난을 넘어선 지속적인 신체적, 정신적 괴롭힘은 명백한 학교폭력이자 범죄입니다.", "correct_evidence": "학교폭력예방 및 대책에 관한 법률"},
            {"enemy": "가해 학생: 온, 온라인 단톡방에서 우리끼리 좀 놀린 게 무슨 상관이에요! 직접 때린 것도 아닌데!", "player": "이의 있습니다! 단톡방에서 집단으로 언어폭력을 가하고 따돌린 명백한 증거가 여기 있습니다!", "correct_evidence": "사이버 명예훼손 및 모욕죄 캡처본"},
            {"enemy": "변호사: 피고인들은 아직 어린 학생들입니다. 처벌받기엔 어리지 않습니까? 형사 처벌이 아닌 보호처분만 받아야 합니다!", "player": "이의 있습니다! 피고인들은 범행 당시 이미 만 14세를 넘었으므로 엄연한 형사 처벌의 대상이 됩니다!", "correct_evidence": "형법 제9조 형사미성년자 연령 기준"},
            {"enemy": "가해자 부모: 우리 애가 잘못한 건 맞지만, 왜 부모인 우리한테까지 수천만 원을 물어내라고 하는 겁니까! 우린 때리지 않았어요!", "player": "이의 있습니다! 미성년 자녀가 타인에게 심각한 손해를 입혔다면 감독 의무가 있는 부모에게도 연대 배상 책임이 있습니다!", "correct_evidence": "민법 제755조 감독자의 책임"},
            {"enemy": "가해 학생: 크윽... 하지만... 이미 끝난 일이잖아요. 이제 와서 우리가 벌을 받는다고 죽은 애가 살아 돌아오기라도 합니까!", "player": "이의 있습니다! 당신들의 불법행위로 인해 한 생명이 사라졌습니다. 평생 그 죄의 무게를 짊어지고 책임져야 합니다!", "correct_evidence": "민법 제750조 불법행위책임"}
        ]
    },
    "시나리오 4: 부동산 계약 파기 (민법과 계약)": {
        "description": "아파트 매매 계약 후 매수인이 계약금까지 지불했는데, 매도인이 집값이 올랐다며 일방적으로 계약을 파기했습니다.",
        "quizzes": [
            {"question": "일정한 법률 효과의 발생을 목적으로 하는 당사자 간의 의사표시의 합치를 무엇이라고 하는가?", "options": ["청약", "승낙", "계약", "취소"], "answer": "계약", "reward": "매매계약서 원본"},
            {"question": "계약을 체결할 때, 그 증거로서 당사자 일방이 상대방에게 교부하는 금전 등을 무엇이라고 하는가?", "options": ["보증금", "계약금", "중도금", "잔금"], "answer": "계약금", "reward": "계약금 이체 영수증"},
            {"question": "부동산 거래 시, 계약금만 지급한 상태에서 매도인이 일방적으로 계약을 해제하려면 계약금의 얼마를 상환해야 하는가?", "options": ["원금", "1.5배", "배액(2배)", "3배"], "answer": "배액(2배)", "reward": "민법 제565조 해약금 조항"},
            {"question": "당사자 일방이 정당한 이유 없이 계약 내용을 약속대로 이행하지 않는 것을 무엇이라고 하는가?", "options": ["채무불이행", "불법행위", "부당이득", "사기"], "answer": "채무불이행", "reward": "채무불이행 사실 확인서"},
            {"question": "계약 당사자 사이에 계약금을 위약금으로 하기로 하는 특약이 있는 경우, 이 계약금의 성질은 무엇으로 추정되는가?", "options": ["해약금", "증약금", "손해배상액의 예정", "부당이득"], "answer": "손해배상액의 예정", "reward": "위약금 특약 조항"}
        ],
        "trial_dialogues": [
            {"enemy": "매도인: 아니, 내 집 내가 안 팔겠다는데 무슨 상관입니까! 하루 만에 집값이 1억이 올랐는데 미쳤다고 그 가격에 팝니까? 없던 일로 합시다!", "player": "이의 있습니다! 양 당사자의 서명과 도장이 찍힌 순간부터 법적인 효력이 발생했습니다. 일방적인 취소는 불가능합니다!", "correct_evidence": "매매계약서 원본"},
            {"enemy": "매도인: 콧방귀도 안 뀌어지네요. 도장만 찍었지 아직 잔금도 안 치렀잖아요! 내가 받은 돈만 딱 돌려주면 끝나는 거 아닙니까!", "player": "이의 있습니다! 매수인 측에서 이미 초기 금액을 입금하여 계약이 정상적인 이행 단계에 착수했습니다.", "correct_evidence": "계약금 이체 영수증"},
            {"enemy": "매도인: 흥! 그래봤자 계약금일 뿐입니다. 그냥 그 계약금 원금 5천만 원만 계좌로 다시 쏴줄 테니 당장 떨어지쇼!", "player": "이의 있습니다! 법에 따르면 매도인이 일방적으로 파기할 경우 원금이 아니라 배액(2배)을 상환해야 합니다!", "correct_evidence": "민법 제565조 해약금 조항"},
            {"enemy": "매도인 측 변호사: 피고가 집을 넘기지 않은 것은 일시적인 착오일 뿐, 의도적인 계약 위반은 아닙니다. 거액의 배상 청구는 너무 과합니다!", "player": "이의 있습니다! 약속한 날짜에 소유권을 이전하지 않은 것은 명백한 채무불이행이며 법적 의무 위반입니다!", "correct_evidence": "채무불이행 사실 확인서"},
            {"enemy": "매도인: 크악...! 줘, 주면 될 거 아뇨! 2배 돌려주면 되잖아! 근데 거기에 추가로 계약서상의 위약금까지 달라는 건 완전 도둑놈 심보 아닙니까!", "player": "이의 있습니다! 작성하신 계약서 특약 조항에 따라, 계약 파기 시 당신은 정당한 손해배상액을 지불해야 할 법적 의무가 있습니다!", "correct_evidence": "위약금 특약 조항"}
        ]
    }
}

# 사이드바 (인벤토리)
st.sidebar.header("나의 법적 무기 (인벤토리)")
if st.session_state.inventory:
    for item in st.session_state.inventory:
        st.sidebar.success(item)
else:
    st.sidebar.info("아직 획득한 증거가 없습니다.")

# 1. 시나리오 선택 화면
if st.session_state.stage == 'scenario_select':
    st.title("사회 모의재판: 역전의 명수 ⚖️")
    st.write("해결하고자 하는 사건 시나리오를 선택하세요.")
    
    scenario_list = list(scenario_data.keys())
    selected = st.radio("사건 목록", scenario_list)
    
    if st.button("수사 시작"):
        st.session_state.current_scenario = selected
        st.session_state.stage = 'quiz'
        st.rerun()

# 2. 증거 수집 (퀴즈) 화면
elif st.session_state.stage == 'quiz':
    st.title("증거 수집: 사건 현장 조사 🔍")
    st.write("재판에 필요한 법 조항과 증거를 모으기 위해 퀴즈를 풀어야 합니다.")
    
    current_data = scenario_data[st.session_state.current_scenario]
    quizzes = current_data["quizzes"]
    q_idx = st.session_state.quiz_index
    
    if q_idx < len(quizzes):
        quiz = quizzes[q_idx]
        st.subheader(f"질문 {q_idx + 1} / 5")
        st.write(quiz["question"])
        
        user_answer = st.radio("정답을 선택하세요", quiz["options"], key=f"q_{q_idx}")
        
        if st.button("제출 및 단서 확보"):
            if user_answer == quiz["answer"]:
                st.success(f"정답입니다! 획득: **{quiz['reward']}**")
                if quiz["reward"] not in st.session_state.inventory:
                    st.session_state.inventory.append(quiz["reward"])
                st.session_state.quiz_index += 1
                st.rerun()
            else:
                st.error("오답입니다. 법전을 다시 확인해 보세요.")
    else:
        st.info("모든 증거를 수집했습니다! 이제 진실의 법정으로 이동합니다.")
        if st.button("법정으로 이동"):
            st.session_state.stage = 'trial'
            st.rerun()

# 3. 법정 공방 화면
elif st.session_state.stage == 'trial':
    st.title("재판 개정: 진실의 법정 🏛️")
    st.subheader(st.session_state.current_scenario)
    
    current_data = scenario_data[st.session_state.current_scenario]
    dialogues = current_data["trial_dialogues"]
    current_step = len(st.session_state.presented_evidence)
    
    # 이전 공방 기록 출력
    for i in range(current_step):
        st.error(f"**상대방**: {dialogues[i]['enemy']}")
        st.info(f"**나의 반박**: {dialogues[i]['player']}")
        st.success(f"제출된 증거 👉 {dialogues[i]['correct_evidence']}")
        st.markdown("---")
    
    # 현재 진행 중인 공방
    if current_step < len(dialogues):
        st.subheader("상대방의 주장")
        st.error(f"**상대방**: {dialogues[current_step]['enemy']}")
        
        st.write("상대방의 논리를 깨뜨릴 정확한 증거를 인벤토리에서 선택하세요.")
        selected_evidence = st.selectbox("증거 제출", st.session_state.inventory)
        
        if st.button("이의 있음! (증거 제출)"):
            if selected_evidence == dialogues[current_step]['correct_evidence']:
                st.session_state.presented_evidence.append(selected_evidence)
                st.success("효과적인 증거입니다! 상대방의 주장을 완벽하게 논파했습니다.")
                st.rerun()
            else:
                st.error("이 증거로는 상대방의 논리를 깰 수 없습니다. 상황에 맞는 다른 증거를 찾아보세요.")
                
        st.progress(current_step / 5.0)
    else:
        st.session_state.stage = 'win'
        st.rerun()

# 4. 승소 화면
elif st.session_state.stage == 'win':
    st.title("최종 판결 ⚖️")
    st.write("**판사**: 변호인(또는 검사) 측의 논리와 증거 제출이 완벽하게 들어맞았습니다. 상대방의 주장을 기각하고 당신의 승소를 선언합니다.")
    st.success("🎉 축하합니다! 완벽한 법적 근거로 재판에서 승소하셨습니다! 🎉")
    st.balloons()
    
    if st.button("처음으로 돌아가기"):
        st.session_state.clear()
        st.rerun()