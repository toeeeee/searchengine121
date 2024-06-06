import streamlit as st
from state import State
from run import load_index, main

def app_main():
    st.title('ICS Search Engine')

    if 'initialized' not in st.session_state:
        st.session_state['initialized'] = True
        st.session_state['data'] = load_index()
        file =  open('tfidf_index.txt', 'r')
        st.session_state['data'].set_main_index(file)

    u_query = st.text_input('Enter a search query:')

    if st.button('Search'):
        results = main(st.session_state['data'], u_query)

        if not results:
            st.warning('No results')
        else:
            for res in results:
                st.write(res)

if __name__ == '__main__':
    app_main()