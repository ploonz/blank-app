import streamlit as st
import pandas as pd

st.set_page_config(page_title="Сегментация клиентов", layout="wide")
BRAZIL_STATES = {
    'AC': 'Acre',
    'AL': 'Alagoas',
    'AP': 'Amapá',
    'AM': 'Amazonas',
    'BA': 'Bahia',
    'CE': 'Ceará',
    'DF': 'Distrito Federal',
    'ES': 'Espírito Santo',
    'GO': 'Goiás',
    'MA': 'Maranhão',
    'MT': 'Mato Grosso',
    'MS': 'Mato Grosso do Sul',
    'MG': 'Minas Gerais',
    'PA': 'Pará',
    'PB': 'Paraíba',
    'PR': 'Paraná',
    'PE': 'Pernambuco',
    'PI': 'Piauí',
    'RJ': 'Rio de Janeiro',
    'RN': 'Rio Grande do Norte',
    'RS': 'Rio Grande do Sul',
    'RO': 'Rondônia',
    'RR': 'Roraima',
    'SC': 'Santa Catarina',
    'SP': 'São Paulo',
    'SE': 'Sergipe',
    'TO': 'Tocantins'
}

@st.cache_data
def load_data():
    return pd.read_csv('final_mb.csv',encoding="utf-8", sep=",", decimal=".")

df = load_data()

st.title("Сегментация клиентов интернет магазина")
col1, col2 = st.columns([1.5, 3])
with col1:
    client_id = st.selectbox(
    "Выберите клиента",
    df['customer_unique_id'].unique(),
    key="client_select"
    )
    
    st.subheader("📋 Информация о клиенте")
    client_data=df[df['customer_unique_id']==client_id]
    avg_price=f"{client_data['price'].mean():.2f}"
    state=BRAZIL_STATES.get(client_data['customer_state'].to_string(index=False).split()[0],client_data['customer_state'].to_string(index=False).split()[0])
    st.metric(f"Штат",f"{state}")
    st.metric(f"Средняя стоимость заказа",f"R${avg_price}")
with col2:
    risk_ent = df[df['customer_unique_id'] == client_id]["clusters"].values[0]
    risk = risk_ent if not pd.isna(risk_ent) else 0
    risk=int(risk)
    if risk==-1:
        st.markdown("Недостаточно информации о клиенте")
    elif risk<=5:
        st.success("🔒 Низкий риск оттока - клиент лоялен")
        st.markdown("Вероятность оттока клиента")
        st.progress(1/20+risk/20)
    elif risk<=11:
        st.warning("⚠️ Средний риск оттока - требуется внимание")
        st.markdown("Вероятность оттока клиента")
        st.progress(1/20+risk/20)
    else:
        st.error("🚨 Высокий риск оттока - срочные действия!")
        st.markdown("Вероятность оттока клиента")
        st.progress(risk/20)

st.markdown("---")

st.subheader("🎯 Рекомендации для клиента")

if risk <= 2:
    st.info("""
    - Поддерживать текущий уровень сервиса
    - Предложить программу лояльности
    - Персонализированные предложения
    """)
elif risk <= 5:
    st.warning("""
    - Анализ причин снижения активности
    - Специальные предложения
    - Опрос удовлетворенности
    """)
else:
    st.error("""
    - Персональный менеджер для работы с клиентом
    - Специальные условия и скидки
    - Глубокий анализ причин оттока
    """)

st.markdown("---")
