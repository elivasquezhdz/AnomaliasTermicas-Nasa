import streamlit as st
import requests
from streamlit_lottie import st_lottie
from PIL import Image
import json
import pandas as pd
import plotly.express as px
import datetime as dt

ciudades = {
    "Acapulco, Mex" : [16.793542,-99.8349],
    "San Jose, Gua" : [13.9234, -91.1628],
    "Acajutla, Sal" : [13.5242, -89.7991],
    "San Rafael Sur, Nic" : [11.8274, -86.5377],
    "Parrita, Cos":[9.4839, -84.2999],
    "Pedasi, Pan":[7.4261, -80.0924],
    "Buenaventura , Col":[3.8461, -77.3266],
    "Perdernales, Ecu":[0.0876, -80.0691],
    "Colán, Per":[-5.0078, -81.0684],
    "Lima, Per":[-12.1085, -77.0831],
    "Antofagasta, Chi" :[-23.6333, -70.4103],
}

epocas = [
    ['19810101', '19911231'],
    ['19920101', '20021231'],
    ['20030101', '20131231'],
    ['20140101', '20230810'],
]

url = "https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M&community=RE&longitude=-70.4103&latitude=-23.6333&start=19810101&end=19911231&format=JSON"

def get_datos(ciudades,epocas):
    df = pd.DataFrame()
    for ciudad, valores in ciudades.items():
        for epoca in epocas:
            print(ciudad + str(epoca))
            url = "https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M&community=RE&longitude="+ str(valores[1]) +"&latitude=" + str(valores[0]) + "&start="+str(epoca[0])+"&end="+str(epoca[1])+"&format=JSON"
            #print(url)
            r = requests.get(url)
            if r.status_code == 200:
                df_q = pd.DataFrame(r.json()['properties']['parameter']['T2M'], index=[0]).T.reset_index()
                print(df_q.head())
                df_q.columns = ['Fecha', 'Temp']
                df_q['Ciudad'] = ciudad
                df_q['Latitud']= valores[0]
                df_q['Longitud']= valores[1]
                df = pd.concat([df,df_q])
            else:
                continue
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Año'] = df['Fecha'].dt.year
    df['Mes'] = df['Fecha'].dt.month
    return df

df = pd.read_csv("Historico_OP_litoral.csv")
df['Fecha'] = pd.to_datetime(df['Fecha'])
df['Año'] = df['Fecha'].dt.year
df['Mes'] = df['Fecha'].dt.month


avg_df = df.groupby([df['Ciudad'], df['Año']], as_index = False).mean()
avg_df = avg_df.iloc[:,0:3]
avg_df.columns = ['Ciudad', 'Año', 'Temp_avg']
df = pd.merge(df,avg_df)

df['Anomalia'] = df['Temp'] - df['Temp_avg']



# Función para nuestra animación
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_coding = load_lottieurl("https://lottie.host/9a195c7f-0740-45e6-be24-e99392f8c207/c6FKaU0eME.json")
#image_video = Image.open('/content/AMEA.png')

st.set_page_config(page_title="Anomalias Termicas", page_icon=":ocean:", layout="wide")

st.sidebar.write("Elige el año inicial y final para mostrar")
ai = st.sidebar.slider('Año Inicial', 1981, 2023,1981)
af = st.sidebar.slider('Año Final', 1981, 2023,2023)

st.sidebar.write("Elige las ciudades")
checkboxes = {}
for ciudad in ciudades:
    checkboxes[ciudad] = st.sidebar.checkbox(ciudad,value=True)
start_date = dt.datetime(ai,1,1,0,0,0)
end_date = dt.datetime(af,1,1,0,0,0)

df = df[df['Fecha']> start_date]
df = df[df['Fecha'] < end_date]

for ciudad in checkboxes:
    if not (checkboxes[ciudad]):
        df= df[df['Ciudad'] != ciudad]



fig1 = px.line(df, x="Fecha", y="Anomalia", color='Ciudad')
fig2 = px.scatter(df, x="Año", y="Temp_avg", trendline="ols", color='Ciudad')


with st.container():
    st.subheader('... 🐧 Vamos a salvar el mundo, ¿te unes? 🐧 ...')
    st.title('Anomalias termicas y El Niño')
    st.write(
        """
        Una anomalía térmica se refiere a una desviación o diferencia
        en la temperatura de un medio (como el agua del océano) en
        relación con un valor de referencia o una media histórica.
        Estas anomalías se utilizan comúnmente en la climatología y
        la oceanografía para estudiar patrones de temperatura y
        cambios en el clima. Las anomalías térmicas pueden ser
        positivas (cuando la temperatura es más cálida de lo normal)
        o negativas (cuando la temperatura es más fría de lo normal).
        """
    )
    st.write("[AMEA](https://linktr.ee/ameamx)")

with st.container():
    st.write('---')
    
    st_lottie(lottie_coding, height=300,key="coding")
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)
with st.container():
    st.write("---")
    st.header("fuente de datos")
    image_column, text_column = st.columns((1,2))
    #with image_column:
        #st.image(image_video)
    with text_column:
        st.write(
            """
            La Agencia Mexicana de Estudios Antárticos facilita la información
            para el mejor entendimiento de los retos humanos y socio-económicos
            que se podrían derivar de fenómenos climatológicos en la Antártida….
            """
        )
        st.markdown("[Ver video...](https://youtu.be/ujsjkBNlY9c?si=XJwibIgOOs12iWyV)")


        st.markdown(
            "[The POWER Project](https://power.larc.nasa.gov/)")
