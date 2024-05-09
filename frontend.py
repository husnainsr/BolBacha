import streamlit as st
from query import getAnswer
from loadData import mainAddData, clear_database
import os

def main():
    st.title("BolBacha ChatBot 🤖")
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add initial assistant message only for the first time
        st.session_state.messages.append({"role": "assistant", "content": "Hey there! How can I help you today?"})

    # Sidebar menu
    st.sidebar.title("Options")

    # Embedding GIF in the sidebar
    st.sidebar.image("assests\\animaiton.gif", use_column_width=True)

    uploaded_file = st.sidebar.file_uploader("Upload PDF", type="pdf")
    if uploaded_file is not None:
        if st.sidebar.button("Process PDF"):
            # clear_database()
            with st.spinner("Processing PDF..."):
                filename = uploaded_file.name
                if not os.path.exists('data'):
                    os.makedirs('data')
                with open(f"data/{filename}", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                mainAddData()
                # mainAddData(f"data/{filename}")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.container():
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("What's up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.container():
            with st.chat_message("user"):
                st.markdown(prompt)

        with st.spinner("Thinking..."):  # Displaying a spinner while generating the response
            response = getAnswer(prompt)  # Using the getAnswer function
            st.markdown(response)  # Assuming response is a string

        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
