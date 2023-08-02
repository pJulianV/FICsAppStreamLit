import numpy as np
import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, JsCode
# from streamlit_autorefresh import st_autorefresh


# cd OneDrive - Grupo Bancolombia\Workspace\FicsAppStreamLit\
# streamlit run pruebaA


from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df







@st.cache_data
def load_data():
    # Create Example DataFrame
    # data = {
    #     "Name": ["Luna", "Waldi", "Milo", "Pixie", "Nelly"],
    #     "Grade": [1, 3, 1, 2, 3],
    # }
    # df = pd.DataFrame(data)
    
    excel_file = "MODELO.xlsb"
    sheet_name = "BD"

    df = pd.read_excel(excel_file,
                    sheet_name= sheet_name,
                    header=0,
                    usecols = "A:AF",
                    )

    df.insert(loc=1, column="Selected", value=True)
    listColumns= df.columns.tolist()
    # mean = df.loc[df["Selected"], listColumns[7]].mean()
    # df["Difference"] = df["Grade"] - mean
    return df

def update_dataframe(input_df):
    # Function updates column "Selected" and calculates column "Difference" depending on column "Selected"

    mean = input_df.loc[input_df["Selected"], "Nombre Negocio"].mean()
    # input_df["Difference"] = np.where(input_df["Selected"].array, input_df["Grade"] - mean, np.nan)


# -----Page Configuration
st.set_page_config(page_title="Test AG-Grid", initial_sidebar_state="collapsed")

#  ----defining session states 
if "example_df" not in st.session_state:
    st.session_state.example_df = load_data()
if "grid_key" not in st.session_state:
    st.session_state.grid_key = 0
if "selected_rows_array" not in st.session_state:
    st.session_state.selected_rows_array = st.session_state.example_df["Selected"].array

st.header("AG-Grid with checkbox for boolean column")



col1, col2 = st.columns(2)
with col1:
    st.write("Dataframe:")
    # st.data_editor
    st.dataframe(st.session_state.example_df)
with col2:
    st.write("AG-Grid:")
    checkbox_renderer = JsCode(
        """
	    class CheckboxRenderer{
	    init(params) {
	        this.params = params;
	        this.eGui = document.createElement('input');
	        this.eGui.type = 'checkbox';
	        this.eGui.checked = params.value;
	        this.checkedHandler = this.checkedHandler.bind(this);
	        this.eGui.addEventListener('click', this.checkedHandler);
	    }
	    checkedHandler(e) {
	        let checked = e.target.checked;
	        let colId = this.params.column.colId;
	        this.params.node.setDataValue(colId, checked);
	    }
	    getGui(params) {
	        return this.eGui;
	    }
	    destroy(params) {
	    this.eGui.removeEventListener('click', this.checkedHandler);
	    }
	    }//end class
    """
    )
    rowStyle_renderer = JsCode(
        """
        function(params) {
            if (params.data.Selected) {
                return {
                    'color': 'black',
                    'backgroundColor': 'pink'
                }
            }
            else {
                return {
                    'color': 'black',
                    'backgroundColor': 'white'
                }
            }
        }; 
    """
    )

    gb = GridOptionsBuilder.from_dataframe(st.session_state.example_df[["Selected", "Nombre Negocio", "Nombre Entidad", "Asset Class"]])
    gb.configure_column("Selected", minWidth=90, maxWidth=90, editable=True, cellRenderer=checkbox_renderer)
    gb.configure_column("Nombre Negocio", minWidth=80, maxWidth=80)
    gb.configure_column("Nombre Entidad", minWidth=75, maxWidth=75)
    gb.configure_selection("multiple", use_checkbox=False)
    gridOptions = gb.build()
    gridOptions["getRowStyle"] = rowStyle_renderer
    ag_grid = AgGrid(
        st.session_state.example_df,
        key=st.session_state.grid_key,
        gridOptions=gridOptions,
        data_return_mode="as_input",
        update_mode="grid_changed",
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
        enable_enterprise_modules=False,
        reload_data=False,
    )



placeholder_sess_state = st.empty()
placeholder_sess_state.write("Session State of selected rows: " + str(list(st.session_state.selected_rows_array)))
placeholder_sess_state2 = st.empty()
placeholder_sess_state2.write("Session State of grid_key: " + str(st.session_state.grid_key))

st.session_state.example_df = ag_grid["data"]

if not np.array_equal(st.session_state.selected_rows_array, st.session_state.example_df["Selected"].array):
    update_dataframe(st.session_state.example_df)
    st.session_state.selected_rows_array = st.session_state.example_df["Selected"].array
    placeholder_sess_state.write("Session State of selected rows: " + str(list(st.session_state.selected_rows_array)))
    placeholder_sess_state2.write("Session State of grid_key: " + str(st.session_state.grid_key))

    st.session_state.grid_key += 1
    st.experimental_rerun()
    # st_autorefresh(interval=((500)), key="dataframerefresh")