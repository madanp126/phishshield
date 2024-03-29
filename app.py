import streamlit as st
import machine_learning as ml
import feature_extraction as fe
from bs4 import BeautifulSoup
import requests as re
import matplotlib.pyplot as plt


st.title('Phishing Website Detection using Machine Learning')
st.write('This ML-based app is developed for educational purposes. Objective of the app is detecting phishing websites using URL features only.'
         ' You can see the details of approach, data set, and feature set if you click on "Project Details" ')


with st.expander("PROJECT DETAILS"):
    st.subheader('Approach')
    st.write('We used _supervised learning_ to classify phishing and legitimate websites. '
             'We used various Machine Learning algorithms for classication of websites. '
             'Different algorithms like Random Forest,Decision Tree,Support Vector Machines, KNN , AdaBoost and Also, we used scikit-learn for the ML models.'
             )
    st.write('For this educational project, '
             'We used data set available on Phishtanka and kaggle.com and defined features, some from the literature and some based on manual analysis. '
             'We used requests library to collect data, BeautifulSoup module to parse and extract features. ')

    st.subheader('Data set')
    st.write('We used _"phishtank.org"_ & _"tranco-list.eu"_ as data sources.')
    st.write('Totally 26584 websites ==> **_16060_ legitimate** websites | **_10524_ phishing** websites')

         
    labels = 'phishing', 'legitimate'
    phishing_rate = int(ml.phishing_df.shape[0] / (ml.phishing_df.shape[0] + ml.legitimate_df.shape[0]) * 100)
    legitimate_rate = 100 - phishing_rate
    sizes = [phishing_rate, legitimate_rate]
    explode = (0.1, 0)
    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, shadow=True, startangle=90, autopct='%1.1f%%')
    ax.axis('equal')
    st.pyplot(fig)
    # ----- !!!!! ----- #

    st.write('Features + URL + Label ==> Dataframe')
    st.markdown('label is 1 for phishing, 0 for legitimate')
    number = st.slider("Select row number to display", 0, 100)
    st.dataframe(ml.legitimate_df.head(number))


    @st.cache
    def convert_df(df):
        # Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(ml.df)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='phishing_legitimate_structured_data.csv',
        mime='text/csv',
    )

    st.subheader('Features')
    st.write('Most of the features are content based and some are URL based features extracted using find_all() method of BeautifulSoup module after parsing html.')

    st.subheader('Results')
    st.write('We used 6 different ML classifiers of scikit-learn and tested them implementing k-fold cross validation.'
             'Firstly obtained their confusion matrices, then calculated their accuracy, precision and recall scores.'
             'Comparison table is below:')
    st.table(ml.df_results)
    st.write('GB --> Gaussian Neive Bayes')  
    st.write('SVM --> Support Vector Machine')
    st.write('DT --> Decision Tree')
    st.write('RF --> Random Forest')
    st.write('AB --> AdaBoost')

    st.write('KN --> K-Neighbours')

with st.expander('EXAMPLE PHISHING URLs:'):
    st.write('https://agricole-connect.pages.dev/')
    st.write('https://tmyvs.blogspot.ug/')
    st.write('https://pgesc0nfrmaccsslog.github.io/')
    st.write('https://mungtgsndj.weebly.com/')

choice = st.selectbox("Please select your machine learning model",
                 [
                     'Gaussian Naive Bayes','Support Vector Machine', 'Decision Tree', 'Random Forest',
                     'AdaBoost', 'K-Neighbours'
                 ]
                )

model = ml.nb_model

if choice == 'Gaussian Naive Bayes':
    model = ml.nb_model
    st.write('GNB model is selected!')
elif choice == 'Support Vector Machine':
    model = ml.svm_model
    st.write('SVM model is selected!')
elif choice == 'Decision Tree':
    model = ml.dt_model
    st.write('DT model is selected!')
elif choice == 'Random Forest':
    model = ml.rf_model
    st.write('RF model is selected!')
elif choice == 'AdaBoost':
    model = ml.ab_model
    st.write('AB model is selected!')
else:
    model = ml.kn_model
    st.write('KN model is selected!')


url = st.text_input('Enter the URL')
if st.button('Check!'):
    try:
        response = re.get(url, verify=False, timeout=4)
        if response.status_code != 200:
            print(". HTTP connection was not successful for the URL: ", url)
        else:
            soup = BeautifulSoup(response.content, "html.parser")
            vector = [fe.create_vector(soup)] 
            result = model.predict(vector)
            if result[0] == 0:
                st.success("This web page seems a legitimate!")
                st.balloons()
            else:
                st.warning("Attention! This web page is a potential PHISHING!")
                st.snow()

    except re.exceptions.RequestException as e:
        print("--> ", e)





