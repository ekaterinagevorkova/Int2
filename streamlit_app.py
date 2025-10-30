import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date

st.set_page_config(page_title="CTR по дням", layout="wide")

st.title("CTR по дням + события")

# =========================
# 1. ДАННЫЕ (пример)
# =========================

# тут ты меняешь на свою загрузку из csv / гугла / бд
# важно: колонка date должна быть datetime
ctr_data = pd.DataFrame({
    "date": pd.date_range("2025-04-23", "2025-10-31", freq="D"),
})
# для примера сгенерим CTR
import numpy as np
np.random.seed(42)
ctr_data["ctr"] = (0.4 + np.random.randn(len(ctr_data)) * 0.05).clip(0.05, 0.9)

# =========================
# 2. ТАБЛИЦА СОБЫТИЙ (как ты дал)
# =========================
events = pd.DataFrame([
    ("2025-03-26", "2025-05-25", "Плей-офф КХЛ", "hockey"),
    ("2025-04-15", "2025-06-22", "Плей-офф НБА", "basket"),
    ("2025-04-19", "2025-06-23", "Плей-офф НХЛ", "hockey"),
    ("2025-04-26", "2025-04-26", "Эль классико (апр)", "football"),
    ("2025-05-09", "2025-05-25", "ЧМ по хоккею", "hockey"),
    ("2025-05-11", "2025-05-11", "Эль классико (май)", "football"),
    ("2025-05-24", "2025-05-24", "Заключительный тур РПЛ", "football"),
    ("2025-05-25", "2025-06-07", "Ролан Гаррос", "tennis"),
    ("2025-05-31", "2025-05-31", "Финал Лиги чемпионов", "football"),
    ("2025-06-14", "2025-07-13", "Клубный ЧМ", "football"),
    ("2025-06-29", "2025-06-29", "UFC 317", "ufc"),
    ("2025-06-30", "2025-07-13", "Уимблдон", "tennis"),
    ("2025-07-18", "2025-07-18", "Старт РПЛ", "football"),
    ("2025-08-02", "2025-08-02", "Старт АПЛ", "football"),
    ("2025-08-15", "2025-08-15", "Старт Ла Лиги", "football"),
    ("2025-08-17", "2025-08-17", "UFC 319", "ufc"),
    ("2025-08-25", "2025-09-07", "US Open", "tennis"),
    ("2025-08-27", "2025-09-14", "Евробаскет (М)", "basket"),
    ("2025-10-04", "2025-10-04", "UFC 320", "ufc"),
    ("2025-10-07", "2025-10-07", "Старт НХЛ", "hockey"),
    ("2025-10-21", "2025-10-21", "Старт НБА", "basket"),
    ("2025-10-26", "2025-10-26", "Эль классико (окт)", "football"),
], columns=["event_start", "event_end", "event_name", "event_type"])

events["event_start"] = pd.to_datetime(events["event_start"])
events["event_end"] = pd.to_datetime(events["event_end"])

# =========================
# 3. ФИЛЬТРЫ ВВЕРХУ
# =========================
col1, col2, col3 = st.columns(3)

min_date = ctr_data["date"].min().date()
max_date = ctr_data["date"].max().date()

with col1:
    from_date = st.date_input("С даты", value=min_date, min_value=min_date, max_value=max_date)

with col2:
    to_date = st.date_input("По дату", value=max_date, min_value=min_date, max_value=max_date)

# фильтруем основной датасет
mask = (ctr_data["date"].dt.date >= from_date) & (ctr_data["date"].dt.date <= to_date)
ctr_filtered = ctr_data.loc[mask].copy()

# события тоже фильтруем по диапазону
events_filtered = events[
    (events["event_end"].dt.date >= from_date) &
    (events["event_start"].dt.date <= to_date)
].copy()

with col3:
    sel_day = st.date_input("Выбрать конкретный день (подсветка)", value=max_date,
                            min_value=min_date, max_value=max_date)

# =========================
# 4. РИСУЕМ
# =========================
fig = go.Figure()

# 4.1 основная линия CTR
fig.add_trace(
    go.Scatter(
        x=ctr_filtered["date"],
        y=ctr_filtered["ctr"],
        mode="lines+markers",
        name="CTR",
        line=dict(color="#D81B60", width=2),
        marker=dict(size=4),
        hovertemplate="%{x|%Y-%m-%d}<br>CTR: %{y:.2%}<extra></extra>",
    )
)

# 4.2 подсветка выбранного дня
sel_day_ts = pd.to_datetime(sel_day)
day_row = ctr_filtered[ctr_filtered["date"] == sel_day_ts]
if not day_row.empty:
    fig.add_trace(
        go.Scatter(
            x=day_row["date"],
            y=day_row["ctr"],
            mode="markers+text",
            name="Выбранный день",
            marker=dict(color="black", size=12, symbol="circle"),
            text=[f"{day_row['ctr'].iloc[0]:.2%}"],
            textposition="top center",
            showlegend=False
        )
    )

# 4.3 диапазоны (плей-оффы и турниры)
for _, row in events_filtered.iterrows():
    # если диапазон больше 1 дня — рисуем vrect
    if row["event_start"].date() != row["event_end"].date():
        fig.add_vrect(
            x0=row["event_start"],
            x1=row["event_end"],
            fillcolor="rgba(0,0,0,0.06)",
            line_width=0,
            layer="below",
            annotation_text=row["event_name"],
            annotation_position="top left",
            annotation_font=dict(size=10),
        )

# 4.4 точечные события (однодневные)
point_events = events_filtered[
    events_filtered["event_start"] == events_filtered["event_end"]
]

if not point_events.empty:
    fig.add_trace(
        go.Scatter(
            x=point_events["event_start"],
            y=[ctr_filtered.set_index("date").reindex(point_events["event_start"]).iloc[i]["ctr"]
               if point_events.iloc[i]["event_start"] in ctr_filtered["date"].values
               else None
               for i in range(len(point_events))
               ],
            mode="markers",
            name="События",
            marker=dict(color="#000", size=9, symbol="diamond"),
            text=point_events["event_name"],
            hovertemplate="%{x|%Y-%m-%d}<br>%{text}<extra></extra>",
        )
    )

# 4.5 оформление
fig.update_layout(
    height=550,
    margin=dict(l=40, r=20, t=40, b=40),
    xaxis=dict(title="Дата"),
    yaxis=dict(title="CTR", tickformat=".0%"),
    hovermode="x unified",
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# 5. ТАБЛИЦА СОБЫТИЙ СНИЗУ
# =========================
with st.expander("Показать события в этом диапазоне"):
    st.dataframe(events_filtered.sort_values("event_start")[["event_start", "event_end", "event_name", "event_type"]])

