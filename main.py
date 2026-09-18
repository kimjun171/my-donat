# ==========================================
# [섹션 8] 개봉일 스크린수 vs 개봉일 상영 횟수 (산점도)
# ==========================================
st.header("📌 8. 개봉일 스크린수가 많은 영화가 상영 횟수도 많은가")

# 산점도(Scatter Plot) 생성
fig8 = px.scatter(
    df,
    x="first_scrn",
    y="first_show",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린수가 많은 영화가 상영 횟수도 많은가",
    labels={
        "first_scrn": "개봉일 스크린수 (개)",
        "first_show": "개봉일 상영 횟수 (회)",
        "genre": "장르",
    },
    color_discrete_sequence=px.colors.qualitative.Vivid,
)

# 마우스 오버(Hover) 시 영화명, 스크린수, 상영 횟수가 보이도록 설정
fig8.update_traces(
    marker=dict(size=9, opacity=0.8),
    hovertemplate="<b>%{hovertext}</b><br><b>장르:</b> %{fullData.name}<br><b>개봉일 스크린수:</b> %{x:,}개<br><b>개봉일 상영 횟수:</b> %{y:,}회<extra></extra>",
)

fig8.update_layout(
    xaxis_title="개봉일 스크린수 (개)",
    yaxis_title="개봉일 상영 횟수 (회)",
    height=550,
    legend=dict(title_text="장르 (클릭 시 ON/OFF)"),
)

# 그래프 출력
st.plotly_chart(fig8, use_container_width=True)

# 💡 '이 그래프로 알 수 있는 것' 문구 작성 구역
st.info(
    "💡 **이 그래프로 알 수 있는 것:**\n\n"
    "(여기에 분석 소감을 작성해 주세요. 예: 개봉일 스크린수가 많은 영화일수록 개봉일 당일 상영 횟수도 거의 비례하여 증가하는 매우 강한 양의 상관관계를 볼 수 있습니다.)"
)
