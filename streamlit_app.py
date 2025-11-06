import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io

# -----------------------------------------------------
# НАСТРОЙКА
# -----------------------------------------------------
st.set_page_config(page_title="CTR // Данные", layout="wide")

# -----------------------------------------------------
# ЭКРАН АВТОРИЗАЦИИ
# -----------------------------------------------------
if "auth_ok" not in st.session_state:
    st.session_state.auth_ok = False

if not st.session_state.auth_ok:
    st.markdown(
        """
        <div style="text-align:center;margin-top:4rem;">
            <h2>Доступ</h2>
            <p style="color:#9ca3af;">Введите пароль, чтобы продолжить</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    pwd = st.text_input("Пароль", type="password", label_visibility="collapsed")
    if pwd == "SportsTeam":
        st.session_state.auth_ok = True
        st.rerun()
    st.stop()

# -----------------------------------------------------
# ФУНКЦИИ ДЛЯ СЕКРЕТОВ
# -----------------------------------------------------
def read_secret_csv(section: str, key: str, date_col: str = None) -> pd.DataFrame:
    """
    Читает CSV из st.secrets[section][key].
    Если указан date_col — приводим к datetime и сортируем.
    """
    txt = st.secrets[section].get(key, "").strip()
    if not txt:
        return pd.DataFrame()
    df = pd.read_csv(io.StringIO(txt))
    if date_col and date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(date_col).reset_index(drop=True)
    return df

def pct_str_to_float(x: str):
    """
    "0,23 %" -> 0.0023 ; пустые -> None
    """
    if pd.isna(x):
        return None
    if not isinstance(x, str):
        return None
    x = x.replace("%", "").replace("\xa0", "").replace(" ", "").replace(",", ".")
    try:
        return float(x) / 100.0
    except Exception:
        return None

# -----------------------------------------------------
# ЗАГРУЗКА ДАННЫХ ИЗ СЕКРЕТОВ
# -----------------------------------------------------
# CTR (основная серия)
df_ctr = read_secret_csv("CTR", "DATA", date_col="День")

# Трафик "в разделе"
df_section = read_secret_csv("SECTION_TRAFFIC", "CSV", date_col="Период")

# События
df_events = read_secret_csv("EVENTS", "CSV")
if not df_events.empty:
    df_events["начало"] = pd.to_datetime(df_events["начало"])
    df_events["окончание"] = pd.to_datetime(df_events["окончание"])

# Другие РК (серии с процентами)
df_F_raw = read_secret_csv("OTHER_CAMPAIGNS", "SERIES_F", date_col="date")
if not df_F_raw.empty:
    df_F_raw.rename(columns={"date": "День", "pct": "pct"}, inplace=True)
    df_F_raw["CTR"] = df_F_raw["pct"].apply(pct_str_to_float)
    df_F = df_F_raw.dropna(subset=["CTR"])[["День", "CTR"]].sort_values("День").reset_index(drop=True)
else:
    df_F = pd.DataFrame(columns=["День", "CTR"])

df_TGF_raw = read_secret_csv("OTHER_CAMPAIGNS", "SERIES_TGF", date_col="date")
if not df_TGF_raw.empty:
    df_TGF_raw.rename(columns={"date": "День", "pct": "pct"}, inplace=True)
    df_TGF_raw["CTR"] = df_TGF_raw["pct"].apply(pct_str_to_float)
    df_TGF = df_TGF_raw.dropna(subset=["CTR"])[["День", "CTR"]].sort_values("День").reset_index(drop=True)
else:
    df_TGF = pd.DataFrame(columns=["День", "CTR"])

# Общий трафик N / V / O
df_N = read_secret_csv("GLOBAL_TRAFFIC", "N", date_col="date")
df_V = read_secret_csv("GLOBAL_TRAFFIC", "V", date_col="date")
df_O = read_secret_csv("GLOBAL_TRAFFIC", "O", date_col="date")

# -----------------------------------------------------
# ПОДГОТОВКА ОСНОВНЫХ ДФ
# -----------------------------------------------------
if not df_ctr.empty:
    df_ctr["День"] = pd.to_datetime(df_ctr["День"])
    df_ctr = df_ctr.sort_values("День").reset_index(drop=True)

if not df_section.empty:
    df_section["Период"] = pd.to_datetime(df_section["Период"])
    df_section = df_section.sort_values("Период").reset_index(drop=True)

# Допсерии для «Другие РК»
EXTRA_SERIES = [
    {"name": "Ф", "df": df_F, "style": {"dash": "dot", "width": 2.2, "color": "rgba(255,99,132,1)", "marker_size": 4}},
    {"name": "ТГ-Ф", "df": df_TGF, "style": {"dash": "dash", "width": 2.2, "color": "rgba(46,204,113,1)", "marker_size": 4}},
]

# -----------------------------------------------------
# ВИЗУАЛЬНЫЙ СЕЛЕКТОР СТРАНИЦ
# -----------------------------------------------------
with st.container():
    st.markdown(
        """
        <style>
        .page-pill { display:inline-block; margin-right:0.5rem; margin-bottom:0.4rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='margin-bottom:0.4rem;font-weight:500;'>Выбор раздела</div>", unsafe_allow_html=True)
    page = st.radio(
        "",
        ("Итоги","Смена креативов","Спортивные события","Трафик в разделе","Просмотры","Другие РК","Общий трафик"),
        horizontal=True,
        label_visibility="collapsed",
    )

# =====================================================
# 1) ИТОГИ
# =====================================================
if page == "Итоги":
    st.markdown("### Итоги")

    stage_2_start = pd.to_datetime("2025-07-07")
    stage_3_start = pd.to_datetime("2025-08-14")
    stage_4_start = pd.to_datetime("2025-10-22")
    stage_switches = [stage_2_start, stage_3_start, stage_4_start]

    df_all = df_ctr.dropna(subset=["CTR"]).copy().sort_values("День").reset_index(drop=True)
    global_views_mean = df_all["Просмотры"].mean()

    def exact_events_for_day(d: pd.Timestamp) -> str:
        if df_events.empty: return ""
        names = []
        for _, ev in df_events.iterrows():
            if ev["начало"].date() == d.date() or ev["окончание"].date() == d.date():
                names.append(ev["название"])
        return ", ".join(names)

    def stage_for_day(d: pd.Timestamp) -> int:
        if d < stage_2_start: return 1
        elif d < stage_3_start: return 2
        elif d < stage_4_start: return 3
        else: return 4

    def is_stage_switch_near(d: pd.Timestamp) -> str:
        for sw in stage_switches:
            if sw < d <= sw + pd.Timedelta(days=7):
                return "да"
        return "нет"

    df_all["Точные события"] = df_all["День"].apply(exact_events_for_day)
    df_all["Этап"] = df_all["День"].apply(stage_for_day)
    df_all["Смена креативов"] = df_all["День"].apply(is_stage_switch_near)
    df_all["Дата"] = df_all["День"].dt.strftime("%d.%m.%Y")
    df_all["CTR (в %)"] = df_all["CTR"].map(lambda x: f"{x:.2%}")
    df_all["Просмотры выше среднего"] = df_all["Просмотры"].apply(lambda v: "да" if v >= global_views_mean else "нет")

    min_day, max_day = df_all["День"].min(), df_all["День"].max()
    local_views_means, local_ctr_means, ctr_local_flags, views_local_flags = [], [], [], []

    for _, row in df_all.iterrows():
        cur_day = row["День"]
        date_min = max(min_day, cur_day - pd.Timedelta(days=7))
        date_max = min(max_day, cur_day + pd.Timedelta(days=7))
        window = df_all[(df_all["День"] >= date_min) & (df_all["День"] <= date_max)]
        lv_mean = window["Просмотры"].mean(); local_views_means.append(lv_mean)
        views_local_flags.append("да" if row["Просмотры"] >= lv_mean else "нет")
        lc_mean = window["CTR"].mean(); local_ctr_means.append(lc_mean)
        ctr_local_flags.append("да" if row["CTR"] >= lc_mean else "нет")

    df_all["Локальное среднее просмотров"] = local_views_means
    df_all["Просмотры выше локального"] = views_local_flags
    df_all["Локальный CTR"] = local_ctr_means
    df_all["CTR выше локального"] = ctr_local_flags
    df_all["Локальный CTR (в %)"] = df_all["Локальный CTR"].map(lambda x: f"{x:.2%}")

    df_table_ctr = df_all[df_all["CTR выше локального"] == "да"].copy().sort_values("CTR", ascending=False)
    total_peaks = len(df_table_ctr)
    events_count = (df_table_ctr["Точные события"] != "").sum()
    views_high_global = (df_table_ctr["Просмотры выше среднего"] == "да").sum()
    views_high_local = (df_table_ctr["Просмотры выше локального"] == "да").sum()
    stage_switch_count = (df_table_ctr["Смена креативов"] == "да").sum()

    def to_pct(count): return 0.0 if total_peaks == 0 else (count / total_peaks) * 100.0

    metrics = [
        {"title": "Просмотры выше локального (±7 дн)", "value": to_pct(views_high_local)},
        {"title": "Просмотры выше среднего (глобально)", "value": to_pct(views_high_global)},
        {"title": "Смена креативов (+7 дн)", "value": to_pct(stage_switch_count)},
        {"title": "События", "value": to_pct(events_count)},
    ]
    metrics = sorted(metrics, key=lambda x: x["value"], reverse=True)

    cards = []
    for m in metrics:
        cards.append(
            f"<div style='background:#111827;border:1px solid #1f2937;border-radius:0.75rem;padding:0.75rem 1rem;min-width:190px;'>"
            f"<div style='font-size:0.7rem;color:#cbd5e1;'>{m['title']}</div>"
            f"<div style='font-size:1.6rem;font-weight:700;color:#f9fafb'>{m['value']:.1f}%</div>"
            f"</div>"
        )
    cards_html = "<div style='display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:0.5rem;'>" + "".join(cards) + "</div>" \
                 "<div style='color:#94a3b8;margin-bottom:1.5rem;'>Наличие признака в день пикового CTR в диапазоне 14 дней</div>"
    st.markdown(cards_html, unsafe_allow_html=True)

    st.markdown("#### 1) Дни по CTR выше локального среднего (±7 дней)")
    cols_ctr = ["Дата","CTR (в %)","Локальный CTR (в %)","Точные события","Просмотры выше среднего","Просмотры выше локального","Этап","Смена креативов"]
    cols_ctr = [c for c in cols_ctr if c in df_table_ctr.columns]
    st.dataframe(df_table_ctr[cols_ctr], use_container_width=True, hide_index=True)
    st.markdown(f"**Количество строк:** {len(df_table_ctr)}")

    st.markdown("#### 2) Все дни по убыванию CTR")
    df_table_all = df_all.sort_values("CTR", ascending=False)
    cols_all = [c for c in cols_ctr if c in df_table_all.columns]
    st.dataframe(df_table_all[cols_all], use_container_width=True, hide_index=True)
    st.markdown("<div style='margin-top:1.5rem;color:#94a3b8;'>Наличие признака в день пикового CTR в диапазоне 14 дней</div>", unsafe_allow_html=True)

# =====================================================
# 2) СМЕНА КРЕАТИВОВ
# =====================================================
elif page == "Смена креативов":
    st.markdown("### CTR по этапам кампании (смены креативов)")
    b1 = pd.to_datetime("2025-04-23"); b2 = pd.to_datetime("2025-07-07")
    b3 = pd.to_datetime("2025-08-14"); b4 = pd.to_datetime("2025-10-22"); b5 = pd.to_datetime("2025-10-29")
    df2 = df_ctr.dropna(subset=["CTR"]).copy()

    fig2 = go.Figure()
    seg1 = df2[(df2["День"] >= b1) & (df2["День"] < b2)]
    fig2.add_trace(go.Scatter(x=seg1["День"], y=seg1["CTR"], mode="lines+markers", name="23.04 – 07.07",
                              line=dict(color="rgba(141,181,255,1)", width=2.2), marker=dict(size=4),
                              hovertemplate="%{x|%d.%m.%Y}<br>CTR: %{y:.2%}<extra></extra>"))
    seg2 = df2[(df2["День"] >= b2) & (df2["День"] < b3)]
    fig2.add_trace(go.Scatter(x=seg2["День"], y=seg2["CTR"], mode="lines+markers", name="07.07 – 14.08",
                              line=dict(color="rgba(102,204,153,1)", width=2.2), marker=dict(size=4),
                              hovertemplate="%{x|%d.%m.%Y}<br>CTR: %{y:.2%}<extra></extra>"))
    seg3 = df2[(df2["День"] >= b3) & (df2["День"] < b4)]
    fig2.add_trace(go.Scatter(x=seg3["День"], y=seg3["CTR"], mode="lines+markers", name="14.08 – 22.10",
                              line=dict(color="rgba(255,159,67,1)", width=2.2), marker=dict(size=4),
                              hovertemplate="%{x|%d.%m.%Y}<br>CTR: %{y:.2%}<extra></extra>"))
    seg4 = df2[(df2["День"] >= b4) & (df2["День"] <= b5)]
    fig2.add_trace(go.Scatter(x=seg4["День"], y=seg4["CTR"], mode="lines+markers", name="22.10 – 29.10",
                              line=dict(color="rgba(255,221,87,1)", width=2.2), marker=dict(size=4),
                              hovertemplate="%{x|%d.%m.%Y}<br>CTR: %{y:.2%}<extra></extra>"))

    fig2.update_layout(
        height=520, margin=dict(l=20, r=20, t=40, b=40), xaxis_title="Дата", yaxis_title="CTR",
        hovermode="x unified", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig2.update_yaxes(tickformat=".2%")
    st.plotly_chart(fig2, use_container_width=True)

# =====================================================
# 3) СПОРТИВНЫЕ СОБЫТИЯ
# =====================================================
elif page == "Спортивные события":
    min_date = pd.to_datetime("2025-04-23")
    max_date = df_ctr["День"].max()
    st.markdown("<div style='text-align:center;margin-top:0.5rem;margin-bottom:0.5rem;'><b>Фильтры</b></div>", unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1, 2.5, 1])
    with col_c:
        date_from, date_to = st.slider(
            "Диапазон дат",
            min_value=min_date.to_pydatetime(), max_value=max_date.to_pydatetime(),
            value=(min_date.to_pydatetime(), max_date.to_pydatetime()), format="DD.MM.YYYY",
        )
        top_n = st.number_input("Пиков CTR вывести", min_value=3, max_value=50, value=15, step=1)

    date_from = pd.to_datetime(date_from); date_to = pd.to_datetime(date_to)
    df_view = df_ctr[(df_ctr["День"] >= date_from) & (df_ctr["День"] <= date_to)].copy().dropna(subset=["CTR"]).sort_values("День")

    def exact_events_for_day(d: pd.Timestamp) -> str:
        if df_events.empty: return ""
        names = []
        for _, ev in df_events.iterrows():
            if ev["начало"].date() == d.date() or ev["окончание"].date() == d.date():
                names.append(ev["название"])
        return ", ".join(names)

    def interval_events_for_day(d: pd.Timestamp) -> str:
        if df_events.empty: return ""
        names = []
        for _, ev in df_events.iterrows():
            if ev["начало"] <= d <= ev["окончание"]:
                names.append(ev["название"])
        return ", ".join(names)

    df_view["CTR_prev"] = df_view["CTR"].shift(1)
    df_view["CTR_change"] = (df_view["CTR"] - df_view["CTR_prev"]) / df_view["CTR_prev"]
    df_view["Событие (точное)"] = df_view["День"].apply(exact_events_for_day)

    CTR_EVENT_THR = 0.12
    def is_dependent(row):
        if not row["Событие (точное)"]: return False
        if pd.isna(row["CTR_change"]): return False
        return abs(row["CTR_change"]) >= CTR_EVENT_THR
    df_view["dependent_move"] = df_view.apply(is_dependent, axis=1)
    dependent_count = int(df_view["dependent_move"].sum())

    sport_colors = {
        "Хоккей": "rgba(46, 204, 113, 0.12)",
        "Баскетбол": "rgba(52, 152, 219, 0.12)",
        "Футбол": "rgba(231, 76, 60, 0.12)",
        "Теннис": "rgba(155, 89, 182, 0.12)",
        "UFC": "rgba(241, 196, 15, 0.12)",
    }

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_view["День"], y=df_view["CTR"], mode="lines+markers", name="CTR",
                             line=dict(width=2.2, color="rgba(181, 220, 255, 1)"), marker=dict(size=4),
                             hovertemplate="%{x|%d.%m.%Y}<br>CTR: %{y:.2%}<extra></extra>"))

    if not df_events.empty:
        for _, ev in df_events.iterrows():
            if ev["окончание"] < date_from or ev["начало"] > date_to:
                continue
            x0 = max(ev["начало"], date_from); x1 = min(ev["окончание"], date_to)
            fill = sport_colors.get(ev["вид спорта"], "rgba(255,255,255,0.05)")
            fig.add_vrect(x0=x0, x1=x1, fillcolor=fill, layer="below", line_width=0)
            fig.add_vline(x=ev["начало"], line_width=0.8, line_dash="dash", line_color="rgba(255,255,255,0.4)")
            fig.add_annotation(x=x0, y=1.03, xref="x", yref="paper", text=ev["название"], showarrow=False, xanchor="left",
                               font=dict(size=10, color="#ffffff"), textangle=65)

    fig.update_layout(height=560, margin=dict(l=20, r=20, t=90, b=40),
                      xaxis_title="Дата", yaxis_title="CTR", hovermode="x unified",
                      plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    fig.update_xaxes(range=[date_from, date_to], showgrid=False)
    fig.update_yaxes(showgrid=True, zeroline=False, tickformat=".2%")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"**Зависимых сдвигов:** {dependent_count}")

    peaks = df_view.sort_values("CTR", ascending=False).head(top_n).copy()
    peaks["Дата"] = peaks["День"].dt.strftime("%d.%m.%Y")
    peaks["CTR (в %)"] = peaks["CTR"].map(lambda x: f"{x:.2%}")
    peaks["Событие (точное)"] = peaks["День"].apply(exact_events_for_day)
    peaks["События (в интервале)"] = peaks["День"].apply(interval_events_for_day)
    st.markdown("### Пиковые значения CTR")
    st.dataframe(peaks[["Дата","CTR (в %)","Событие (точное)","События (в интервале)"]], use_container_width=True, hide_index=True)

