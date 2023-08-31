# Copyright 2018-2022 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# ¡Bienvenid@ a nuestra Informe de Fondos de Inversión! 👋")

    st.markdown( 
        """
        Nuestro informe está diseñado para ayudarte a explorar y analizar diversas opciones de fondos de inversión. 👈 Selecciona un filtro en la barra lateral para ver ejemplos de cómo puedes utilizar nuestra aplicación y encontrar los fondos que se ajusten a tus necesidades.
        ### ¿Quieres saber mas?
        - Selecciona el mes que desees
        - Usa los filtros para seleccionar los fondos de la base de datos
        - Los fondos filtrados seran los descargados
        ### ¿Tienes dudas o sugerencias?
        Escribenos al correo: 
    """
    )
    
    st.markdown(
        """
        Gerencia_Desarrollo_Negocio_AM@bancolombia.com.co
        """
    )

if __name__ == "__main__":
    run()
