import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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
# ДАННЫЕ (из «Новая таблица 10»)
# -----------------------------------------------------
CTR_DATA = [
    {"День": "2025-04-23", "Просмотры": 265237, "CTR": 0.0054},
    {"День": "2025-04-24", "Просмотры": 426884, "CTR": 0.0051},
    {"День": "2025-04-25", "Просмотры": 413081, "CTR": 0.0049},
    {"День": "2025-04-26", "Просмотры": 481718, "CTR": 0.0069},
    {"День": "2025-04-27", "Просмотры": 623013, "CTR": 0.0064},
    {"День": "2025-04-28", "Просмотры": 472590, "CTR": 0.0050},
    {"День": "2025-04-29", "Просмотры": 500183, "CTR": 0.0048},
    {"День": "2025-04-30", "Просмотры": 517238, "CTR": 0.0042},
    {"День": "2025-05-01", "Просмотры": 244971, "CTR": 0.0036},
    {"День": "2025-05-02", "Просмотры": 371701, "CTR": 0.0038},
    {"День": "2025-05-03", "Просмотры": 437894, "CTR": 0.0029},
    {"День": "2025-05-04", "Просмотры": 561845, "CTR": 0.0049},
    {"День": "2025-05-05", "Просмотры": 476233, "CTR": 0.0034},
    {"День": "2025-05-06", "Просмотры": 471161, "CTR": 0.0037},
    {"День": "2025-05-07", "Просмотры": 471216, "CTR": 0.0040},
    {"День": "2025-05-08", "Просмотры": 485460, "CTR": 0.0037},
    {"День": "2025-05-09", "Просмотры": 422336, "CTR": 0.0030},
    {"День": "2025-05-10", "Просмотры": 454709, "CTR": 0.0039},
    {"День": "2025-05-11", "Просмотры": 558409, "CTR": 0.0037},
    {"День": "2025-05-12", "Просмотры": 565616, "CTR": 0.0034},
    {"День": "2025-05-13", "Просмотры": 547357, "CTR": 0.0030},
    {"День": "2025-05-14", "Просмотры": 526545, "CTR": 0.0033},
    {"День": "2025-05-15", "Просмотры": 535184, "CTR": 0.0038},
    {"День": "2025-05-16", "Просмотры": 516963, "CTR": 0.0031},
    {"День": "2025-05-17", "Просмотры": 500540, "CTR": 0.0037},
    {"День": "2025-05-18", "Просмотры": 462166, "CTR": 0.0049},
    {"День": "2025-05-19", "Просмотры": 538880, "CTR": 0.0037},
    {"День": "2025-05-20", "Просмотры": 541629, "CTR": 0.0036},
    {"День": "2025-05-21", "Просмотры": 527592, "CTR": 0.0035},
    {"День": "2025-05-22", "Просмотры": 460450, "CTR": 0.0035},
    {"День": "2025-05-23", "Просмотры": 467756, "CTR": 0.0031},
    {"День": "2025-05-24", "Просмотры": 534840, "CTR": 0.0035},
    {"День": "2025-05-25", "Просмотры": 506351, "CTR": 0.0035},
    {"День": "2025-05-26", "Просмотры": 522780, "CTR": 0.0030},
    {"День": "2025-05-27", "Просмотры": 478067, "CTR": 0.0033},
    {"День": "2025-05-28", "Просмотры": 509517, "CTR": 0.0031},
    {"День": "2025-05-29", "Просмотры": 531466, "CTR": 0.0034},
    {"День": "2025-05-30", "Просмотры": 524913, "CTR": 0.0029},
    {"День": "2025-05-31", "Просмотры": 462039, "CTR": 0.0040},
    {"День": "2025-06-01", "Просмотры": 465341, "CTR": 0.0044},
    {"День": "2025-06-02", "Просмотры": 535146, "CTR": 0.0033},
    {"День": "2025-06-03", "Просмотры": 560600, "CTR": 0.0035},
    {"День": "2025-06-04", "Просмотры": 559671, "CTR": 0.0031},
    {"День": "2025-06-05", "Просмотры": 575665, "CTR": 0.0031},
    {"День": "2025-06-06", "Просмотры": 561396, "CTR": 0.0034},
    {"День": "2025-06-07", "Просмотры": 465010, "CTR": 0.0046},
    {"День": "2025-06-08", "Просмотры": 508173, "CTR": 0.0041},
    {"День": "2025-06-09", "Просмотры": 567428, "CTR": 0.0034},
    {"День": "2025-06-10", "Просмотры": 531868, "CTR": 0.0031},
    {"День": "2025-06-11", "Просмотры": 523310, "CTR": 0.0034},
    {"День": "2025-06-12", "Просмотры": 469664, "CTR": 0.0042},
    {"День": "2025-06-13", "Просмотры": 502609, "CTR": 0.0034},
    {"День": "2025-06-14", "Просмотры": 472580, "CTR": 0.0044},
    {"День": "2025-06-15", "Просмотры": 525757, "CTR": 0.0043},
    {"День": "2025-06-16", "Просмотры": 591741, "CTR": 0.0034},
    {"День": "2025-06-17", "Просмотры": 558300, "CTR": 0.0030},
    {"День": "2025-06-18", "Просмотры": 619877, "CTR": 0.0027},
    {"День": "2025-06-19", "Просмотры": 504746, "CTR": 0.0029},
    {"День": "2025-06-20", "Просмотры": 507177, "CTR": 0.0031},
    {"День": "2025-06-21", "Просмотры": 529465, "CTR": 0.0038},
    {"День": "2025-06-22", "Просмотры": 557972, "CTR": 0.0036},
    {"День": "2025-06-23", "Просмотры": 720505, "CTR": 0.0029},
    {"День": "2025-06-24", "Просмотры": 557098, "CTR": 0.0030},
    {"День": "2025-06-25", "Просмотры": 553033, "CTR": 0.0031},
    {"День": "2025-06-26", "Просмотры": 542082, "CTR": 0.0029},
    {"День": "2025-06-27", "Просмотры": 555067, "CTR": 0.0028},
    {"День": "2025-06-28", "Просмотры": 541955, "CTR": 0.0037},
    {"День": "2025-06-29", "Просмотры": 559450, "CTR": 0.0035},
    {"День": "2025-06-30", "Просмотры": 571918, "CTR": 0.0028},
    {"День": "2025-07-01", "Просмотры": 542226, "CTR": 0.0033},
    {"День": "2025-07-02", "Просмотры": 550525, "CTR": 0.0031},
    {"День": "2025-07-03", "Просмотры": 538977, "CTR": 0.0034},
    {"День": "2025-07-04", "Просмотры": 559607, "CTR": 0.0031},
    {"День": "2025-07-05", "Просмотры": 546075, "CTR": 0.0037},
    {"День": "2025-07-06", "Просмотры": 556872, "CTR": 0.0035},
    {"День": "2025-07-07", "Просмотры": 559247, "CTR": 0.0033},
    {"День": "2025-07-08", "Просмотры": 550701, "CTR": 0.0030},
    {"День": "2025-07-09", "Просмотры": 546590, "CTR": 0.0031},
    {"День": "2025-07-10", "Просмотры": 538504, "CTR": 0.0031},
    {"День": "2025-07-11", "Просмотры": 547488, "CTR": 0.0032},
    {"День": "2025-07-12", "Просмотры": 518794, "CTR": 0.0036},
    {"День": "2025-07-13", "Просмотры": 532777, "CTR": 0.0033},
    {"День": "2025-07-14", "Просмотры": 566576, "CTR": 0.0033},
    {"День": "2025-07-15", "Просмотры": 553796, "CTR": 0.0030},
    {"День": "2025-07-16", "Просмотры": 551008, "CTR": 0.0030},
    {"День": "2025-07-17", "Просмотры": 557916, "CTR": 0.0031},
    {"День": "2025-07-18", "Просмотры": 543210, "CTR": 0.0032},
    {"День": "2025-07-19", "Просмотры": 534881, "CTR": 0.0037},
    {"День": "2025-07-20", "Просмотры": 560954, "CTR": 0.0033},
    {"День": "2025-07-21", "Просмотры": 565443, "CTR": 0.0032},
    {"День": "2025-07-22", "Просмотры": 560722, "CTR": 0.0030},
    {"День": "2025-07-23", "Просмотры": 547406, "CTR": 0.0032},
    {"День": "2025-07-24", "Просмотры": 579756, "CTR": 0.0032},
    {"День": "2025-07-25", "Просмотры": 546727, "CTR": 0.0033},
    {"День": "2025-07-26", "Просмотры": 545462, "CTR": 0.0033},
    {"День": "2025-07-27", "Просмотры": 577077, "CTR": 0.0034},
    {"День": "2025-07-28", "Просмотры": 580362, "CTR": 0.0032},
    {"День": "2025-07-29", "Просмотры": 588064, "CTR": 0.0031},
    {"День": "2025-07-30", "Просмотры": 581064, "CTR": 0.0031},
    {"День": "2025-07-31", "Просмотры": 544739, "CTR": 0.0035},
    {"День": "2025-08-01", "Просмотры": 520185, "CTR": 0.0035},
    {"День": "2025-08-02", "Просмотры": 501907, "CTR": 0.0039},
    {"День": "2025-08-03", "Просмотры": 482822, "CTR": 0.0040},
    {"День": "2025-08-04", "Просмотры": 669837, "CTR": 0.0025},
    {"День": "2025-08-05", "Просмотры": 576567, "CTR": 0.0027},
    {"День": "2025-08-06", "Просмотры": 642780, "CTR": 0.0028},
    {"День": "2025-08-07", "Просмотры": 673041, "CTR": 0.0029},
    {"День": "2025-08-08", "Просмотры": 566337, "CTR": 0.0026},
    {"День": "2025-08-09", "Просмотры": 576441, "CTR": 0.0032},
    {"День": "2025-08-10", "Просмотры": 535174, "CTR": 0.0035},
    {"День": "2025-08-11", "Просмотры": 652811, "CTR": 0.0028},
    {"День": "2025-08-12", "Просмотры": 581944, "CTR": 0.0030},
    {"День": "2025-08-13", "Просмотры": 574248, "CTR": 0.0027},
    {"День": "2025-08-14", "Просмотры": 571454, "CTR": 0.0025},
    {"День": "2025-08-15", "Просмотры": 609677, "CTR": 0.0026},
    {"День": "2025-08-16", "Просмотры": 553333, "CTR": 0.0034},
    {"День": "2025-08-17", "Просмотры": 543042, "CTR": 0.0033},
    {"День": "2025-08-18", "Просмотры": 593552, "CTR": 0.0030},
    {"День": "2025-08-19", "Просмотры": 604993, "CTR": 0.0029},
    {"День": "2025-08-20", "Просмотры": 585223, "CTR": 0.0029},
    {"День": "2025-08-21", "Просмотры": 565594, "CTR": 0.0031},
    {"День": "2025-08-22", "Просмотры": 561710, "CTR": 0.0031},
    {"День": "2025-08-23", "Просмотры": 573074, "CTR": 0.0034},
    {"День": "2025-08-24", "Просмотры": 576296, "CTR": 0.0036},
    {"День": "2025-08-25", "Просмотры": 639742, "CTR": 0.0030},
    {"День": "2025-08-26", "Просмотры": 628276, "CTR": 0.0028},
    {"День": "2025-08-27", "Просмотры": 682482, "CTR": 0.0038},
    {"День": "2025-08-28", "Просмотры": 634092, "CTR": 0.0030},
    {"День": "2025-08-29", "Просмотры": 649224, "CTR": 0.0028},
    {"День": "2025-08-30", "Просмотры": 618085, "CTR": 0.0030},
    {"День": "2025-08-31", "Просмотры": 587591, "CTR": 0.0031},
    {"День": "2025-09-01", "Просмотры": 716232, "CTR": 0.0028},
    {"День": "2025-09-02", "Просмотры": 639847, "CTR": 0.0029},
    {"День": "2025-09-03", "Просмотры": 662381, "CTR": 0.0027},
    {"День": "2025-09-04", "Просмотры": 634538, "CTR": 0.0029},
    {"День": "2025-09-05", "Просмотры": 630812, "CTR": 0.0027},
    {"День": "2025-09-06", "Просмотры": 599470, "CTR": 0.0031},
    {"День": "2025-09-07", "Просмотры": 631420, "CTR": 0.0033},
    {"День": "2025-09-08", "Просмотры": 682262, "CTR": 0.0027},
    {"День": "2025-09-09", "Просмотры": 657384, "CTR": 0.0028},
    {"День": "2025-09-10", "Просмотры": 636123, "CTR": 0.0026},
    {"День": "2025-09-11", "Просмотры": 648090, "CTR": 0.0027},
    {"День": "2025-09-12", "Просмотры": 609418, "CTR": 0.0029},
    {"День": "2025-09-13", "Просмотры": 617821, "CTR": 0.0035},
    {"День": "2025-09-14", "Просмотры": 617338, "CTR": 0.0033},
    {"День": "2025-09-15", "Просмотры": 672473, "CTR": 0.0029},
    {"День": "2025-09-16", "Просмотры": 679641, "CTR": 0.0027},
    {"День": "2025-09-17", "Просмотры": 633946, "CTR": 0.0029},
    {"День": "2025-09-18", "Просмотры": 656208, "CTR": 0.0027},
    {"День": "2025-09-19", "Просмотры": 654711, "CTR": 0.0028},
    {"День": "2025-09-20", "Просмотры": 637633, "CTR": 0.0033},
    {"День": "2025-09-21", "Просмотры": 642665, "CTR": 0.0031},
    {"День": "2025-09-22", "Просмотры": 669762, "CTR": 0.0027},
    {"День": "2025-09-23", "Просмотры": 660455, "CTR": 0.0030},
    {"День": "2025-09-24", "Просмотры": 672452, "CTR": 0.0027},
    {"День": "2025-09-25", "Просмотры": 660577, "CTR": 0.0027},
    {"День": "2025-09-26", "Просмотры": 679489, "CTR": 0.0026},
    {"День": "2025-09-27", "Просмотры": 653993, "CTR": 0.0031},
    {"День": "2025-09-28", "Просмотры": 635230, "CTR": 0.0033},
    {"День": "2025-09-29", "Просмотры": 696249, "CTR": 0.0026},
    {"День": "2025-09-30", "Просмотры": 652620, "CTR": 0.0026},
    {"День": "2025-10-01", "Просмотры": 652261, "CTR": 0.0026},
    {"День": "2025-10-02", "Просмотры": 663432, "CTR": 0.0026},
    {"День": "2025-10-03", "Просмотры": 642417, "CTR": 0.0028},
    {"День": "2025-10-04", "Просмотры": 538845, "CTR": 0.0036},
    {"День": "2025-10-05", "Просмотры": 564007, "CTR": 0.0035},
    {"День": "2025-10-06", "Просмотры": 691805, "CTR": 0.0025},
    {"День": "2025-10-07", "Просмотры": 636792, "CTR": 0.0026},
    {"День": "2025-10-08", "Просмотры": 641702, "CTR": 0.0027},
    {"День": "2025-10-09", "Просмотры": 658915, "CTR": 0.0026},
    {"День": "2025-10-10", "Просмотры": 611511, "CTR": 0.0028},
    {"День": "2025-10-11", "Просмотры": 623414, "CTR": 0.0032},
    {"День": "2025-10-12", "Просмотры": 614969, "CTR": 0.0031},
    {"День": "2025-10-13", "Просмотры": 656572, "CTR": 0.0027},
    {"День": "2025-10-14", "Просмотры": 652482, "CTR": 0.0026},
    {"День": "2025-10-15", "Просмотры": 651238, "CTR": 0.0025},
    {"День": "2025-10-16", "Просмотры": 643982, "CTR": 0.0027},
    {"День": "2025-10-17", "Просмотры": 615524, "CTR": 0.0029},
    {"День": "2025-10-18", "Просмотры": 632823, "CTR": 0.0030},
    {"День": "2025-10-19", "Просмотры": 643107, "CTR": 0.0029},
    {"День": "2025-10-20", "Просмотры": 638985, "CTR": 0.0028},
    {"День": "2025-10-21", "Просмотры": 614872, "CTR": 0.0025},
    {"День": "2025-10-22", "Просмотры": 610813, "CTR": 0.0026},
    {"День": "2025-10-23", "Просмотры": 687987, "CTR": 0.0027},
    {"День": "2025-10-24", "Просмотры": 603319, "CTR": 0.0024},
    {"День": "2025-10-25", "Просмотры": 0, "CTR": None},
    {"День": "2025-10-26", "Просмотры": 0, "CTR": None},
    {"День": "2025-10-27", "Просмотры": 966724, "CTR": 0.002456},
    {"День": "2025-10-28", "Просмотры": 587150, "CTR": 0.002381},
    {"День": "2025-10-29", "Просмотры": 316702, "CTR": 0.003499},
]

