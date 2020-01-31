import os
import json
import requests
import streamlit as st

st.title("Katecheo")

question = st.text_input('Ask a question...', '')

with st.spinner('Wait for it...'):

    # Send the question as part of a POST request to Katecheo
    katecheo_req = requests.post(
        os.environ["KATECHEO_URL"],
        data=json.dumps({
            "data" : {
                "names": ["message"],
                'ndarray': [question]
            }
        }),
        headers={"content-type": "application/json"}
    )

    if katecheo_req.status_code == 200:

        # Parse through the response data from Katecheo
        response = katecheo_req.json()

        if "strData" in response:

            # Katecheo's answer
            answer = response["strData"]

            if answer:
                st.success("Answer: " + answer)

                if "tags" in response["meta"]:
                    tags = response["meta"]["tags"]

                    # Get the topic of the question detected by Katecheo
                    if "topic" in tags and tags["topic"]:
                        st.info("Topic: " + tags["topic"].capitalize())

                    # Get the ID of the article detected by Katecheo
                    if "article_id" in tags and tags["article_id"]:
                        st.info("Article ID: " + tags["article_id"])

                    # Get the model used by Katecheo for comprehension
                    if "comprehension_model" in tags and tags["comprehension_model"]:
                        st.info("Comprehension Model: " + tags["comprehension_model"])

        else:

            # Log the error messages
            if "tags" in response["meta"]:
                tags = response["meta"]["tags"]

                if "question_detector_error" in tags and tags["question_detector_error"]:
                    st.error(tags["question_detector_error"])

                if "on_topic" in tags and not tags["on_topic"]:
                    st.error("The question isn't on topic")

                if "kb_search_error" in tags and tags["kb_search_error"]:
                    st.error(tags["kb_search_error"])
                        
                if "comprehension_error" in tags and tags["comprehension_error"]:
                    st.error(tags["comprehension_error"])
    
