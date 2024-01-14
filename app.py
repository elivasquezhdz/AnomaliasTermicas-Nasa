import streamlit as st
import requests
from streamlit_lottie import st_lottie
from PIL import Image

# Función para nuestra animación
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_coding = load_lottieurl("https://lottie.host/9a195c7f-0740-45e6-be24-e99392f8c207/c6FKaU0eME.json")
#image_video = Image.open('/content/AMEA.png')

st.set_page_config(page_title="Anomalias Termicas", page_icon=":ocean:", layout="wide")

a = st.sidebar.slider('Año', min_value=2000, max_value=2023)

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
    left_column, right_column = st.columns(2)
    with left_column:
        st.header('Acá iran los filtros')
        if st.button('Ayudas o que?'):
            st.write('Eso chingao')
        else:
            st.write('Ve a calentar el planeta')
        st.write("[NASA](https://power.larc.nasa.gov)")

    with right_column:
        st_lottie(lottie_coding, height=300,key="coding")

with st.container():
    st.write("---")
    st.header("fuente de datos")
    image_column, text_column = st.columns((1,2))
    with image_column:
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