# =====================================================
# 4) ТРАФИК В РАЗДЕЛЕ (CTR vs Просмотры "в разделе")
# =====================================================
elif page == "Трафик в разделе":
    st.markdown("### Трафик в разделе: CTR (красная) и Просмотры (синяя)")

    df_ctr_short = df_ctr[["День", "CTR"]].copy().sort_values("День")
    df_traf = df_section.rename(columns={"Период": "День", "Просмотры": "Просмотры (раздел)"}).copy()
    df_mix = pd.merge(df_ctr_short, df_traf, on="День", how="outer").sort_values("День").reset_index(drop=True)
    min_date = df_mix["День"].min(); max_date = df_mix["День"].max()

    st.markdown("<div style='text-align:center;margin-top:0.5rem;margin-bottom:0.5rem;'><b>Фильтры</b></div>", unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1, 2.5, 1])
    with col_c:
        date_from, date_to = st.slider(
            "Диапазон дат", min_value=min_date.to_pydatetime(), max_value=max_date.to_pydatetime(),
            value=(min_date.to_pydatetime(), max_date.to_pydatetime()), format="DD.MM.YYYY",
        )
        trend_mode = st.radio("Агрегация тренда", options=["По неделям","По месяцам"], index=0, horizontal=True)

    date_from = pd.to_datetime(date_from); date_to = pd.to_datetime(date_to)
    df_view = df_mix[(df_mix["День"] >= date_from) & (df_mix["День"] <= date_to)].copy()

    # График 1: дневные значения
    figx = go.Figure()
    figx.add_trace(go.Scatter(x=df_view["День"], y=df_view["CTR"], mode="lines+markers", name="CTR",
                              line=dict(color="rgba(255,80,80,1)", width=2.2), marker=dict(size=4),
                              hovertemplate="%{x|%d.%m.%Y}<br>CTR: %{y:.2%}<extra></extra>", yaxis="y1"))
    figx.add_trace(go.Scatter(x=df_view["День"], y=df_view["Просмотры (раздел)"], mode="lines+markers", name="Просмотры (раздел)",
                              line=dict(color="rgba(80,140,255,1)", width=2.0), marker=dict(size=3),
                              hovertemplate="%{x|%d.%m.%Y}<br>Просмотры: %{y:,}<extra></extra>", yaxis="y2"))
    figx.update_layout(height=560, margin=dict(l=20, r=20, t=40, b=40),
                       xaxis=dict(title="Дата", range=[date_from, date_to], showgrid=False),
                       yaxis=dict(title="CTR", showgrid=True, zeroline=False, tickformat=".2%"),
                       yaxis2=dict(title="Просмотры (раздел)", overlaying="y", side="right", showgrid=False),
                       hovermode="x unified", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                       legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(figx, use_container_width=True)

    # График 2: тренды
    st.markdown("### Тренды (агрегация)")
    def monthly(df_in): return df_in.set_index("День").resample("MS").agg({"CTR":"mean","Просмотры (раздел)":"sum"}).reset_index()
    def weekly(df_in): 
        out = df_in.set_index("День").resample("W-MON").agg({"CTR":"mean","Просмотры (раздел)":"sum"}).reset_index()
        out["label"] = out["День"].dt.strftime("%d.%m") + "–" + (out["День"]+pd.Timedelta(days=6)).dt.strftime("%d.%m.%Y")
        return out

    agg = weekly(df_view) if trend_mode=="По неделям" else monthly(df_view)
    figm = go.Figure()
    figm.add_trace(go.Scatter(x=agg["День"], y=agg["CTR"], mode="lines+markers", name=f"CTR (ср. за {'неделю' if trend_mode=='По неделям' else 'месяц'})",
                              line=dict(color="rgba(255,80,80,1)", width=2.6), marker=dict(size=5),
                              hovertemplate=("%{x|%d.%m.%Y}" if trend_mode=="По месяцам" else "%{x|%d.%m.%Y}") + "<br>CTR (ср.): %{y:.2%}<extra></extra>", yaxis="y1"))
    figm.add_trace(go.Scatter(x=agg["День"], y=agg["Просмотры (раздел)"], mode="lines+markers", name=f"Просмотры (сумма за {'неделю' if trend_mode=='По неделям' else 'месяц'})",
                              line=dict(color="rgba(80,140,255,1)", width=2.4), marker=dict(size=5),
                              hovertemplate="%{x|%d.%m.%Y}<br>Просмотры: %{y:,}<extra></extra>", yaxis="y2"))
    figm.update_layout(height=520, margin=dict(l=20, r=20, t=30, b=40),
                       xaxis=dict(title="Недели (пн)" if trend_mode=="По неделям" else "Месяцы", showgrid=False),
                       yaxis=dict(title="CTR", showgrid=True, zeroline=False, tickformat=".2%"),
                       yaxis2=dict(title="Просмотры (сумма)", overlaying="y", side="right", showgrid=False),
                       hovermode="x unified", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                       legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(figm, use_container_width=True)

# =====================================================
# 5) ПРОСМОТРЫ (основные)
# =====================================================
elif page == "Просмотры":
    st.markdown("### CTR vs Просмотры (по дням)")
    min_date = pd.to_datetime("2025-04-23"); max_date = df_ctr["День"].max()
    st.markdown("<div style='text-align:center;margin-top:0.5rem;margin-bottom:0.5rem;'><b>Фильтры</b></div>", unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1, 2.5, 1])
    with col_c:
        date_from, date_to = st.slider("Диапазон дат", min_value=min_date.to_pydatetime(), max_value=max_date.to_pydatetime(),
                                       value=(min_date.to_pydatetime(), max_date.to_pydatetime()), format="DD.MM.YYYY")
        top_n = st.number_input("Пиков CTR вывести", min_value=3, max_value=50, value=15, step=1)

    date_from = pd.to_datetime(date_from); date_to = pd.to_datetime(date_to)
    df3 = df_ctr[(df_ctr["День"] >= date_from) & (df_ctr["День"] <= date_to)].copy().dropna(subset=["CTR"]).sort_values("День")
    df3["CTR_prev"] = df3["CTR"].shift(1); df3["Views_prev"] = df3["Просмотры"].shift(1)
    df3["CTR_change"] = (df3["CTR"] - df3["CTR_prev"]) / df3["CTR_prev"]
    df3["Views_change"] = (df3["Просмотры"] - df3["Views_prev"]) / df3["Views_prev"]

    CTR_THR = 0.12; VIEWS_THR = 0.12
    def is_joint3(row):
        if pd.isna(row["CTR_change"]) or pd.isna(row["Views_change"]): return False
        if row["CTR_change"] > CTR_THR and row["Views_change"] > VIEWS_THR: return True
        if row["CTR_change"] < -CTR_THR and row["Views_change"] < -VIEWS_THR: return True
        return False
    df3["joint_move"] = df3.apply(is_joint3, axis=1); joint_days = df3[df3["joint_move"]]

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=df3["День"], y=df3["CTR"], mode="lines+markers", name="CTR",
                              line=dict(color="rgba(102,178,255,1)", width=2.2), marker=dict(size=4),
                              hovertemplate="%{x|%d.%m.%Y}<br>CTR: %{y:.2%}<extra></extra>", yaxis="y1"))
    fig3.add_trace(go.Scatter(x=df3["День"], y=df3["Просмотры"], mode="lines+markers", name="Просмотры",
                              line=dict(color="rgba(255,159,67,1)", width=2.0), marker=dict(size=3),
                              hovertemplate="%{x|%d.%m.%Y}<br>Просмотры: %{y:,}<extra></extra>", yaxis="y2"))
    for _, row in joint_days.iterrows():
        fig3.add_vline(x=row["День"], line_width=1.1, line_dash="dot", line_color="rgba(255,80,80,0.85)")

    fig3.update_layout(height=560, margin=dict(l=20, r=20, t=40, b=40),
                       xaxis=dict(title="Дата", range=[date_from, date_to], showgrid=False),
                       yaxis=dict(title="CTR", showgrid=True, zeroline=False, tickformat=".2%"),
                       yaxis2=dict(title="Просмотры", overlaying="y", side="right", showgrid=False),
                       hovermode="x unified", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                       legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig3, use_container_width=True)

    avg_views = df3["Просмотры"].mean()
    peaks3 = df3.sort_values("CTR", ascending=False).head(top_n).copy()
    peaks3["Дата"] = peaks3["День"].dt.strftime("%d.%m.%Y")
    peaks3["CTR (в %)"] = peaks3["CTR"].map(lambda x: f"{x:.2%}")
    peaks3["Уровень просмотров"] = peaks3["Просмотры"].apply(lambda v: "выше среднего" if v >= avg_views else "ниже среднего")
    st.markdown("### Пиковые значения CTR в выбранный период")
    st.dataframe(peaks3[["Дата","CTR (в %)","Просмотры","Уровень просмотров"]], use_container_width=True, hide_index=True)