df_ctr = pd.DataFrame(CTR_DATA)
df_ctr["День"] = pd.to_datetime(df_ctr["День"])
df_ctr = df_ctr.sort_values("День").reset_index(drop=True)

# -----------------------------------------------------
# СПОРТСОБЫТИЯ
# -----------------------------------------------------
EVENTS = [
    {"начало": "2025-03-26", "окончание": "2025-05-25", "название": "Плей-офф КХЛ", "вид спорта": "Хоккей"},
    {"начало": "2025-04-15", "окончание": "2025-06-22", "название": "Плей-офф НБА", "вид спорта": "Баскетбол"},
    {"начало": "2025-04-19", "окончание": "2025-06-23", "название": "Плей-офф НХЛ", "вид спорта": "Хоккей"},
    {"начало": "2025-04-26", "окончание": "2025-04-26", "название": "Эль Классико (апрель)", "вид спорта": "Футбол"},
    {"начало": "2025-05-09", "окончание": "2025-05-25", "название": "Чемпионат мира по хоккею", "вид спорта": "Хоккей"},
    {"начало": "2025-05-11", "окончание": "2025-05-11", "название": "Эль Классико (май)", "вид спорта": "Футбол"},
    {"начало": "2025-05-24", "окончание": "2025-05-24", "название": "Заключительный тур РПЛ", "вид спорта": "Футбол"},
    {"начало": "2025-05-25", "окончание": "2025-06-07", "название": "Теннис «Ролан Гаррос»", "вид спорта": "Теннис"},
    {"начало": "2025-05-31", "окончание": "2025-05-31", "название": "Финал Лиги чемпионов", "вид спорта": "Футбол"},
    {"начало": "2025-06-14", "окончание": "2025-07-13", "название": "Клубный чемпионат мира", "вид спорта": "Футбол"},
    {"начало": "2025-06-29", "окончание": "2025-06-29", "название": "UFC 317", "вид спорта": "UFC"},
    {"начало": "2025-06-30", "окончание": "2025-07-13", "название": "Теннис «Уимблдон»", "вид спорта": "Теннис"},
    {"начало": "2025-07-18", "окончание": "2025-10-29", "название": "Старт сезона РПЛ", "вид спорта": "Футбол"},
    {"начало": "2025-08-02", "окончание": "2025-10-29", "название": "Старт сезона АПЛ", "вид спорта": "Футбол"},
    {"начало": "2025-08-15", "окончание": "2025-10-29", "название": "Старт сезона Ла Лиги", "вид спорта": "Футбол"},
    {"начало": "2025-08-17", "окончание": "2025-08-17", "название": "UFC 319", "вид спорта": "UFC"},
    {"начало": "2025-08-25", "окончание": "2025-09-07", "название": "Теннис US Open", "вид спорта": "Теннис"},
    {"начало": "2025-08-27", "окончание": "2025-09-14", "название": "Баскетбол Евро-2025 (М)", "вид спорта": "Баскетбол"},
    {"начало": "2025-10-04", "окончание": "2025-10-04", "название": "UFC 320", "вид спорта": "UFC"},
    {"начало": "2025-10-07", "окончание": "2025-10-29", "название": "Старт сезона НХЛ", "вид спорта": "Хоккей"},
    {"начало": "2025-10-21", "окончание": "2025-10-29", "название": "Старт сезона НБА", "вид спорта": "Баскетбол"},
    {"начало": "2025-10-26", "окончание": "2025-10-26", "название": "Эль Классико (октябрь)", "вид спорта": "Футбол"},
]
df_events = pd.DataFrame(EVENTS)
df_events["начало"] = pd.to_datetime(df_events["начало"])
df_events["окончание"] = pd.to_datetime(df_events["окончание"])

