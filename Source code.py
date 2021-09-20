# LIBRARY USED
import streamlit as st
import requests
from bs4 import BeautifulSoup
import mysql.connector
import pandas as pd
from datacleaner import autoclean
import sweetviz as sv

st.title("Data Analysis Webapp")

# MAIN MENU
Main_Menu=["WEBSCRAPPING","DATABASE","PREPROCESSING","EDA"]
Main_choice=st.sidebar.selectbox("PART",Main_Menu)

                                              # WEBSCRAPPING PART
def WEBSCRAPPING():

    # CREATING SIDEBAR SELECTBOX
    menu = ["INFO", "Scrapping"]
    choice = st.sidebar.selectbox("Menu", menu)

    def Scrapping():
        url = st.text_input("Enter the url here", key='1')
        if url is not None:
            # STEP 1: Getting the request
            r = requests.get(url)
            htmlContent = r.content
            # print(htmlContent)

            # STEP 2: PARSE THE HTML(In a good tree like structure)
            soup = BeautifulSoup(htmlContent, 'html.parser')

            # STEP 3: HTML TREE TRAVERSAL
            a = 1
            b = 2
            c = 3
            d = 4

            # FOR PRODUCT NAME
            nam = st.text_input("Enter name div", key="a")
            name = soup.find_all('div', {"class": nam})
            nm = []
            for i in name:
                nm.append(i.text)
            st.write(len(nm))

            # FOR PRICE
            pri = st.text_input("Enter price div", key="b")
            price = soup.find_all('div', {"class": pri})
            pr = []
            for i in price:
                pr.append(i.text)
            st.write(len(pr))

            # FOR RATINGS
            rat = st.text_input("Enter rating div", key="c")
            rating = soup.find_all('div', {"class": rat})
            rt = []
            for i in range(len(nm)):
                rt.append(rating[i].text)
            st.write(len(rt))

            # FOR DESCRIPTION
            des = st.text_input("Enter the description div", key="d")
            desc = soup.find_all('div', {"class": des})
            dc = []
            for i in desc:
                dc.append(i.text)
            st.write(len(dc))

            # CLEANING  DATA
            f = 6
            cl = st.number_input("new length", key=6)
            NM = nm[0:int(cl)]
            PR = pr[0:int(cl)]
            RT = rt[0:int(cl)]
            DC = dc[0:int(cl)]

            # CONVERTING INTO DATAFRAME
            data = {"Name": NM, "Price": PR, "Description": DC,
                    "Rating": RT}

            df = pd.DataFrame(data)
            st.write(df)

    if choice == "Scrapping":
        Scrapping()

                                                   # DATABASE PART
def DATABASE():

    menu=["INFO","Database"]
    choice=st.sidebar.selectbox("Menu",menu)

    def Database():
        # CONNECTING TO THE MYSQl DB
        a=1
        b=2
        c=3
        host=st.text_input("Enter host name", key="a")
        user=st.text_input("Enter username", key="b")
        password=st.text_input("Enter password", key="c")
        mydb = mysql.connector.connect(
            host,
            user,
            password
        )
        st.write(mydb)

        # 3. CREATING CURSOR AND DATABASE
        d=4
        mydatabase=st.text_input("Enter the new database name",key="d")
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE mydatabase")

        menu1=["active_database","creating_tables","active_tables","inserting_data","running_query"]
        choice1=st.sidebar.selectbox(menu1)

        def active_database():
            # 4. PRINTING THE LIST OF ACTIVATED DATABASES
            mydb=mysql.connector.connect(mydatabase)
            mycursor.execute("SHOW DATABASES")
            for x in mycursor:
                st.write(x)

        def creating_tables():
            # 5. CREATING TABLES
            e=5
            f=6
            mydb = mysql.connector.connect(mydatabase)
            table_name=st.text_input("Enter the table name",key="e")
            table_query=st.text_input("Enter the table query",key="f")
            mycursor.execute("CREATE TABLE table_name (table_query)")

        def active_tables():
            # 5. PRINTING ACTIVE TABLES
            mydb = mysql.connector.connect(mydatabase)
            mycursor.execute("SHOW TABLES")
            for x in mycursor:
                st.write(x)

        def inserting_data():
            # 6. INSERTING DATA THROUGH EXCEL
            g=7
            mydb = mysql.connector.connect(mydatabase)
            tablename_ = st.text_input("Enter your new table name",key="g")
            tablename_ = pd.read_csv()
            tablename_.to_sql('tablename_', mydb, if_exists='append', index=False)

        def running_query():
            # 7. RUNNING MYSQL QUERY
            h=8
            mydb = mysql.connector.connect(mydatabase)
            raw_code=st.text_input("Enter the MYSQL Query",key="h")
            mycursor.execute(raw_code)
            data1 = mycursor.fetchall()

        if choice1=="active_database":
            active_database()
        if choice1=="active_tables":
            active_tables()
        if choice1=="inserting_data":
            inserting_data()
        if choice1=="creating_tables":
            creating_tables()
        if choice1=="running_query":
            running_query()
        if choice=="Database":
            Database()

    if choice=="Database":
        Database()
                                                  # DATAPREPROCESSING PART

