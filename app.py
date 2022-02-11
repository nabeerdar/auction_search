import numpy as np
import streamlit as st
import pandas as pd
def main():
    st.title("Dummy Prices Database")

    export_data = pd.read_csv("export.csv",sep=";")

    st.write(export_data)

    just_cap_price = []
    for cap_price in export_data["cap_price"]:
        cap_price = cap_price.replace(',','')
        cap_price = cap_price.replace("‘",'')
        cap_price = cap_price[1:]
        if cap_price[0] == " ":
            cap_price = cap_price[1:-1]
        just_cap_price.append(int(cap_price))

    export_data["just_cap_price"]=just_cap_price
    export_data = export_data.drop("cap_price", axis = 1)

    just_auc_price = []
    for auc_price in export_data["auc_price"].replace(np.nan, 0):

        if type(auc_price) == str:
            auc_price = auc_price.replace(',','')
            auc_price = auc_price[1:].strip()
            just_auc_price.append(int(auc_price))
        else:
            just_auc_price.append(auc_price)
    export_data["just_auc_price"]= just_auc_price
    export_data = export_data.drop("auc_price", axis =1)




    with st.form(key='searchform'):
        nav1, nav2 = st.columns([2,1])

        with nav1:
            search_term = st.text_input("Enter Value",key="search_value")
        with nav2:
            st.text("...")
            submit_search = st.form_submit_button(label='Search')

    sliders = {
        "just_cap_price": st.sidebar.slider(
            "Cap Price", min_value=0, max_value=46800, value=(0, 46800), step=50
        ),
        "just_auc_price": st.sidebar.slider(
            "Auc Price", min_value=0, max_value=40000, value=(0, 40000), step=50
        ),
    }

    filter = np.full(len(export_data), True)  # Initialize filter as only True

    for feature_name, slider in sliders.items():
        # Here we update the filter to take into account the value of each slider
        print("feature name: ", feature_name)
        print("slider", slider)
        filter = (
            filter
            & (export_data[feature_name] >= slider[0])
            & (export_data[feature_name] <= slider[1])
        )

    st.dataframe(export_data[filter].style.highlight_max(axis=0))

    if submit_search:
        st.header("\nSearch Results")
        search_value = st.session_state.search_value

        search_results = dict()
        reg_numbers = []
        current_time_list = []
        cap_prices = []
        auc_prices = []
        for index,row in export_data.iterrows():
            for value in row.values:
                str(value)
                if search_value==value:
                    # st.write(f"value exists at index {index}")
                    filtered_df = export_data[filter].astype(str)
                    indexed_filter = filtered_df.iloc[index]
                    reg_numbers.append(indexed_filter[0])
                    current_time_list.append(indexed_filter[1])
                    cap_prices.append(indexed_filter[2])
                    auc_prices.append(indexed_filter[3])
        search_results['reg_num'] = reg_numbers
        search_results['current_time'] = current_time_list
        search_results['cap_price'] = cap_prices
        search_results['auc_price'] = auc_prices

        search_results_df = pd.DataFrame(search_results)
        st.write(search_results_df)


if __name__ == "__main__":
     main()

