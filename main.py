import pandas as pd
import plotly.express as px
import streamlit as st

# Streamlit 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide",
)


# 데이터 불러오기 및 전처리 함수 (1시간 캐싱)
@st.cache_data(ttl=3600)
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

    # CSV 로드 (개봉일과 영화코드는 문자열로 변환)
    df = pd.read_csv(url, dtype={"movieCd": str, "openDt": str})

    # 1. 장르 처리: 세로막대 기호(|)로 여러 개 적힌 경우 첫 번째 장르만 추출
    df["genre"] = (
        df["genre"].astype(str).apply(lambda x: x.split("|")[0].strip())
    )

    # 2. 숫자형 데이터 정제
    numeric_cols = [
        "first_scrn",
        "first_show",
        "first_week_audi",
        "total_audi",
        "days_in_top10",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = (
                pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
            )

    return df


# 데이터 로드
df = load_data()

# 메인 타이틀
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.caption(
    "박스오피스 10위권에 등재된 개봉 영화 216편의 장르, 국가, 관객수 분포 및 상관관계 분석"
)

st.markdown("---")

# ==========================================
# [섹션 1] 장르별 영화 편수 (도넛 그래프)
# ==========================================
st.header("📌 1. 장르별 영화 편수 분포")

# 장르별 영화 편수 집계
genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["장르", "영화수"]

# Plotly 도넛 그래프(Donut Chart) 생성
fig1 = px.pie(
    genre_counts,
    names="장르",
    values="영화수",
    title="개봉 영화의 장르별 비중",
    hole=0.4,
    color_discrete_sequence=px.colors.qualitative.Pastel,
)

# 마우스 오버(Hover) 시 편수와 비율(퍼센트) 표시
fig1.update_traces(
    textposition="inside",
    textinfo="percent+label",
    hovertemplate="<b>장르:</b> %{label}<br><b>영화 수:</b> %{value}편<br><b>비율:</b> %{percent}<extra></extra>",
)

fig1.update_layout(
    height=500,
    legend=dict(title_text="장르 목록", orientation="v", y=0.5),
)

# 그래프 출력
st.plotly_chart(fig1, use_container_width=True)

# 💡 '이 그래프로 알 수 있는 것' 문구 작성 구역
st.info(
    "💡 **이 그래프로 알 수 있는 것:**\n\n"
    "(여기에 분석 소감을 작성해 주세요. 예: 흥행권에 진입한 영화 중 애니메이션과 드라마가 가장 높은 비중을 차지함을 알 수 있습니다.)"
)

st.markdown("---")

# ==========================================
# [섹션 2] 장르 및 영화별 총 관객수 (트리맵)
# ==========================================
st.header("📌 2. 장르별 영화 및 총 관객수 규모 (트리맵)")

# 트리맵 계층 구조 설정 (장르 -> 영화명)
fig2 = px.treemap(
    df,
    path=[px.Constant("전체 장르"), "genre", "movieNm"],
    values="total_audi",
    title="장르 및 영화별 총 관객수 비중 (칸 크기: 총 관객수)",
    color="genre",
    color_discrete_sequence=px.colors.qualitative.Set3,
)

# 마우스 오버(Hover) 시 영화명(또는 장르명)과 총 관객수 콤마 서식 표시
fig2.update_traces(
    hovertemplate="<b>%{label}</b><br><b>총 관객수:</b> %{value:,}명<extra></extra>"
)

fig2.update_layout(
    height=600,
)

# 그래프 출력
st.plotly_chart(fig2, use_container_width=True)

# 💡 '이 그래프로 알 수 있는 것' 문구 작성 구역
st.info(
    "💡 **이 그래프로 알 수 있는 것:**\n\n"
    "(여기에 분석 소감을 작성해 주세요. 예: 특정 장르 내에서도 소수의 초대형 대작 영화가 전체 장르 관객수의 대부분을 견인하는 모습을 볼 수 있습니다.)"
)

st.markdown("---")

# ==========================================
# [섹션 3] 총 관객수 분포 (히스토그램)
# ==========================================
st.header("📌 3. 총 관객수 분포 (히스토그램)")

# 1. 총 관객수 히스토그램 생성
fig3 = px.histogram(
    df,
    x="total_audi",
    title="영화별 총 관객수 분포",
    labels={"total_audi": "총 관객수 (명)", "count": "영화 수 (편)"},
    nbins=30,  # 구간(bin) 세분화
)

# 마우스 오버 툴팁 및 색상 서식
fig3.update_traces(
    marker_color="#636EFA",
    marker_line_color="white",
    marker_line_width=1,
    hovertemplate="<b>관객수 구간:</b> %{x}<br><b>해당 영화 수:</b> %{y}편<extra></extra>",
)

fig3.update_layout(
    xaxis_title="총 관객수 (명)",
    yaxis_title="영화 수 (편)",
    height=450,
)

# 그래프 출력
st.plotly_chart(fig3, use_container_width=True)

# 2. 가장 관객이 많은 영화 데이터 추출
top_movie = df.loc[df["total_audi"].idxmax()]

# 💡 '이 그래프로 알 수 있는 것' 문구 작성 구역 (자동 탐지 문구 포함)
st.info(
    "💡 **이 그래프로 알 수 있는 것:**\n\n"
    f"- **밀집 구간:** 대부분의 영화는 관객수 **50만 명 이하** 구간에 강하게 집중되어 분포하고 있습니다.\n"
    f"- **최다 관객 영화:** 이 기간 가장 관객이 많은 영화는 **'{top_movie['movieNm']}'** (총 {top_movie['total_audi']:,}명)입니다.\n\n"
    "(소수의 흥행 대작이 오른쪽 끝에 위치하며 긴 꼬리 형태의 오른쪽으로 비대칭인 분포를 형성합니다.)"
)

st.markdown("---")

# ==========================================
# [섹션 4] 향후 추가될 그래프 구역
# ==========================================
st.header("📌 4. (추가 예정 구역)")
st.caption(
    "앞으로 '분포와 관계'에 관한 다양한 그래프(예: 스크린 수와 관객수의 산점도 등)가 추가될 영역입니다."
)
