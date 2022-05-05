import streamlit as st
import easyocr
import cv2
import numpy as np
from io import StringIO 
# from easyocr import Reader
from PIL import Image
from PIL import ImageDraw

# ---------------------Work function---------------------
def draw_boxes(image, bounds, color='yellow', width=2):
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        p0, p1, p2, p3 = bound[0]
        draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
    return image


# ---------------------Header---------------------
st.markdown('''<h1 style='text-align: right; color: grey;'
            >Text Recognition from photo</h1>''', 
            unsafe_allow_html=True)
img_ocr = Image.open('ocr.jpeg') #
st.image(img_ocr, use_column_width='auto') # width=450

st.write("""
Приложение *"Text Recognition from photo"* демонстрирует, как можно получать текстовую информацию с изображений или печатных носителей.
* **Используемые библиотеки:** [Streamlit](https://docs.streamlit.io/library/get-started), [EasyOCR](https://github.com/JaidedAI/EasyOCR), [cv2](https://opencv.org/), [Numpy](https://numpy.org/doc/stable/reference/index.html).
* **Полезные ссылки:** [Наиболее распространённые варианты решений OCR](https://habr.com/ru/post/573030/), [о системе EasyOCR](https://www.jaided.ai/easyocr/tutorial/), [Документация EasyOCR](https://www.jaided.ai/easyocr/documentation/)
\nДанные подготовили сотрудники ЛИА РАНХиГС.
""")

# img_pipeline = Image.open('Pipeline_for_Streamlit.png') #
# st.image(img_pipeline, use_column_width='auto', caption='Общий пайплайн для приложения') #width=450

expander_bar = st.expander("Что такое OCR и как это рабоает?")
expander_bar.markdown("""\n**Оптическое распознавание символов** (англ. optical character recognition, OCR) — 
механический или электронный перевод изображений рукописного, машинописного или печатного текста в текстовые данные.
\n**Обработка данных при помощи OCR может применяться для самых различных задач:**

* извлечение данных и размещение в электронной базе банковских, бухгалтерских, юридических документов;
* сканирование печатных документов с последующей возможностью редактирования;
* перенос исторических документов и книг в архивы;
* распределение печатного материала по темам;
* индексирование и поиск отсканированного печатного материала.

\n**В общих словах, OCR-pipeline содержит следующие этапы:**

\n1. загрузка скана документа;
\n2. извлечение слов и строк из скана;
\n3. распознавание символов в словах и строках;
\n4. формирование электронного документа.

\n**Обратите внимание:** чем чётче загруженное изображение, тем точнее будет определение текста на нём!
""")

# ---------------------Uploading img---------------------
uploaded_img = st.file_uploader("Загрузите изображение с текстом ниже:", type=['jpg', 'jpeg', 'png'])
# uploaded_img_cache = None
if uploaded_img is not None: # and uploaded_img != uploaded_img_cache:
    uploaded_img_cache = uploaded_img
    st.image(uploaded_img, use_column_width='auto', caption=f'Загруженное изображение {uploaded_img.name}')
    file_bytes = np.asarray(bytearray(uploaded_img.read()), dtype=np.uint8) # переводим в numpy.ndarray
    bytearray_img = cv2.imdecode(file_bytes, 1) # переводим в numpy.ndarray

    # im = Image.open(uploaded_img)

# ---------------------Choosing language---------------------
chose_lang = st.multiselect('Выберите язык для распознавания', 
        ['ar', 
        'az',
        'be',
        'bg',
        'ch_sim',
        'che',
        'cs',
        'de',
        'en',
        'es',
        'fr',
        'hi',
        'hu',
        'it',
        'ja',
        'la',
        'pl',
        'ru',
        'tr',
        'uk',
        'vi'])

if not chose_lang or not uploaded_img:
    st.write('Обработка приостановлена: загрузите изображение и/или выберите язык для распознавания.')
else:
    reader = easyocr.Reader(chose_lang)
    bounds = reader.readtext(bytearray_img) # работает c bytearray_img


    # iii = Image.open(uploaded_img)
    # iii_array = np.array(iii) # if you want to pass it to OpenCV

    # def draw_boxes(image, bounds, color='yellow', width=2):
    # immm = Image.open(uploaded_img)
    # st.image(immm)

    # imggg = cv2.imread(uploaded_img)

    # def draw_boxes(image, bounds, color='yellow', width=2):
    # draw = ImageDraw.Draw(image)
    # for bound in bounds:
    #     p0, p1, p2, p3 = bound[0]
    #     draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
    # return image

    # draw_boxes(uploaded_img.name, bounds)
    result = reader.readtext(bytearray_img, detail = 0, paragraph=True)
    st.markdown('Распознанный текст:')
    result
    













        
        
        
       