# -----------------------------------------------------
# ВИЗУАЛЬНЫЙ СЕЛЕКТОР СТРАНИЦ
# -----------------------------------------------------
with st.container():
    st.markdown(
        """
        <style>
        .page-pill {
            display:inline-block;
            margin-right:0.5rem;
            margin-bottom:0.4rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='margin-bottom:0.4rem;font-weight:500;'>Выбор раздела</div>",
        unsafe_allow_html=True,
    )
    page = st.radio(
        "",
        (
            "1. Спортивные события",
            "2. Смена креативов",
            "3. Просмотры",
            "4. Итоги",
        ),
        horizontal=True,
        label_visibility="collapsed",
    )

# =====================================================
# 1. СПОРТИВНЫЕ СОБЫТИЯ
# =====================================================
if page == "1. Спортивные события":
    min_date = pd.to_datetime("2025-04-23")
    max_date = df_ctr["День"].max()

    st.markdown(
        "<div style='text-align:center;margin-top:0.5rem;margin-bottom:0.5rem;'><b>Фильтры</b></div>",
        unsafe_allow_html=True,
    )
    col_l, col_c, col_r = st.columns([1, 2.5, 1])
    with col_c:
        date_from, date_to = st.slider(
            "Диапазон дат",
            min_value=min_date.to_pydatetime(),
            max_value=max_date.to_pydatetime(),
            value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
            format="DD.MM.YYYY",
        )
        top_n = st.number_input(
            "Пиков CTR вывести",
            min_value=3,
            max_value=50,
            value=15,
            step=1,
        )

    date_from = pd.to_datetime(date_from)
    date_to = pd.to_datetime(date_to)

    df_view = df_ctr[(df_ctr["День"] >= date_from) & (df_ctr["День"] <= date_to)].copy()
    df_view = df_view.dropna(subset=["CTR"]).sort_values("День")

    def exact_events_for_day(d: pd.Timestamp) -> str:
        names = []
        for _, ev in df_events.iterrows():
            if ev["начало"].date() == d.date() or ev["окончание"].date() == d.date():
                names.append(ev["название"])
        return ", ".join(names)

    def interval_events_for_day(d: pd.Timestamp) -> str:
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
        if not row["Событие (точное)"]:
            return False
        if pd.isna(row["CTR_change"]):
            return False
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
    fig.add_trace(
        go.Scatter(
            x=df_view["День"],
            y=df_view["CTR"],
            mode="lines+markers",
            name="CTR",
            line=dict(width=2.2, color="rgba(181, 220, 255, 1)"),
            marker=dict(size=4),
            hovertemplate="%{x|%d.%m.%Y}<br>CTR: %{y:.2%}<extra></extra>",
        )
    )

    for _, ev in df_events.iterrows():
        if ev["окончание"] < date_from or ev["начало"] > date_to:
            continue
        x0 = max(ev["начало"], date_from)
        x1 = min(ev["окончание"], date_to)
        fill = sport_colors.get(ev["вид спорта"], "rgba(255,255,255,0.05)")

        fig.add_vrect(
            x0=x0,
            x1=x1,
            fillcolor=fill,
            layer="below",
            line_width=0,
        )
        fig.add_vline(
            x=ev["начало"],
            line_width=0.8,
            line_dash="dash",
            line_color="rgba(255,255,255,0.4)",
        )
        fig.add_annotation(
            x=x0,
            y=1.03,
            xref="x",
            yref="paper",
            text=ev["название"],
            showarrow=False,
            xanchor="left",
            font=dict(size=10, color="#ffffff"),
            textangle=65,
        )

    fig.update_layout(
        height=560,
        margin=dict(l=20, r=20, t=90, b=40),
        xaxis_title="Дата",
        yaxis_title="CTR",
        hovermode="x unified",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_xaxes(range=[date_from, date_to], showgrid=False)
    fig.update_yaxes(showgrid=True, zeroline=False, tickformat=".2%")

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        f"**Зависимых сдвигов:** {dependent_count}"
    )

    peaks = df_view.sort_values("CTR", ascending=False).head(top_n).copy()
    peaks["Дата"] = peaks["День"].dt.strftime("%d.%m.%Y")
    peaks["CTR (в %)"] = peaks["CTR"].map(lambda x: f"{x:.2%}")
    peaks["Событие (точное)"] = peaks["День"].apply(exact_events_for_day)
    peaks["События (в интервале)"] = peaks["День"].apply(interval_events_for_day)

    st.markdown("### Пиковые значения CTR")
    st.dataframe(
        peaks[["Дата", "CTR (в %)", "Событие (точное)", "События (в интервале)"]],
        use_container_width=True,
        hide_index=True,
    )

# =====================================================
# 2. СМЕНА КРЕАТИВОВ
# =====================================================
elif page == "2. Смена креативов":
    st.markdown("### CTR по этапам кампании (смены креативов)")

    b1 = pd.to_datetime("2025-04-23")
    b2 = pd.to_datetime("2025-07-07")
    b3 = pd.to_datetime("2025-08-14")
    b4 = pd.to_datetime("2025-10-22")
    b5 = pd.to_datetime("2025-10-29")

    df2 = df_ctr.dropna(subset=["CTR"]).copy()

    fig2 = go.Figure()

    seg1 = df2[(df2["День"] >= b1) & (df2["День"] < b2)]
    fig2.add_trace(
        go.Scatter(
            x=seg1["День"],
            y=seg1["CTR"],
            mode="lines+markers",
            name="23.04 – 07.07",
            line=dict(color="rgba(141,181,255,1)", width=2.2),
            marker=dict(size=4),
            hovertemplate="%{x|%d.%m.%Y}<br>CTR: %{y:.2%}<extra></extra>",
        )
    )

    seg2 = df2[(df2["День"] >= b2) & (df2["День"] < b3)]
    fig2.add_trace(
        go.Scatter(
            x=seg2["День"],
            y=seg2["CTR"],
            mode="lines+markers",
            name="07.07 – 14.08",
            line=dict(color="rgba(102,204,153,1)", width=2.2),
            marker=dict(size=4),
            hovertemplate="%{x|%d.%m.%Y}<br>CTR: %{y:.2%}<extra></extra>",
        )
    )

    seg3 = df2[(df2["День"] >= b3) & (df2["День"] < b4)]
    fig2.add_trace(
        go.Scatter(
            x=seg3["День"],
            y=seg3["CTR"],
            mode="lines+markers",
            name="14.08 – 22.10",
            line=dict(color="rgba(255,159,67,1)", width=2.2),
            marker=dict(size=4),
            hovertemplate="%{x|%d.%m.%Y}<br>CTR: %{y:.2%}<extra></extra>",
        )
    )

    seg4 = df2[(df2["День"] >= b4) & (df2["День"] <= b5)]
    fig2.add_trace(
        go.Scatter(
            x=seg4["День"],
            y=seg4["CTR"],
            mode="lines+markers",
            name="22.10 – 29.10",
            line=dict(color="rgba(255,221,87,1)", width=2.2),
            marker=dict(size=4),
            hovertemplate="%{x|%d.%m.%Y}<br>CTR: %{y:.2%}<extra></extra>",
        )
    )

    fig2.update_layout(
        height=520,
        margin=dict(l=20, r=20, t=40, b=40),
        xaxis_title="Дата",
        yaxis_title="CTR",
        hovermode="x unified",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig2.update_yaxes(tickformat=".2%")
    st.plotly_chart(fig2, use_container_width=True)

    def make_window(df, center_date, days=3):
        win = df[(df["День"] >= center_date - pd.Timedelta(days=days)) &
                 (df["День"] <= center_date + pd.Timedelta(days=days))].copy()
        win["Дата"] = win["День"].dt.strftime("%d.%m.%Y")
        win["CTR (в %)"] = win["CTR"].map(lambda x: f"{x:.2%}")
        return win[["Дата", "CTR (в %)"]]

    def render_small_table(df_table, title, highlight_date, color_hex):
        st.markdown(f"**{title}**")
        html = "<table style='width:100%;max-width:260px;border-collapse:collapse;font-size:0.85rem;'>"
        html += (
            "<tr>"
            "<th style='text-align:left;padding:4px 6px;border-bottom:1px solid #555;'>Дата</th>"
            "<th style='text-align:right;padding:4px 6px;border-bottom:1px solid #555;'>CTR</th>"
            "</tr>"
        )
        target_str = highlight_date.strftime("%d.%m.%Y")
        for _, row in df_table.iterrows():
            bg = ""
            if row["Дата"] == target_str:
                bg = f"background-color:{color_hex};"
            html += (
                f"<tr style='{bg}'>"
                f"<td style='padding:3px 6px;'>{row['Дата']}</td>"
                f"<td style='padding:3px 6px;text-align:right;'>{row['CTR (в %)']}</td>"
                f"</tr>"
            )
        html += "</table>"
        st.markdown(html, unsafe_allow_html=True)

    win_b1 = make_window(df2, b1, 3)
    win_b2 = make_window(df2, b2, 3)
    win_b3 = make_window(df2, b3, 3)
    win_b4 = make_window(df2, b4, 3)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_small_table(win_b1, "1 ФЛАЙТ", b1, "#8DB5FF55")
    with c2:
        render_small_table(win_b2, "2 ФЛАЙТ", b2, "#66CC9955")
    with c3:
        render_small_table(win_b3, "3 ФЛАЙТ", b3, "#FF9F4355")
    with c4:
        render_small_table(win_b4, "4 ФЛАЙТ", b4, "#FFDD5755")

# =====================================================
# 3. ПРОСМОТРЫ
# =====================================================
elif page == "3. Просмотры":
    st.markdown("### CTR vs Просмотры (по дням)")

    min_date = pd.to_datetime("2025-04-23")
    max_date = df_ctr["День"].max()

    st.markdown(
        "<div style='text-align:center;margin-top:0.5rem;margin-bottom:0.5rem;'><b>Фильтры</b></div>",
        unsafe_allow_html=True,
    )

    col_l, col_c, col_r = st.columns([1, 2.5, 1])
    with col_c:
        date_from, date_to = st.slider(
            "Диапазон дат",
            min_value=min_date.to_pydatetime(),
            max_value=max_date.to_pydatetime(),
            value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
            format="DD.MM.YYYY",
        )
        top_n = st.number_input(
            "Пиков CTR вывести",
            min_value=3,
            max_value=50,
            value=15,
            step=1,
        )

    date_from = pd.to_datetime(date_from)
    date_to = pd.to_datetime(date_to)

    df3 = df_ctr[(df_ctr["День"] >= date_from) & (df_ctr["День"] <= date_to)].copy()
    df3 = df3.dropna(subset=["CTR"]).sort_values("День")

    df3["CTR_prev"] = df3["CTR"].shift(1)
    df3["Views_prev"] = df3["Просмотры"].shift(1)
    df3["CTR_change"] = (df3["CTR"] - df3["CTR_prev"]) / df3["CTR_prev"]
    df3["Views_change"] = (df3["Просмотры"] - df3["Views_prev"]) / df3["Views_prev"]

    CTR_THR = 0.12
    VIEWS_THR = 0.12

    def is_joint3(row):
        if pd.isna(row["CTR_change"]) or pd.isna(row["Views_change"]):
            return False
        if row["CTR_change"] > CTR_THR and row["Views_change"] > VIEWS_THR:
            return True
        if row["CTR_change"] < -CTR_THR and row["Views_change"] < -VIEWS_THR:
            return True
        return False

    df3["joint_move"] = df3.apply(is_joint3, axis=1)
    joint_days = df3[df3["joint_move"]]

    fig3 = go.Figure()

    fig3.add_trace(
        go.Scatter(
            x=df3["День"],
            y=df3["CTR"],
            mode="lines+markers",
            name="CTR",
            line=dict(color="rgba(102,178,255,1)", width=2.2),
            marker=dict(size=4),
            hovertemplate="%{x|%d.%m.%Y}<br>CTR: %{y:.2%}<extra></extra>",
            yaxis="y1",
        )
    )

    fig3.add_trace(
        go.Scatter(
            x=df3["День"],
            y=df3["Просмотры"],
            mode="lines+markers",
            name="Просмотры",
            line=dict(color="rgba(255,159,67,1)", width=2.0),
            marker=dict(size=3),
            hovertemplate="%{x|%d.%m.%Y}<br>Просмотры: %{y:,}<extra></extra>",
            yaxis="y2",
        )
    )

    for _, row in joint_days.iterrows():
        fig3.add_vline(
            x=row["День"],
            line_width=1.1,
            line_dash="dot",
            line_color="rgba(255,80,80,0.85)",
        )

    fig3.update_layout(
        height=560,
        margin=dict(l=20, r=20, t=40, b=40),
        xaxis=dict(
            title="Дата",
            range=[date_from, date_to],
            showgrid=False,
        ),
        yaxis=dict(
            title="CTR",
            showgrid=True,
            zeroline=False,
            tickformat=".2%",
        ),
        yaxis2=dict(
            title="Просмотры",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        hovermode="x unified",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.markdown(
        f"**Совместных сильных движений (CTR и Просмотры вместе):** {len(joint_days)}"
    )

    avg_views = df3["Просмотры"].mean()
    peaks3 = df3.sort_values("CTR", ascending=False).head(top_n).copy()
    peaks3["Дата"] = peaks3["День"].dt.strftime("%d.%m.%Y")
    peaks3["CTR (в %)"] = peaks3["CTR"].map(lambda x: f"{x:.2%}")
    peaks3["Уровень просмотров"] = peaks3["Просмотры"].apply(
        lambda v: "выше среднего" if v >= avg_views else "ниже среднего"
    )

    st.markdown("### Пиковые значения CTR в выбранный период")
    st.dataframe(
        peaks3[["Дата", "CTR (в %)", "Просмотры", "Уровень просмотров"]],
        use_container_width=True,
        hide_index=True,
    )

# =====================================================
# 4. ИТОГИ
# =====================================================
# =====================================================
# 4. ИТОГИ
# =====================================================
else:
    st.markdown("### Итоги")

    # границы этапов
    stage_1_start = pd.to_datetime("2025-04-23")
    stage_2_start = pd.to_datetime("2025-07-07")
    stage_3_start = pd.to_datetime("2025-08-14")
    stage_4_start = pd.to_datetime("2025-10-22")

    # даты смен креативов
    stage_switches = [
        pd.to_datetime("2025-07-07"),
        pd.to_datetime("2025-08-14"),
        pd.to_datetime("2025-10-22"),
    ]

    # вся база по дням
    df_all = df_ctr.dropna(subset=["CTR"]).copy()
    df_all = df_all.sort_values("День").reset_index(drop=True)

    # глобальные средние
    global_views_mean = df_all["Просмотры"].mean()

    # --- вспомогательные функции ---
    def exact_events_for_day(d: pd.Timestamp) -> str:
        names = []
        for _, ev in df_events.iterrows():
            if ev["начало"].date() == d.date() or ev["окончание"].date() == d.date():
                names.append(ev["название"])
        return ", ".join(names)

    def stage_for_day(d: pd.Timestamp) -> int:
        if d < stage_2_start:
            return 1
        elif d < stage_3_start:
            return 2
        elif d < stage_4_start:
            return 3
        else:
            return 4

    def is_stage_switch_near(d: pd.Timestamp) -> str:
        for sw in stage_switches:
            # только в 7 дней ПОСЛЕ смены
            if sw < d <= sw + pd.Timedelta(days=7):
                return "да"
        return "нет"

    # --- расчёты полей ---
    df_all["Точные события"] = df_all["День"].apply(exact_events_for_day)
    df_all["Этап"] = df_all["День"].apply(stage_for_day)
    df_all["Смена креативов"] = df_all["День"].apply(is_stage_switch_near)
    df_all["Дата"] = df_all["День"].dt.strftime("%d.%m.%Y")
    df_all["CTR (в %)"] = df_all["CTR"].map(lambda x: f"{x:.2%}")

    # глобально выше среднего по просмотрам
    df_all["Просмотры выше среднего"] = df_all["Просмотры"].apply(
        lambda v: "да" if v >= global_views_mean else "нет"
    )

    # --- локальные средние (±7 дней) для просмотров и CTR ---
    min_day = df_all["День"].min()
    max_day = df_all["День"].max()

    local_views_means = []
    local_ctr_means = []
    ctr_local_flags = []

    for _, row in df_all.iterrows():
        cur_day = row["День"]

        date_min = max(min_day, cur_day - pd.Timedelta(days=7))
        date_max = min(max_day, cur_day + pd.Timedelta(days=7))

        window = df_all[(df_all["День"] >= date_min) & (df_all["День"] <= date_max)]

        # локальные просмотры
        lv_mean = window["Просмотры"].mean()
        local_views_means.append(lv_mean)

        # локальный ctr
        lc_mean = window["CTR"].mean()
        local_ctr_means.append(lc_mean)

        ctr_local_flags.append("да" if row["CTR"] >= lc_mean else "нет")

    df_all["Локальное среднее просмотров"] = local_views_means
    df_all["Локальный CTR"] = local_ctr_means
    df_all["CTR выше локального"] = ctr_local_flags

    # --- ТАБЛИЦА 1: дни по CTR выше локального (±7 дней) ---
    df_table_ctr = df_all[df_all["CTR выше локального"] == "да"].copy()
    df_table_ctr = df_table_ctr.sort_values("CTR", ascending=False)

    # метрики для карточек считаем по этой таблице
    events_count = (df_table_ctr["Точные события"] != "").sum()
    views_high_global = (df_table_ctr["Просмотры выше среднего"] == "да").sum()
    rows_ctr_local = len(df_table_ctr)
    stage_switch_count = (df_table_ctr["Смена креативов"] == "да").sum()

    # --- карточки ---
    st.markdown(
        f"""
        <div style="display:flex;gap:1rem;margin-bottom:1rem;flex-wrap:wrap;">
            <div style="background:#1f2937;border:1px solid #374151;border-radius:0.75rem;padding:0.75rem 1rem;min-width:180px;">
                <div style="font-size:0.7rem;color:#9ca3af;">События</div>
                <div style="font-size:1.6rem;font-weight:600;">{events_count}</div>
            </div>
            <div style="background:#1f2937;border:1px solid #374151;border-radius:0.75rem;padding:0.75rem 1rem;min-width:180px;">
                <div style="font-size:0.7rem;color:#9ca3af;">Просмотры выше среднего (глобально)</div>
                <div style="font-size:1.6rem;font-weight:600;">{views_high_global}</div>
            </div>
            <div style="background:#1f2937;border:1px solid #374151;border-radius:0.75rem;padding:0.75rem 1rem;min-width:180px;">
                <div style="font-size:0.7rem;color:#9ca3af;">CTR выше локального (±7 дн)</div>
                <div style="font-size:1.6rem;font-weight:600;">{rows_ctr_local}</div>
            </div>
            <div style="background:#1f2937;border:1px solid #374151;border-radius:0.75rem;padding:0.75rem 1rem;min-width:180px;">
                <div style="font-size:0.7rem;color:#9ca3af;">Смена креативов (+7 дн)</div>
                <div style="font-size:1.6rem;font-weight:600;">{stage_switch_count}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- 1) таблица по CTR ---
    st.markdown("#### 1) Дни по CTR выше локального среднего (±7 дней)")

    cols_ctr = [
        "Дата",
        "CTR (в %)",
        "Локальный CTR",
        "CTR выше локального",
        "Точные события",
        "Просмотры",
        "Просмотры выше среднего",
        "Этап",
        "Смена креативов",
    ]
    cols_ctr = [c for c in cols_ctr if c in df_table_ctr.columns]

    st.dataframe(
        df_table_ctr[cols_ctr],
        use_container_width=True,
        hide_index=True,
    )
    st.markdown(f"**Количество строк:** {len(df_table_ctr)}")

    # --- 2) все дни по убыванию CTR ---
    st.markdown("#### 2) Все дни по убыванию CTR")

    df_table_all = df_all.sort_values("CTR", ascending=False)
    cols_all = [
        "Дата",
        "CTR (в %)",
        "Локальный CTR",
        "CTR выше локального",
        "Точные события",
        "Просмотры",
        "Локальное среднее просмотров",
        "Просмотры выше среднего",
        "Этап",
        "Смена креативов",
    ]
    cols_all = [c for c in cols_all if c in df_table_all.columns]

    st.dataframe(
        df_table_all[cols_all],
        use_container_width=True,
        hide_index=True,
    )



