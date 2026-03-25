import random
import streamlit as st

st.set_page_config(page_title="사회 모의재판: 역전의 명수", page_icon="⚖️", layout="wide")

# =========================================================
# 0. 게임 초기화 / 리셋
# =========================================================
def init_game():
    defaults = {
        "stage": "scenario_select",
        "inventory": {},
        "quiz_index": 0,
        "presented_evidence": [],
        "lives": 3,
        "current_scenario": "",
        "score": 0,
        "combo": 0,
        "max_combo": 0,
        "hint_count": 2,
        "used_hints": 0,
        "trust": 100,
        "bonus_evidence": [],
        "badges": [],
        "ending_type": "",
        "court_index": 0,
        "pressed_mode": False,
        "last_result": "",
        "current_hint": "",
        "current_quiz_feedback": "",
        "current_trial_feedback": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_game():
    keys_to_reset = {
        "stage": "scenario_select",
        "inventory": {},
        "quiz_index": 0,
        "presented_evidence": [],
        "lives": 3,
        "current_scenario": "",
        "score": 0,
        "combo": 0,
        "max_combo": 0,
        "hint_count": 2,
        "used_hints": 0,
        "trust": 100,
        "bonus_evidence": [],
        "badges": [],
        "ending_type": "",
        "court_index": 0,
        "pressed_mode": False,
        "last_result": "",
        "current_hint": "",
        "current_quiz_feedback": "",
        "current_trial_feedback": "",
    }
    for key, value in keys_to_reset.items():
        st.session_state[key] = value


init_game()

# =========================================================
# 1. 보조 함수
# =========================================================
def handle_correct(base_score=10):
    st.session_state.combo += 1
    st.session_state.max_combo = max(st.session_state.max_combo, st.session_state.combo)
    combo_bonus = min(st.session_state.combo * 2, 10)
    st.session_state.score += base_score + combo_bonus
    st.session_state.last_result = "correct"


def handle_wrong(life_penalty=1, trust_penalty=10):
    st.session_state.combo = 0
    st.session_state.lives -= life_penalty
    st.session_state.trust = max(0, st.session_state.trust - trust_penalty)
    st.session_state.last_result = "wrong"


def calculate_grade():
    score = st.session_state.score
    lives = st.session_state.lives
    trust = st.session_state.trust
    hints = st.session_state.used_hints

    if score >= 180 and lives == 3 and trust >= 80 and hints == 0:
        return "S"
    elif score >= 140 and trust >= 60:
        return "A"
    elif score >= 100:
        return "B"
    elif score >= 60:
        return "C"
    return "D"


def determine_ending():
    score = st.session_state.score
    lives = st.session_state.lives
    trust = st.session_state.trust
    hints = st.session_state.used_hints

    if score >= 180 and lives == 3 and trust >= 80 and hints == 0:
        return "완전 승소 엔딩"
    elif trust >= 70 and score >= 130:
        return "정의 실현 엔딩"
    elif trust >= 50 and score >= 90:
        return "간신히 승소 엔딩"
    elif hints >= 2 and score >= 80:
        return "고군분투 승소 엔딩"
    return "증거 불충분 속 힘겨운 승소 엔딩"


def assign_badges():
    badges = []

    if st.session_state.used_hints == 0:
        badges.append("🧠 추리 천재")
    if st.session_state.max_combo >= 5:
        badges.append("🔥 완벽 반박러")
    if len(st.session_state.bonus_evidence) >= 2:
        badges.append("🕵️ 숨은 증거 수집가")
    if st.session_state.lives == 3:
        badges.append("💎 퍼펙트 변론가")
    if st.session_state.trust >= 90:
        badges.append("⚖️ 법정의 신뢰")
    if st.session_state.score >= 180:
        badges.append("🏆 역전의 명수")

    st.session_state.badges = badges


def get_quiz_hint(quiz):
    answer = quiz["answer"]
    return f"힌트: 정답은 **'{answer[0]}'**(으)로 시작합니다."


def get_trial_hint(dialogue):
    ev = dialogue["correct_evidence"]
    short_name = ev[:10] + ("..." if len(ev) > 10 else "")
    return f"힌트: 지금 필요한 증거는 **'{short_name}'** 와 관련된 자료입니다."


bonus_evidence_pool = [
    {
        "title": "CCTV 추가 캡처본",
        "text": "사건 당시 현장을 더 선명하게 보여주는 보조 자료. 최종 점수 보너스에 반영된다."
    },
    {
        "title": "증인 진술서",
        "text": "상대방 진술의 신빙성을 약화시키는 보조 자료. 반박 성공 시 점수 보너스."
    },
    {
        "title": "메신저 대화 캡처",
        "text": "상대 주장과 모순되는 대화 기록. 숨겨진 보조 증거로 사용된다."
    }
]


def try_get_bonus_evidence():
    if random.random() < 0.30:
        bonus = random.choice(bonus_evidence_pool)
        if bonus["title"] not in st.session_state.inventory:
            st.session_state.inventory[bonus["title"]] = bonus["text"]
            st.session_state.bonus_evidence.append(bonus["title"])
            st.session_state.score += 10
            st.success(f"🎁 숨겨진 증거 발견: **{bonus['title']}**")


def get_bonus_score_from_inventory():
    bonus_count = len(st.session_state.bonus_evidence)
    return min(bonus_count * 3, 15)


def check_game_over():
    if st.session_state.lives <= 0 or st.session_state.trust <= 0:
        st.session_state.stage = "game_over"
        return True
    return False


# =========================================================
# 2. 시나리오 데이터
# =========================================================
scenario_data = {
    "시나리오 1: 악덕 사장의 두 얼굴 (노동권 보호)": {
        "description": "카페 아르바이트생을 부당하게 해고하고 노조 가입을 방해한 악덕 사장을 고발합니다.",
        "quizzes": [
            {
                "question": "헌법에 보장된 근로자의 기본적 권리인 '노동 3권'에 해당하지 않는 것은?",
                "options": ["단결권", "단체교섭권", "단체행동권", "평등권"],
                "answer": "평등권",
                "reward_title": "헌법 제33조 (노동 3권)",
                "reward_text": "① 근로자는 근로조건의 향상을 위하여 자주적인 단결권·단체교섭권 및 단체행동권을 가진다.\n② 공무원인 근로자는 법률이 정하는 자에 한하여 단결권·단체교섭권 및 단체행동권을 가진다."
            },
            {
                "question": "근로 조건의 최저 기준을 정하여 근로자의 기본적 생활을 보장하는 법률은?",
                "options": ["민법", "근로기준법", "상법", "형법"],
                "answer": "근로기준법",
                "reward_title": "근로기준법 제23조 (해고 등의 제한)",
                "reward_text": "① 사용자는 근로자에게 정당한 이유 없이 해고, 휴직, 정직, 전직, 감봉, 그 밖의 징벌(이하 '부당해고등')을 하지 못한다."
            },
            {
                "question": "단순한 지각 몇 번을 이유로 해고하는 등, 정당한 이유 없는 해고를 무효로 보는 기준은 무엇인가?",
                "options": ["업무상 과실", "부당해고", "직장 내 괴롭힘", "임금체불"],
                "answer": "부당해고",
                "reward_title": "대법원 부당해고 무효 판례 (2001다...)",
                "reward_text": "[대법원 판례] 해고는 사회통념상 고용관계를 계속할 수 없을 정도로 근로자에게 책임 있는 사유가 있는 경우에 행하여져야 하며, 단순한 몇 차례의 지각만으로는 징계해고 사유로 삼기 어렵다."
            },
            {
                "question": "근로자가 노동조합에 가입했다는 이유로 불이익을 주는 사용자의 위법 행위는?",
                "options": ["부당노동행위", "업무방해", "배임", "직무유기"],
                "answer": "부당노동행위",
                "reward_title": "노동조합법 제81조 (부당노동행위)",
                "reward_text": "사용자는 근로자가 노동조합에 가입 또는 가입하려고 하였음을 이유로 불이익을 주는 행위를 할 수 없다."
            },
            {
                "question": "근로 관계 성립 시 임금, 근로시간 등을 서면으로 명시해야 하는 문서는?",
                "options": ["이력서", "근로계약서", "사직서", "취업규칙"],
                "answer": "근로계약서",
                "reward_title": "근로기준법 제17조 (근로조건의 명시)",
                "reward_text": "① 사용자는 근로계약을 체결할 때 근로자에게 임금, 소정근로시간, 휴일, 연차 유급휴가 등을 명시하여야 한다."
            }
        ],
        "trial_dialogues": [
            {
                "speaker": "enemy",
                "name": "악덕 사장",
                "text": "내 가게에서 내 맘대로 알바생 자르는 게 무슨 죕니까! 언제든지 자를 수 있는 거 아닙니까!",
                "press_text": "사장: 내 가게 운영은 내 자유 아닙니까? 직원 하나 자르는 것도 마음대로 못합니까?",
                "player_text": "이의 있습니다! 사장님은 법에서 정한 해고의 정당한 요건과 절차를 지키지 않았습니다. 관련 법안을 제출합니다.",
                "correct_evidence": "근로기준법 제23조 (해고 등의 제한)"
            },
            {
                "speaker": "enemy",
                "name": "악덕 사장",
                "text": "쳇... 하지만 쟤들이 먼저 카페에서 노조를 만든다고 설쳤다고요! 내 가게에서 노조가 웬 말입니까!",
                "press_text": "사장: 사장이 싫다는데도 노조를 만들겠다고 하면 질서가 무너지지 않겠습니까?",
                "player_text": "이의 있습니다! 헌법이 보장하는 근로자의 정당한 권리를 방해하는 것은 명백한 헌법 위반입니다.",
                "correct_evidence": "헌법 제33조 (노동 3권)"
            },
            {
                "speaker": "enemy",
                "name": "악덕 사장",
                "text": "노조 가입은 둘째치고, 지각을 자주 해서 해고한 겁니다! 이건 정당한 해고 사유라고요!",
                "press_text": "사장: 몇 번 지각했으면 사장 입장에선 신뢰가 깨진 거죠. 해고할 만하지 않습니까?",
                "player_text": "이의 있습니다! 대법원 판례에 따르면 단순한 지각 몇 번은 즉시 해고의 정당한 사유가 될 수 없습니다!",
                "correct_evidence": "대법원 부당해고 무효 판례 (2001다...)"
            },
            {
                "speaker": "enemy",
                "name": "악덕 사장",
                "text": "크악! 그, 그래도 노조에 가입하려고 해서 불이익을 준 건 사장의 권리 아닙니까!",
                "press_text": "사장: 사장이 마음에 들지 않는 직원을 구분해서 대우하는 것도 경영 판단 아닌가요?",
                "player_text": "이의 있습니다! 노동조합 가입을 이유로 불이익을 주는 행위는 법으로 엄격히 금지된 '부당노동행위'입니다!",
                "correct_evidence": "노동조합법 제81조 (부당노동행위)"
            },
            {
                "speaker": "enemy",
                "name": "악덕 사장",
                "text": "으아아! 하지만 애초에 정식으로 고용된 것도 아니었습니다. 계약서도 안 썼다고요!",
                "press_text": "사장: 계약서가 없으면 정식 고용이 아니라는 뜻 아닙니까? 그래서 문제도 없는 겁니다!",
                "player_text": "이의 있습니다! 근로계약서 미작성은 오히려 사장님의 중대한 위법 행위입니다. 처벌 조항을 확인하십시오!",
                "correct_evidence": "근로기준법 제17조 (근로조건의 명시)"
            }
        ]
    },

    "시나리오 2: 음주운전 과실치사 (형사법과 헌법)": {
        "description": "만취 상태로 운전하다 보행자를 사망에 이르게 하고도 심신상실을 주장하며 책임을 회피하는 피고인을 단죄하십시오.",
        "quizzes": [
            {
                "question": "스스로 술을 마셔 심신장애를 유발하고 범죄를 저지른 경우, 형을 감경받을 수 없도록 규정한 원칙은?",
                "options": ["원인에 있어서 자유로운 행위", "일사부재리의 원칙", "무죄 추정의 원칙", "정당방위"],
                "answer": "원인에 있어서 자유로운 행위",
                "reward_title": "형법 제10조 제3항",
                "reward_text": "③ 위험의 발생을 예견하고 자의로 심신장애를 야기한 자의 행위에는 심신장애 감면 규정을 적용하지 아니한다."
            },
            {
                "question": "범죄 사실을 객관적으로 증명할 수 있는 과학적 자료를 무엇이라 하는가?",
                "options": ["증명서", "증거", "판례", "영장"],
                "answer": "증거",
                "reward_title": "혈중알코올농도 감정서",
                "reward_text": "[국과수 감정서] 피의자의 혈중알코올농도는 0.18%로 측정되었음. 이는 면허 취소 기준을 크게 초과한 만취 상태임."
            },
            {
                "question": "경찰이 피의자를 체포할 때 범죄 사실과 변호인 선임권 등을 미리 알려주어야 하는 적법절차 원칙은?",
                "options": ["미란다 원칙", "죄형법정주의", "영장주의", "연좌제 금지"],
                "answer": "미란다 원칙",
                "reward_title": "적법절차 준수 수사보고서",
                "reward_text": "[수사보고서] 피의자 체포 당시 피의사실, 체포 이유, 변호인 선임권 및 변명 기회를 명확히 고지하였음."
            },
            {
                "question": "음주운전으로 사람을 다치게 하거나 사망에 이르게 한 경우 가중처벌하기 위해 제정된 이른바 '윤창호법'의 법적 근거는?",
                "options": ["도로교통법", "특정범죄 가중처벌 등에 관한 법률", "민법", "경범죄처벌법"],
                "answer": "특정범죄 가중처벌 등에 관한 법률",
                "reward_title": "특가법 제5조의11 (위험운전 등 치사상)",
                "reward_text": "음주 또는 약물의 영향으로 정상적인 운전이 곤란한 상태에서 자동차를 운전하여 사람을 사망에 이르게 한 사람은 무기 또는 3년 이상의 징역에 처한다."
            },
            {
                "question": "모든 국민은 인간으로서의 존엄과 가치를 가지며, 국가는 이를 보장할 의무가 있다고 명시한 규범은?",
                "options": ["형법 제1조", "헌법 제10조", "민법 제1조", "근로기준법 제1조"],
                "answer": "헌법 제10조",
                "reward_title": "헌법 제10조",
                "reward_text": "모든 국민은 인간으로서의 존엄과 가치를 가지며, 행복을 추구할 권리를 가진다."
            }
        ],
        "trial_dialogues": [
            {
                "speaker": "enemy",
                "name": "만취 피고인",
                "text": "판사님, 억울합니다! 회식에서 필름이 끊겨서 운전대를 잡은 기억조차 안 납니다. 저는 아무것도 모르는 심신상실 상태였다고요!",
                "press_text": "피고인: 기억이 없는데 어떻게 제 책임이 된다는 겁니까? 저는 판단할 수 없는 상태였습니다!",
                "player_text": "이의 있습니다! 스스로 술을 마셔 심신장애를 유발한 자는 처벌을 피할 수 없습니다!",
                "correct_evidence": "형법 제10조 제3항"
            },
            {
                "speaker": "enemy",
                "name": "만취 피고인",
                "text": "큭...! 제가 그렇게까지 이성을 잃었다는 객관적인 증거가 있습니까? 그냥 술냄새 조금 난 거 아닙니까!",
                "press_text": "피고인: 기계 수치 하나로 만취라고 단정할 수 있습니까? 과장된 것 아닙니까?",
                "player_text": "이의 있습니다! 사건 직후 확인된 과학적이고 명백한 증거 자료를 제출합니다. 면허 취소 수준을 아득히 넘겼습니다!",
                "correct_evidence": "혈중알코올농도 감정서"
            },
            {
                "speaker": "enemy",
                "name": "만취 피고인",
                "text": "앗...! 그, 그건 경찰이 저를 강제로 끌고 가서 피를 뽑은 겁니다! 저는 제 권리도 듣지 못했습니다. 불법 증거입니다!",
                "press_text": "피고인: 절차가 잘못됐으니 그 증거 자체가 무효 아닙니까?",
                "player_text": "이의 있습니다! 경찰은 헌법에 명시된 피의자의 권리를 정확히 고지하고 절차를 지켰습니다!",
                "correct_evidence": "적법절차 준수 수사보고서"
            },
            {
                "speaker": "enemy",
                "name": "만취 피고인",
                "text": "크아악! 설사 그렇다 해도 살인할 생각은 없었습니다. 이건 단순한 실수니까 일반 교통사고로 가볍게 처벌해주십시오!",
                "press_text": "피고인: 고의가 없었으니 중하게 벌할 이유도 없지 않습니까?",
                "player_text": "이의 있습니다! 음주운전 사망 사고는 더 이상 단순 과실이 아닙니다. 엄격한 가중처벌 대상입니다!",
                "correct_evidence": "특가법 제5조의11 (위험운전 등 치사상)"
            },
            {
                "speaker": "enemy",
                "name": "만취 피고인",
                "text": "으아아아! 한 번의 실수였습니다! 저도 살아야 하지 않겠습니까! 감옥에서 평생 썩을 수는 없다고요!",
                "press_text": "피고인: 제 인생도 중요합니다! 너무 가혹한 처벌 아닙니까?",
                "player_text": "이의 있습니다! 당신의 행동 때문에 누군가의 생명이 사라졌습니다. 피해자의 존엄성을 짓밟은 죄, 절대 가볍지 않습니다!",
                "correct_evidence": "헌법 제10조"
            }
        ]
    },

    "시나리오 3: 학교폭력 사건 (불법행위와 민법)": {
        "description": "동급생을 지속적으로 괴롭혀 비극적인 결과에 이르게 한 가해 학생들과 그 부모의 민형사상 책임을 묻습니다.",
        "quizzes": [
            {
                "question": "학교 내외에서 학생을 대상으로 발생하는 신체적, 정신적 피해를 수반하는 모든 행위를 일컫는 법적 용어는?",
                "options": ["협박", "학교폭력", "명예훼손", "업무방해"],
                "answer": "학교폭력",
                "reward_title": "학교폭력예방 및 대책에 관한 법률 제2조",
                "reward_text": "'학교폭력'이란 학교 내외에서 학생을 대상으로 발생한 상해, 폭행, 감금, 협박, 명예훼손, 모욕, 공갈, 강요, 따돌림, 사이버 따돌림 등에 의한 피해 행위를 말한다."
            },
            {
                "question": "정보통신망을 이용하여 사이버 공간에서 타인을 끈질기게 괴롭히고 명예를 훼손하는 행위를 처벌하는 법률은?",
                "options": ["사이버보호법", "정보통신망법", "민법", "소년법"],
                "answer": "정보통신망법",
                "reward_title": "정보통신망법 제70조 (벌칙)",
                "reward_text": "사람을 비방할 목적으로 정보통신망을 통하여 공공연하게 사실을 드러내어 타인의 명예를 훼손한 자는 처벌된다."
            },
            {
                "question": "만 14세 이상으로, 형사 처벌의 대상이 되는 청소년을 무엇이라 하는가?",
                "options": ["촉법소년", "범죄소년", "우범소년", "보호소년"],
                "answer": "범죄소년",
                "reward_title": "형법 제9조 (형사미성년자)",
                "reward_text": "14세 되지 아니한 자의 행위는 벌하지 아니한다. 반대로 만 14세 이상은 형사책임의 대상이 될 수 있다."
            },
            {
                "question": "미성년자가 타인에게 손해를 입혔을 때, 그 미성년자를 감독할 의무가 있는 부모 등이 지는 민사상 책임은?",
                "options": ["특수불법행위책임(감독자 책임)", "사용자 배상책임", "공동불법행위", "채무불이행책임"],
                "answer": "특수불법행위책임(감독자 책임)",
                "reward_title": "민법 제755조 (감독자의 책임)",
                "reward_text": "다른 자에게 손해를 가한 사람이 책임이 없는 경우에는 그를 감독할 법정의무가 있는 자가 손해를 배상할 책임이 있다."
            },
            {
                "question": "다른 사람에게 고의 또는 과실로 위법하게 손해를 입힌 자가 그 손해를 물어주어야 하는 일반적인 민사 책임은?",
                "options": ["연대책임", "불법행위로 인한 손해배상", "무과실책임", "신의성실의 원칙"],
                "answer": "불법행위로 인한 손해배상",
                "reward_title": "민법 제750조 (불법행위의 내용)",
                "reward_text": "고의 또는 과실로 인한 위법행위로 타인에게 손해를 가한 자는 그 손해를 배상할 책임이 있다."
            }
        ],
        "trial_dialogues": [
            {
                "speaker": "enemy",
                "name": "가해 학생",
                "text": "장난으로 몇 번 툭툭 친 것뿐이에요. 걔가 그렇게 예민하게 반응할 줄 몰랐다고요! 그게 무슨 범죄입니까?",
                "press_text": "가해 학생: 친구끼리 장난도 못 칩니까? 다들 웃고 넘길 수 있는 일이었어요!",
                "player_text": "이의 있습니다! 장난을 넘어선 지속적인 신체적, 정신적 괴롭힘은 명백한 학교폭력입니다.",
                "correct_evidence": "학교폭력예방 및 대책에 관한 법률 제2조"
            },
            {
                "speaker": "enemy",
                "name": "가해 학생",
                "text": "온라인 단톡방에서 우리끼리 좀 뒷담화한 게 무슨 상관이에요! 직접 때린 것도 아닌데!",
                "press_text": "가해 학생: 단톡방 말장난까지 처벌하면 너무한 것 아닙니까?",
                "player_text": "이의 있습니다! 정보통신망을 이용해 집단으로 명예를 훼손하고 따돌린 행위는 엄연한 범죄입니다!",
                "correct_evidence": "정보통신망법 제70조 (벌칙)"
            },
            {
                "speaker": "enemy",
                "name": "가해자 측 변호사",
                "text": "피고인들은 아직 미성숙한 학생들입니다. 형사 처벌이 아닌 소년부 송치를 통한 보호처분만 받아야 합니다!",
                "press_text": "변호사: 어린 학생에게 성인과 같은 책임을 묻는 것은 과도합니다!",
                "player_text": "이의 있습니다! 피고인들은 범행 당시 이미 만 14세를 넘었으므로 엄연한 형사 처벌의 대상이 됩니다!",
                "correct_evidence": "형법 제9조 (형사미성년자)"
            },
            {
                "speaker": "enemy",
                "name": "가해자 부모",
                "text": "우리 애가 잘못한 건 맞지만, 왜 부모인 우리한테까지 수천만 원을 물어내라고 하는 겁니까! 우린 때리지 않았어요!",
                "press_text": "부모: 부모가 직접 행동한 것도 아닌데 왜 책임을 져야 합니까?",
                "player_text": "이의 있습니다! 미성년 자녀가 불법행위를 저질렀을 때 감독 의무가 있는 부모에게도 민사상 배상 책임이 있습니다!",
                "correct_evidence": "민법 제755조 (감독자의 책임)"
            },
            {
                "speaker": "enemy",
                "name": "가해 학생",
                "text": "크윽... 하지만... 이미 끝난 일이잖아요. 이제 와서 우리가 배상금을 낸다고 죽은 애가 살아 돌아오기라도 합니까!",
                "press_text": "가해 학생: 어차피 되돌릴 수 없는 일이라면 지금 와서 책임을 묻는 게 무슨 의미가 있죠?",
                "player_text": "이의 있습니다! 당신들의 위법행위로 인해 한 생명이 사라졌습니다. 평생 그 손해를 배상하고 책임져야 합니다!",
                "correct_evidence": "민법 제750조 (불법행위의 내용)"
            }
        ]
    },

    "시나리오 4: 부동산 계약 파기 (계약과 채무불이행)": {
        "description": "아파트 매매 계약 후 매수인이 계약금까지 지불했는데, 집값이 올랐다며 일방적으로 계약을 파기한 매도인과 맞섭니다.",
        "quizzes": [
            {
                "question": "일정한 법률 효과의 발생을 목적으로 하는 당사자 간의 의사표시의 합치를 무엇이라고 하는가?",
                "options": ["청약", "승낙", "계약", "증여"],
                "answer": "계약",
                "reward_title": "매매계약서 원본 (민법 제563조)",
                "reward_text": "[아파트 매매계약서 원본] 매도인은 재산권을 이전하고 매수인은 대금을 지급할 것을 약정함으로써 효력이 발생한다."
            },
            {
                "question": "계약을 체결할 때, 그 증거로서 당사자 일방이 상대방에게 교부하는 초기 금전을 무엇이라고 하는가?",
                "options": ["보증금", "계약금", "중도금", "잔금"],
                "answer": "계약금",
                "reward_title": "계약금 이체 영수증",
                "reward_text": "[은행 이체 확인증] 이체 금액: 50,000,000원 / 적요: 아파트 매매 계약금 / 상태: 이체 완료"
            },
            {
                "question": "계약금만 지급한 상태에서 매도인이 일방적으로 계약을 해제하려면 계약금의 얼마를 상환해야 하는가?",
                "options": ["원금", "1.5배", "배액(2배)", "3배"],
                "answer": "배액(2배)",
                "reward_title": "민법 제565조 (해약금)",
                "reward_text": "매매 당사자 일방은 이행에 착수할 때까지 교부자는 계약금을 포기하고, 수령자는 그 배액을 상환하여 계약을 해제할 수 있다."
            },
            {
                "question": "당사자 일방이 정당한 이유 없이 계약 내용을 약속대로 이행하지 않는 것을 무엇이라고 하는가?",
                "options": ["채무불이행", "불법행위", "부당이득", "사기"],
                "answer": "채무불이행",
                "reward_title": "민법 제390조 (채무불이행과 손해배상)",
                "reward_text": "채무자가 채무의 내용에 좇은 이행을 하지 아니한 때에는 채권자는 손해배상을 청구할 수 있다."
            },
            {
                "question": "계약 위반 시 미리 정해둔 금액을 배상하기로 하는 약정을 무엇이라 하는가?",
                "options": ["해약금", "증약금", "손해배상액의 예정(위약금)", "보증금"],
                "answer": "손해배상액의 예정(위약금)",
                "reward_title": "위약금 특약 조항 (민법 제398조)",
                "reward_text": "[계약서 특약사항] 매도인 또는 매수인이 계약 내용을 불이행할 경우, 상대방은 계약금을 손해배상의 기준으로 삼아 청구할 수 있다."
            }
        ],
        "trial_dialogues": [
            {
                "speaker": "enemy",
                "name": "매도인",
                "text": "아니, 내 집 내가 안 팔겠다는데 무슨 상관입니까! 하루 만에 집값이 1억이 올랐는데 미쳤다고 그 가격에 팝니까! 없던 일로 합시다!",
                "press_text": "매도인: 아직 등기 넘긴 것도 아닌데, 그냥 계약 취소하면 되는 것 아닙니까?",
                "player_text": "이의 있습니다! 양 당사자의 서명과 도장이 찍힌 순간부터 법적인 효력이 발생했습니다. 일방적인 취소는 불가능합니다!",
                "correct_evidence": "매매계약서 원본 (민법 제563조)"
            },
            {
                "speaker": "enemy",
                "name": "매도인",
                "text": "도장만 찍었지 아직 제대로 된 돈도 안 줬잖아요! 구두 계약이나 다름없습니다!",
                "press_text": "매도인: 돈이 오간 게 별로 없으니 아직 본격적인 계약이 아니라고 봐야 하지 않습니까?",
                "player_text": "이의 있습니다! 매수인 측에서 이미 초기 금액을 입금하여 계약이 정상적으로 성립되었습니다.",
                "correct_evidence": "계약금 이체 영수증"
            },
            {
                "speaker": "enemy",
                "name": "매도인",
                "text": "흥! 그래봤자 계약금일 뿐입니다. 그냥 그 계약금 원금 5천만 원만 통장으로 다시 쏴줄 테니 당장 떨어지쇼!",
                "press_text": "매도인: 계약금만 돌려주면 깔끔한 것 아닙니까? 뭐가 더 문제죠?",
                "player_text": "이의 있습니다! 법에 따르면 매도인이 일방적으로 파기할 경우 원금이 아니라 배액(2배)을 상환해야 합니다!",
                "correct_evidence": "민법 제565조 (해약금)"
            },
            {
                "speaker": "enemy",
                "name": "매도인 측 변호사",
                "text": "피고가 집을 넘기지 않은 것은 일시적인 변심일 뿐, 의도적인 계약 위반은 아닙니다. 거액의 배상 청구는 너무 과합니다!",
                "press_text": "변호사: 단순 변심일 뿐이라면 손해배상까지 인정하는 것은 지나치지 않습니까?",
                "player_text": "이의 있습니다! 약속한 날짜에 소유권을 이전하지 않은 것은 명백한 채무불이행이며 법적 의무 위반입니다!",
                "correct_evidence": "민법 제390조 (채무불이행과 손해배상)"
            },
            {
                "speaker": "enemy",
                "name": "매도인",
                "text": "크악...! 줘, 주면 될 거 아뇨! 2배 돌려주면 되잖아! 근데 거기에 추가로 계약서상의 위약금까지 달라는 건 완전 도둑놈 심보 아닙니까!",
                "press_text": "매도인: 계약서 문구까지 들먹이며 더 달라는 건 너무 과욕 아닌가요?",
                "player_text": "이의 있습니다! 작성하신 계약서 특약 조항에 따라, 계약 파기 시 당신은 정당한 손해배상액을 지불해야 할 법적 의무가 있습니다!",
                "correct_evidence": "위약금 특약 조항 (민법 제398조)"
            }
        ]
    }
}

# =========================================================
# 3. 사이드바
# =========================================================
st.sidebar.header("⚖️ 변호사 상태창")

lives_display = "❤️" * max(st.session_state.lives, 0) + "🖤" * (3 - max(st.session_state.lives, 0))
st.sidebar.subheader(f"남은 기회: {lives_display}")
st.sidebar.write(f"신뢰도: {st.session_state.trust}/100")
st.sidebar.progress(min(max(st.session_state.trust, 0), 100) / 100)

st.sidebar.markdown("---")
st.sidebar.header("🏅 플레이 기록")
st.sidebar.write(f"점수: {st.session_state.score}")
st.sidebar.write(f"콤보: {st.session_state.combo}")
st.sidebar.write(f"최대 콤보: {st.session_state.max_combo}")
st.sidebar.write(f"남은 힌트: {st.session_state.hint_count}")
st.sidebar.write(f"숨겨진 증거 수: {len(st.session_state.bonus_evidence)}")

st.sidebar.markdown("---")
st.sidebar.header("🧳 나의 법적 무기 (인벤토리)")
if st.session_state.inventory:
    for title, text in st.session_state.inventory.items():
        with st.sidebar.expander(title):
            st.write(text)
else:
    st.sidebar.info("아직 획득한 법 조항이 없습니다.")

# =========================================================
# 4. 시나리오 선택 화면
# =========================================================
if st.session_state.stage == "scenario_select":
    st.title("사회 모의재판: 역전의 명수 🏛️")
    st.write("진행할 사건 시나리오를 선택하세요.")

    scenario_list = list(scenario_data.keys())
    selected = st.radio("사건 목록", scenario_list)

    st.info(scenario_data[selected]["description"])

    if st.button("수사 시작"):
        st.session_state.current_scenario = selected
        st.session_state.stage = "quiz"
        st.rerun()

# =========================================================
# 5. 증거 수집(퀴즈) 화면
# =========================================================
elif st.session_state.stage == "quiz":
    st.title("증거 수집: 사건 현장 조사 🔍")
    st.write("재판에 필요한 법 조항과 증거를 모으기 위해 퀴즈를 해결하세요.")

    current_data = scenario_data[st.session_state.current_scenario]
    quizzes = current_data["quizzes"]
    q_idx = st.session_state.quiz_index

    if q_idx < len(quizzes):
        quiz = quizzes[q_idx]
        st.subheader(f"질문 {q_idx + 1} / {len(quizzes)}")
        st.write(quiz["question"])

        if st.session_state.current_hint:
            st.info(st.session_state.current_hint)

        user_answer = st.radio("정답을 선택하세요", quiz["options"], key=f"q_{q_idx}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🕵️ 힌트 사용"):
                if st.session_state.hint_count > 0:
                    st.session_state.hint_count -= 1
                    st.session_state.used_hints += 1
                    st.session_state.score = max(0, st.session_state.score - 5)
                    st.session_state.trust = max(0, st.session_state.trust - 3)
                    st.session_state.current_hint = get_quiz_hint(quiz)
                    st.rerun()
                else:
                    st.warning("더 이상 사용할 수 있는 힌트가 없습니다.")

        with col2:
            if st.button("제출 및 단서 확보"):
                st.session_state.current_hint = ""
                if user_answer == quiz["answer"]:
                    handle_correct(base_score=10)
                    st.session_state.inventory[quiz["reward_title"]] = quiz["reward_text"]
                    st.success(f"정답입니다! 단서 획득: **{quiz['reward_title']}**")
                    try_get_bonus_evidence()
                    st.session_state.quiz_index += 1
                    st.rerun()
                else:
                    handle_wrong(life_penalty=1, trust_penalty=5)
                    st.error("오답입니다. 법전을 다시 확인해 보세요.")
                    if check_game_over():
                        st.rerun()

        st.progress((q_idx) / len(quizzes))
    else:
        st.success("모든 증거를 수집했습니다! 이제 법정으로 이동할 수 있습니다.")
        if st.button("법정으로 이동"):
            st.session_state.stage = "trial"
            st.session_state.current_hint = ""
            st.rerun()

# =========================================================
# 6. 법정 공방 화면
# =========================================================
elif st.session_state.stage == "trial":
    st.title("재판 개정: 진실의 법정 ⚖️")
    st.subheader(st.session_state.current_scenario)

    current_data = scenario_data[st.session_state.current_scenario]
    dialogues = current_data["trial_dialogues"]
    current_step = st.session_state.court_index

    try:
        st.image("judge.png", width=150)
    except Exception:
        st.caption("[재판장 이미지 자리 - judge.png 필요]")

    st.markdown("---")

    if current_step < len(dialogues):
        dialogue = dialogues[current_step]

        col1, col2 = st.columns(2)

        with col1:
            try:
                st.image("enemy.png", width=220)
            except Exception:
                st.caption("[상대방 이미지 자리 - enemy.png 필요]")

            st.error(f"**{dialogue['name']}**: {dialogue['text']}")

            if st.button("🔍 추궁한다"):
                st.session_state.pressed_mode = True
                st.session_state.score += 3
                st.rerun()

            if st.session_state.pressed_mode:
                st.info(f"추궁 결과: {dialogue.get('press_text', '상대의 진술에 미세한 모순이 보입니다.')}")

        with col2:
            try:
                st.image("player.png", width=220)
            except Exception:
                st.caption("[변호사 이미지 자리 - player.png 필요]")

            st.write("상대방의 주장을 논파할 정확한 증거를 선택하세요.")

            if st.session_state.current_hint:
                st.info(st.session_state.current_hint)

            inventory_keys = list(st.session_state.inventory.keys())
            selected_evidence = st.selectbox(
                "증거 제출",
                inventory_keys,
                key=f"trial_select_{current_step}"
            )

            c1, c2 = st.columns(2)

            with c1:
                if st.button("📚 법정 힌트 사용"):
                    if st.session_state.hint_count > 0:
                        st.session_state.hint_count -= 1
                        st.session_state.used_hints += 1
                        st.session_state.score = max(0, st.session_state.score - 8)
                        st.session_state.trust = max(0, st.session_state.trust - 5)
                        st.session_state.current_hint = get_trial_hint(dialogue)
                        st.rerun()
                    else:
                        st.warning("더 이상 힌트가 없습니다.")

            with c2:
                if st.button("이의 있음! (증거 제출)"):
                    st.session_state.current_hint = ""
                    pressed_bonus = 5 if st.session_state.pressed_mode else 0
                    bonus_score = get_bonus_score_from_inventory()

                    if selected_evidence == dialogue["correct_evidence"]:
                        st.session_state.presented_evidence.append(selected_evidence)
                        handle_correct(base_score=20 + pressed_bonus + bonus_score)
                        st.success(f"**나의 반박**: {dialogue['player_text']}")
                        st.info("재판장: 증거가 타당합니다. 다음으로 넘어가시죠.")
                        st.session_state.court_index += 1
                        st.session_state.pressed_mode = False

                        if st.session_state.court_index >= len(dialogues):
                            st.session_state.stage = "win"
                        st.rerun()
                    else:
                        handle_wrong(life_penalty=1, trust_penalty=15)
                        st.error("판사: 기각합니다! 적절치 않은 증거입니다.")
                        st.session_state.pressed_mode = False
                        if check_game_over():
                            st.rerun()

        st.progress(current_step / len(dialogues))

    else:
        st.session_state.stage = "win"
        st.rerun()

# =========================================================
# 7. 승소 화면
# =========================================================
elif st.session_state.stage == "win":
    assign_badges()
    ending = determine_ending()
    grade = calculate_grade()

    st.title("최종 판결: 승소! 🎉")

    try:
        st.image("judge.png", width=200)
    except Exception:
        pass

    st.write("**판사**: 변호인 측의 논리와 법적 근거가 충분히 인정됩니다. 피고의 주장을 기각하고 원고 측의 승소를 선언합니다.")
    st.success("축하합니다! 정의를 수호하셨습니다!")
    st.balloons()

    st.markdown("---")
    st.subheader(f"엔딩: {ending}")
    st.subheader(f"최종 등급: {grade}")

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"점수: {st.session_state.score}")
        st.write(f"남은 목숨: {st.session_state.lives}")
        st.write(f"신뢰도: {st.session_state.trust}")
    with col2:
        st.write(f"최대 콤보: {st.session_state.max_combo}")
        st.write(f"사용한 힌트: {st.session_state.used_hints}")
        st.write(f"숨겨진 증거 수집: {len(st.session_state.bonus_evidence)}")

    if st.session_state.badges:
        st.markdown("### 획득 배지")
        for badge in st.session_state.badges:
            st.write(badge)

    if st.button("다른 사건 맡기 (처음으로)"):
        reset_game()
        st.rerun()

# =========================================================
# 8. 패소 화면
# =========================================================
elif st.session_state.stage == "game_over":
    st.title("최종 판결: 패소... 😭")

    try:
        st.image("enemy.png", width=200)
    except Exception:
        pass

    if st.session_state.lives <= 0:
        reason = "증거 제출 기회(목숨)를 모두 소진했습니다."
    elif st.session_state.trust <= 0:
        reason = "법정 신뢰도를 모두 잃었습니다."
    else:
        reason = "재판 진행이 불가능해졌습니다."

    st.error("**판사**: 변호인 측의 잦은 무리한 주장과 부적절한 증거 제출로 인해 재판을 더 이상 신뢰할 수 없습니다. 패소를 선언합니다.")
    st.warning(reason)

    st.markdown("---")
    st.write(f"최종 점수: {st.session_state.score}")
    st.write(f"최대 콤보: {st.session_state.max_combo}")
    st.write(f"사용한 힌트: {st.session_state.used_hints}")

    if st.button("재심 청구 (다시 시작)"):
        reset_game()
        st.rerun()
