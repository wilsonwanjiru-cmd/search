# Core Pkgs
import streamlit as st
import streamlit.components.v1 as stc
import requests

# Define the RapidAPI key and host
RAPIDAPI_KEY = '83ce275436msh916daea89d6c100p18d37ajsna89b20bc3648'
RAPIDAPI_HOST = 'jobsearch4.p.rapidapi.com'

base_url = "https://jobsearch4.p.rapidapi.com/api/v2/Jobs/Latest"

# Fxn to Retrieve Data
def get_data(url, headers):
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()  # Check for request errors

        data = resp.json()

        if "data" in data:
            # Extract the actual job data
            job_data = data["data"]
            return job_data
        else:
            st.error("Invalid response format from the API: {}".format(data))
            return None

    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred during the request: {str(e)}")
        return None
    except ValueError as e:
        st.error(f"Error while parsing JSON data: {str(e)}")
        return None

JOB_HTML_TEMPLATE = """
<div style="width:100%;height:100%;margin:1px;padding:5px;position:relative;border-radius:5px;border-bottom-right-radius: 10px;
box-shadow:0 0 1px 1px #eee; background-color: #31333F;
  border-left: 5px solid #6c6c6c;color:white;">
<h4>{}</h4>
<h4>{}</h4>
<h5>{}</h5>
<h6>{}</h6>
</div>
"""

JOB_DES_HTML_TEMPLATE = """
<div style='color:#fff'>
{}
</div>
"""

def main():
    menu = ["Home", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    st.title("DevDeeds - Search Jobs")

    if choice == "Home":
        st.subheader("Home")

        # Nav  Search Form
        with st.form(key='searchform'):
            nav1, nav2, nav3 = st.beta_columns([3, 2, 1])

            with nav1:
                search_term = st.text_input("Search Job")
            with nav2:
                location = st.text_input("Location")

            with nav3:
                st.text("Search ")
                submit_search = st.form_submit_button(label='Search')

        st.success("You searched for {} in {}".format(search_term, location))

        # Results
        col1, col2 = st.beta_columns([2, 1])

        with col1:
            if submit_search:
                # Set the RapidAPI headers
                headers = {
                    'X-RapidAPI-Key': RAPIDAPI_KEY,
                    'X-RapidAPI-Host': RAPIDAPI_HOST
                }

                data = get_data(base_url, headers)

                if data is not None:
                    # Number of Results
                    num_of_results = len(data)
                    st.subheader("Showing {} jobs".format(num_of_results))

                    for i in data:
                        job_title = i['title']
                        job_location = i.get('location', 'Location N/A')
                        company = i.get('company', 'Company N/A')
                        company_url = i.get('url', 'N/A')
                        job_post_date = i.get('dateAdded', 'Date N/A')
                        job_desc = "Description N/A"
                        job_howtoapply = "How to Apply N/A"
                        st.markdown(JOB_HTML_TEMPLATE.format(job_title, company, job_location, job_post_date),
                            unsafe_allow_html=True)

                        # Description
                        with st.beta_expander("Description"):
                            stc.html(JOB_DES_HTML_TEMPLATE.format(job_desc), scrolling=True)

                        # How to Apply
                        with st.beta_expander("How To Apply"):
                            stc.html(JOB_DES_HTML_TEMPLATE.format(job_howtoapply), scrolling=True)

        with col2:
            with st.form(key='email_form'):
                st.write("Be the first to get new jobs info")
                email = st.text_input("Email")

                submit_email = st.form_submit_button(label='Subscribe')

                if submit_email:
                    st.success("A message was sent to {}".format(email))

    else:
        st.subheader("About")

if __name__ == '__main__':
    main()