def PROPROCESSING():

    # CREATING SLIDEBAR
    menu=["Cleaning","INFO"]
    choice=st.sidebar.selectbox("Menu",menu)

    # UPLOADING CSV FILE
    st.write("UPLOAD DATASET HERE")
    dataset = st.file_uploader("upload file here", type=['csv'])
    if dataset is not None:
        df = pd.read_csv(dataset)
        st.dataframe(df.head())
        st.write("Data uploaded ")


    def preprocessing():

    # INDEX OF NULL VALUES
        i=0
        aa=[]
        for i in range(len(df.columns)):
            result=df[df.columns[i]].isnull().to_numpy().nonzero()
            aa.append(result)
            i=i+1
        st.write("No of columns :",len(df.columns))
        st.write("Indexes :",aa)
        # DELETING NULL VALUES
        j=0
        for j in range(len(df.columns)):
            df.dropna(subset=[df.columns[j]],axis=0,inplace=True)
            j=j+1
        st.dataframe(df)

        l=1
        choice2=st.text_input("(subset, replacing values)",key="9+l")

        def subset():
            x1=int(st.number_input("row parameter",key=12+l))
            x2=int(st.number_input("row parameter",key=14+l))
            y1=int(st.number_input("col parameter",key=13+l))
            y2=int(st.number_input("col parameter",key=15+l))
            df1=df.iloc[x1:x2,y1:y2]
            st.write(df1.shape)

        def replacing():
            col_name2=st.text_input("enter that col name",key=17+l)
            old_value=st.text_input("Enter old value",key=18+l)
            new_value=st.text_input("Enter new value",key=19+l)
            df[col_name2].replace(old_value,new_value,inplace=True)
            st.dataframe(df)
        if choice2=="subset":
            subset()
        if choice2=="replacing values":
            replacing()

    d=4
    choice1=st.text_input("Enter value",key="d")
    if choice1=="preprocessing":
        preprocessing()

                                                     # EDA PART

def EDA():

    menu=["Info","EDA"]
    choice=st.sidebar.selectbox("Menu",menu)

    # EDA USING SWEETVIZ
    def EDA():
        st.subheader("Automated EDA with swetviz")
        dataset = st.file_uploader("upload file here", type = ['csv'])
        if dataset is not None:
            df = pd.read_csv(dataset)
            st.dataframe(df.head())
            report=sv.analyze(df)
            report.show_html()

    def Info():
        st.subheader("Basic Info")
        dataset = st.file_uploader("upload file here", type=['csv'])
        if dataset is not None:
            df = pd.read_csv(dataset)
            i = 1
            ah = "Yes"
            while ah == "Yes":
                task = st.text_input("Enter the task", key=1 + i)
                if task == "info":
                    st.write(df.info)
                if task == "shape":
                    st.write(df.shape)
                if task == "dtypes":
                    st.write(df.dtypes)
                if task == "columns":
                    st.write(df.columns)
                if task == "first 5 rows":
                    st.write(df.head(5))
                if task == "last 5 rows":
                    st.write(df.tail(5))
                if task == "copy":
                    DF = df.copy()
                if task == "df":
                    st.write(df)
                ah = st.text_input("want to continue", key=3 + i)
                i = i + 1


    if choice=="EDA":
        EDA()
    if choice=="Info":
        Info()


if Main_choice=="WEBSCRAPPING":
    WEBSCRAPPING()
if Main_choice=="DATABASE":
    DATABASE()
if Main_choice=="PREPROCESSING":
    PROPROCESSING()
if Main_choice=="EDA":
    EDA()