# =====================================================
# 6) ДРУГИЕ РК — сравнение CTR
# =====================================================
elif page == "Другие РК":
    st.markdown("### Другие РК: сравнение CTR")

    base = df_ctr[["День", "CTR"]].dropna().copy().sort_values("День")
    series = []
    series.append({"key":"BASE","label":"Основная серия","df":base.copy(),
                   "style":{"dash":"solid","width":2.4,"color":"rgba(52,152,219,1)","marker_size":4}})
    for s in EXTRA_SERIES:
        series.append({"key":f"EXTRA_{s['name']}","label":f"Серия «{s['name']}»",
                       "df": s["df"].copy().dropna().sort_values("День"),
                       "style": s.get("style", {"dash":"dot","width":2.2,"color":"rgba(255,99,132,1)","marker_size":4})})

    min_date = min([s["df"]["День"].min() for s in series if not s["df"].empty])
    max_date = max([s["df"]["День"].max() for s in series if not s["df"].empty])

    st.markdown("<div style='text-align:center;margin-top:0.5rem;margin-bottom:0.5rem;'><b>Фильтры</b></div>", unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1, 2.5, 1])
    with col_c:
        date_from, date_to = st.slider("Диапазон дат", min_value=min_date.to_pydatetime(), max_value=max_date.to_pydatetime(),
                                       value=(min_date.to_pydatetime(), max_date.to_pydatetime()), format="DD.MM.YYYY")

    date_from = pd.to_datetime(date_from); date_to = pd.to_datetime(date_to)

    opt_col1, opt_col2 = st.columns([1, 1.5])
    with opt_col1:
        show_lines = st.radio("Отображение линий совпадений:", ["С линиями","Без линий"], horizontal=True, index=0)
    with opt_col2:
        trend_mode = st.radio("Тренды:", ["По неделям","По месяцам"], horizontal=True, index=0)

    def add_trace(fig, df_src, label, style):
        if df_src.empty: return
        fig.add_trace(go.Scatter(x=df_src["День"], y=df_src["CTR"], mode="lines+markers", name=label,
                                 line=dict(color=style.get("color"), width=style.get("width"), dash=style.get("dash")),
                                 marker=dict(size=style.get("marker_size",4)),
                                 hovertemplate="%{x|%d.%m.%Y}<br>CTR: %{y:.2%}<extra></extra>"))

    def with_sign(df_in: pd.DataFrame) -> pd.DataFrame:
        d = df_in[(df_in["День"] >= date_from) & (df_in["День"] <= date_to)].copy().sort_values("День")
        d["prev"] = d["CTR"].shift(1); d["chg"] = d["CTR"] - d["prev"]
        d["sign"] = d["chg"].apply(lambda v: 1 if pd.notna(v) and v > 0 else (-1 if pd.notna(v) and v < 0 else 0))
        return d[["День","CTR","sign"]]

    series_view = [{**s, "dfv": with_sign(s["df"])} for s in series]

    all_dates = pd.DataFrame({"День": pd.date_range(date_from, date_to, freq="D")})
    signs_df = all_dates.copy()
    for s in series_view:
        col = f"sign_{s['key']}"
        signs_df = signs_df.merge(s["dfv"][["День","sign"]].rename(columns={"sign":col}), on="День", how="left")

    marks_white, marks_green = [], []
    for _, row in signs_df.iterrows():
        vals = [v for k, v in row.items() if str(k).startswith("sign_")]
        vals = [int(v) for v in vals if pd.notna(v) and v != 0]
        if len(vals) < 2: continue
        up = sum(1 for v in vals if v == 1); dn = sum(1 for v in vals if v == -1)
        consensus = max(up, dn)
        if consensus >= 3: marks_green.append(row["День"])
        elif consensus == 2: marks_white.append(row["День"])

    fig = go.Figure()
    for s in series_view:
        add_trace(fig, s["dfv"], s["label"], s["style"])

    if show_lines == "С линиями":
        for d in marks_white:
            fig.add_vline(x=d, line_width=1.2, line_dash="dot", line_color="rgba(255,255,255,0.95)")
        for d in marks_green:
            fig.add_vline(x=d, line_width=1.6, line_dash="solid", line_color="rgba(46,204,113,0.95)")

    fig.update_layout(height=560, margin=dict(l=20, r=20, t=40, b=40),
                      xaxis=dict(title="Дата", range=[date_from, date_to], showgrid=False),
                      yaxis=dict(title="CTR", showgrid=True, zeroline=False, tickformat=".2%"),
                      hovermode="x unified", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig, use_container_width=True)

    if show_lines == "С линиями":
        st.markdown(
            "<div style='color:#94a3b8;margin-top:-0.5rem;margin-bottom:0.7rem;'>"
            "Вертикальные линии: <b style='color:#e5e7eb;'>белая</b> — совпадение тенденции у двух кампаний; "
            "<b style='color:#22c55e;'>зелёная</b> — у трёх и более.</div>", unsafe_allow_html=True
        )

    st.markdown("### Линии тренда")
    def monthly_ctr(df_in: pd.DataFrame) -> pd.DataFrame:
        if df_in.empty: return pd.DataFrame(columns=["Период","CTR"])
        out = df_in[(df_in["День"] >= date_from) & (df_in["День"] <= date_to)].set_index("День").resample("MS").agg({"CTR":"mean"}).reset_index()
        out.rename(columns={"День":"Период"}, inplace=True)
        out["label"] = out["Период"].dt.strftime("%b %Y")
        return out

    def weekly_ctr(df_in: pd.DataFrame) -> pd.DataFrame:
        if df_in.empty: return pd.DataFrame(columns=["Период","CTR"])
        out = df_in[(df_in["День"] >= date_from) & (df_in["День"] <= date_to)].set_index("День").resample("W-MON").agg({"CTR":"mean"}).reset_index()
        out.rename(columns={"День":"Период"}, inplace=True)
        out["Период_конец"] = out["Период"] + pd.Timedelta(days=6)
        out["label"] = out["Период"].dt.strftime("%d.%m") + "–" + out["Период_конец"].dt.strftime("%d.%m.%Y")
        return out

    figm = go.Figure()
    for s in series:
        m = weekly_ctr(s["df"]) if trend_mode=="По неделям" else monthly_ctr(s["df"])
        if m.empty: continue
        stl = s["style"]
        figm.add_trace(go.Scatter(
            x=m["Период"], y=m["CTR"], mode="lines+markers",
            name=f"{s['label']} ({'недели' if trend_mode=='По неделям' else 'месяцы'})",
            line=dict(color=stl.get("color"), width=max(2.4, stl.get("width",2.4)), dash=stl.get("dash","solid")),
            marker=dict(size=5), text=m["label"], hovertemplate="%{text}<br>CTR (ср.): %{y:.2%}<extra></extra>"
        ))

    figm.update_layout(height=520, margin=dict(l=20, r=20, t=30, b=40),
                       xaxis=dict(title="Неделя (пн)" if trend_mode=="По неделям" else "Месяц", showgrid=False),
                       yaxis=dict(title="CTR (ср.)", showgrid=True, zeroline=False, tickformat=".2%"),
                       hovermode="x unified", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                       legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(figm, use_container_width=True)

# =====================================================
# 7) ОБЩИЙ ТРАФИК
# =====================================================
else:  # "Общий трафик"
    st.markdown("### Общий трафик: N / V / O / CTR")

    min_candidates, max_candidates = [], []
    for d in [df_N, df_V, df_O]:
        if not d.empty:
            min_candidates.append(d["date"].min())
            max_candidates.append(d["date"].max())
    if not df_ctr.empty:
        min_candidates.append(df_ctr["День"].min())
        max_candidates.append(df_ctr["День"].max())
    if len(min_candidates) == 0:
        st.warning("Нет данных для отображения."); st.stop()

    min_date = min(min_candidates); max_date = max(max_candidates)
    st.markdown("<div style='text-align:center;margin-top:0.5rem;margin-bottom:0.5rem;'><b>Фильтры</b></div>", unsafe_allow_html=True)
    col_f = st.columns([1, 2.5, 1])[1]
    with col_f:
        date_from, date_to = st.slider("Диапазон дат", min_value=min_date.to_pydatetime(), max_value=max_date.to_pydatetime(),
                                       value=(min_date.to_pydatetime(), max_date.to_pydatetime()), format="DD.MM.YYYY")

    date_from = pd.to_datetime(date_from); date_to = pd.to_datetime(date_to)

    c1, c2, c3, c4 = st.columns(4)
    with c1: show_N = st.checkbox("Показать «Н»", value=not df_N.empty)
    with c2: show_V = st.checkbox("Показать «В»", value=not df_V.empty)
    with c3: show_O = st.checkbox("Показать «О»", value=not df_O.empty)
    with c4: show_CTR = st.checkbox("Показать CTR (основной)", value=True)

    def clip(df, col_date="date"):
        if df.empty: return df
        return df[(df[col_date] >= date_from) & (df[col_date] <= date_to)].copy()

    dfN = clip(df_N, "date"); dfV = clip(df_V, "date"); dfO = clip(df_O, "date")
    dfC = clip(df_ctr.rename(columns={"День": "date", "CTR": "ctr"}), "date")

    fig = go.Figure()
    if show_CTR and not dfC.empty and ("ctr" in dfC.columns):
        fig.add_trace(go.Scatter(x=dfC["date"], y=dfC["ctr"], mode="lines+markers", name="CTR",
                                 line=dict(color="rgba(255,80,80,1)", width=2.4), marker=dict(size=4),
                                 hovertemplate="%{x|%d.%m.%Y}<br>CTR: %{y:.2%}<extra></extra>", yaxis="y1"))

    def add_traffic(df, label, color):
        if df.empty: return
        fig.add_trace(go.Scatter(x=df["date"], y=df["value"], mode="lines+markers", name=label,
                                 line=dict(color=color, width=2.0), marker=dict(size=3),
                                 hovertemplate="%{x|%d.%m.%Y}<br>%{y:,}<extra></extra>", yaxis="y2"))

    if show_N: add_traffic(dfN, "Н", "rgba(102,178,255,1)")
    if show_V: add_traffic(dfV, "В", "rgba(46,204,113,1)")
    if show_O: add_traffic(dfO, "О", "rgba(255,206,86,1)")

    fig.update_layout(height=560, margin=dict(l=20, r=20, t=40, b=40),
                      xaxis=dict(title="Дата", range=[date_from, date_to], showgrid=False),
                      yaxis=dict(title="CTR", showgrid=True, zeroline=False, tickformat=".2%"),
                      yaxis2=dict(title="Трафик, шт.", overlaying="y", side="right", showgrid=False),
                      hovermode="x unified", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig, use_container_width=True)

