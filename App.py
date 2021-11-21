import streamlit as st
import csv
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time
import numpy as np
import cv2


st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 350px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 350px;
        margin-left: -350px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.title('QuizAI')
st.sidebar.subheader(
    'Are you bored with giving quizes and exams online? Do not worry, we got you covered. We have a virtual Quiz built on AI that will give you an amazing experience along with knowledge.')

app_mode = st.sidebar.selectbox('Choose the App mode',
                                ['About App', 'Try the quiz']
                                )


if app_mode == 'About App':
    st.markdown(
        """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 400px;
        margin-left: -400px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    kpj1, kpj2 = st.columns(2)

    with kpj1:
        st.markdown("**What is QuizAI all about?**")
        st.markdown(''' QuizAI is basically an idea of using AI for online educational purposes such as quizes.
        Generally, online tests and quizes seem to be uninteresting.
        This idea will somehow make quizes interesting and students will take more interest in appearing for these.
          
            ''')

    with kpj2:

        st.video(
            r"C:\Users\HP\OneDrive\Desktop\QuizAI\gif.mp4", start_time=0)


elif app_mode == 'Try the quiz':
    st.set_option('deprecation.showfileUploaderEncoding', False)

    Start = st.sidebar.button('Start')

    st.sidebar.markdown('---')
    st.markdown(
        """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 400px;
        margin-left: -400px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("Get, set and Readyyyy!!                 ")

    stframe = st.empty()

    if Start:
        cap = cv2.VideoCapture(0)

        cap.set(3, 4000)
        cap.set(4, 4020)
        detector = HandDetector(detectionCon=0.8)

        class MCQ():
            def __init__(self, data):
                self.question = data[0]
                self.choice1 = data[1]
                self.choice2 = data[2]
                self.choice3 = data[3]
                self.choice4 = data[4]
                self.answer = int(data[5])

                self.userAns = None

            def update(self, cursor, bboxs):
                for x, bbox in enumerate(bboxs):
                    x1, y1, x2, y2 = bbox
                    if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                        self.userAns = x + 1
                        cv2.rectangle(img, (x1, y1), (x2, y2),
                                      (0, 255, 0), cv2.FILLED)

        # Import csv file data
        pathCSV = "Mcqs.csv"
        with open(pathCSV, newline='\n') as f:
            reader = csv.reader(f)
            dataAll = list(reader)[1:]

        # Create Object for each MCQ
        mcqList = []
        for q in dataAll:
            mcqList.append(MCQ(q))

        print("Total MCQ Objects Created:", len(mcqList))

        qNo = 0
        i = 0
        qTotal = len(dataAll)

        while cap.isOpened():
            i += 1
            success, img = cap.read()
            img = cv2.flip(img, 1)
            hands, img = detector.findHands(img, flipType=False
                                            )

            if qNo < qTotal:
                mcq = mcqList[qNo]

                img, bbox = cvzone.putTextRect(
                    img, mcq.question, [100, 100], 2, 2, offset=50, border=5)

                img, bbox1 = cvzone.putTextRect(
                    img, mcq.choice1, [100, 250], 2, 2, offset=50, border=5)

                img, bbox2 = cvzone.putTextRect(
                    img, mcq.choice2, [400, 250], 2, 2, offset=50, border=5)

                img, bbox3 = cvzone.putTextRect(
                    img, mcq.choice3, [100, 400], 2, 2, offset=50, border=5)

                img, bbox4 = cvzone.putTextRect(
                    img, mcq.choice4, [400, 400], 2, 2, offset=50, border=5)

                if hands:
                    lmList = hands[0]['lmList']
                    cursor = lmList[8]
                    length, info = detector.findDistance(lmList[8], lmList[12])
                    print(length)
                    if length < 20:
                        mcq.update(cursor, [bbox1, bbox2, bbox3, bbox4])
                        print(mcq.userAns)
                    if mcq.userAns is not None:
                        time.sleep(0.3)
                        qNo += 1

            else:
                score = 0
                for mcq in mcqList:
                    if mcq.answer == mcq.userAns:
                        score += 1
                score = round((score / qTotal) * 100, 2)
                img, _ = cvzone.putTextRect(img, "Quiz Completed", [
                                            250, 300], 2, 2, offset=50, border=5)

                img, _ = cvzone.putTextRect(img, f'Your Score: {score}%', [
                                            700, 300], 2, 2, offset=50, border=5)

       # Draw Progress Bar

            barValue = 150 + (950 // qTotal) * qNo
            cv2.rectangle(img, (150, 600), (barValue, 650),
                          (0, 255, 0), cv2.FILLED)
            cv2.rectangle(img, (150, 600), (1100, 650), (255, 0, 255), 5)
            img, _ = cvzone.putTextRect(
                img, f'{round((qNo / qTotal) * 100)}%', [1130, 635], 2, 2, offset=16)

            #cv2.imshow("Img", img)
            # cv2.waitKey(1)

            # kpi1, kpi2 = st.columns(2)

            # with kpi1:
            #     st.markdown("**FrameRate**")
            #     kpi1_text = st.markdown("0")

            # with kpi2:
            #     st.markdown("**No of curls**")
            #     kpi2_text = st.markdown("0")

            # with kpi3:
            #     st.markdown("**Image Width**")
            #     kpi3_text = st.markdown("0")

            # st.markdown("<hr/>", unsafe_allow_html=True)

            #     # Dashboard
            #     kpi1_text.write(
            #         f"<h1 style='text-align: center; color: red;'>{int(fps)}</h1>", unsafe_allow_html=True)
            #     kpi2_text.write(
            #         f"<h1 style='text-align: center; color: red;'>{count}</h1>", unsafe_allow_html=True)
            #     kpi3_text.write(
            #         f"<h1 style='text-align: center; color: red;'>{width}</h1>", unsafe_allow_html=True)

            stframe.image(img, channels='BGR', use_column_width=True)
        cap.release()
