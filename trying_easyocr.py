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
    image = Image.open(image) # дописала, чтобы загруженное img перевести в "путь" к нему (str)
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        p0, p1, p2, p3 = bound[0]
        draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
    return st.image(image)

# ---------------------Header---------------------
st.markdown('''<h1 style='text-align: center; color: black;'
            >Распознавание текста с изображений</h1>''', 
            unsafe_allow_html=True)
# st.markdown('''<h3 style='text-align: right; color: grey;'
#             >Text Recognition from photo</h13>''', 
#             unsafe_allow_html=True)

img_ocr = Image.open('ocr_title.png') #
st.image(img_ocr, use_column_width='auto') # width=450

st.write("""
Лабораторная работа *"Распознавание текста с изображений"* демонстрирует, как можно получать текстовую информацию с изображений или печатных носителей.
\n_Данные подготовили сотрудники ЛИА РАНХиГС._
""")

#-------------------------Актуальность-------------------------
st.markdown('''<h2 style='text-align: center; color: black;'>Актуальность тематики</h2>''',unsafe_allow_html=True)
st.write(""" \n##### **Кому будет полезна эта лабораторная работа и почему?**
\n* **Студентам управленческих специальностей:**
\nДля ознакомления с современными технологиями, оптимизирующими рутинные бизнес-процессы (в т.ч. банковские, бухгалтерские и юридические).
\n* **Студентам, чьи будущие профессии непосредственно связаны с делопроизводством:**
\nПосле прохождения лабораторной работы вы узнаете о сферах, где используют оптическое распознавание символов, познакомитесь с наиболее распространёнными инструментами и сервисами распознавания текста с изображения, 
а также попробуете применить их на практическом примере.
\n* **Студентам факультетов дизайна:**
\nИз лабораторной работы вы узнаете о возможностях извлечения текста с изображений различного формата.
\n* **Студентам отделений филологии и перевода:**
\nТак как данная технология полезна при работе с историческими данными и архивными документами.
\n* **Студентам других специальностей:**
\nДля общего понимания современных технологий в сфере работы с документами и их оцифровки.
""")

#-------------------------Pipeline description-------------------------
st.markdown('''<h2 style='text-align: center; color: black;'
            >Этапы разработки кейса</h2>''', 
            unsafe_allow_html=True)
img_pipeline = Image.open('Pipeline_for_OCR.png') #
st.image(img_pipeline, use_column_width='auto', caption='Общий пайплайн') #width=450

pipeline_bar = st.expander("Описание пайплайна лабораторной работы:")
pipeline_bar.markdown(
    """
    \n**Этапы:**
    \n_(зелёным обозначены этапы, работа с которыми доступна студенту, красным - этапы, доступные для корректировки сотрудникам ЛИА)_
    \n1. Выбор библиотеки OCR:
    \n*EasyOCR* была выбрана по следующим причинам:
    \n* открытый исходный код
    \n* простота использования 
    \n* доступная и удобная документация
    \n* широко применяется для задач OCR
    \n* высокая точность распознавания текста (до 100%, в зависимости от качества фото/скана)
    \n[Библиотека EasyOCR](https://github.com/JaidedAI/EasyOCR)
    \n2. Написание функций обработки изображения: 
    \nфункции преобразования загруженного изображения в типа данных, доступный для приёма моделью, функции риования границ текста
    \nС использованием языка [Python](https://www.python.org/), библиотек [Streamlit](https://docs.streamlit.io/library/get-started), [cv2](https://opencv.org/), [Numpy](https://numpy.org/doc/stable/reference/index.html)
    \n3. Загрузка изображения с текстом: 
    \nс использованием библиотеки [Streamlit](https://docs.streamlit.io/library/get-started)
    \n4. Выбор языка для определения: 
    \nязык определяется пользователем
    \n5. Обработка изображения: 
    \nбиблиотека EasyOCR может быть использована для распознавания текста с изображений более чем на 80 языках. Она использует CRAFT text detector обученный на 24 тыс. изображений текста. Принимает на вход трёхмерный массив чисел (numpy.ndarray), созданый на основе загруженного изображения теста/надписи​
    \n6. Проверка результата и корректировки:
    \nесли результат неудовлетворительный, проводится корректировка гиперпараметров и функций из п.2
    \n7. Оформление микросервиса Streamlit, выгрузка на сервер: 
    \nпроводится сотрудником лаборатории, используется студентами РАНХиГС
    """)

#-------------------------Info-------------------------
st.markdown('''<h2 style='text-align: center; color: black;'
            >Блок 1: Теория</h2>''', 
            unsafe_allow_html=True)
st.write("_Пожалуйста, внимательно ознакомьтесь с информацией ниже:_")
info_bar = st.expander("Что такое оптическое распознавание символов и как это рабоает?")
info_bar.markdown("""\n**Оптическое распознавание символов** (англ. optical character recognition, OCR) — 
механический или электронный перевод изображений рукописного, машинописного или печатного текста в текстовые данные.
\nЗадача распознавания текстовой информации является одной из важнейших составляющих любого проекта, имеющего целью автоматизацию документооборота или внедрение безбумажных технологий. 
Вместе с тем эта задача является одной из наиболее сложных и наукоемких задач полностью автоматического анализа изображений. Даже человек, читающий рукописный текст, в отрыве от контекста, делает в среднем около 4% ошибок. 
Между тем, в наиболее ответственных приложениях OCR необходимо обеспечивать более высокую надежность распознавания (свыше 99%) даже при плохом качестве печати и оцифровки исходного текста. 
\nВ последние десятилетия, благодаря использованию современных достижений компьютерных технологий, были развиты новые методы обработки изображений и распознавания образов, благодаря чему стало возможным создание промышленных 
систем распознавания печатного текста, которые удовлетворяют основным требованиям систем автоматизации документооборота.
\n**Обработка данных при помощи OCR может применяться для самых различных задач:**
* извлечение данных и размещение в электронной базе банковских, бухгалтерских, юридических документов;
* сканирование печатных документов с последующей возможностью редактирования;
* перенос исторических документов и книг в архивы;
* распределение печатного материала по темам;
* индексирование и поиск отсканированного печатного материала.

\n**Имеется также ряд существенных проблем, связанных с распознаванием рукописных и печатных символов. Наиболее важные из них следующие:**
\n * разнообразие форм начертания символов:
\nrаждый отдельный символ может быть написан различными стандартными шрифтами, например (Times, Gothic, Elite, Courier, Orator), а также - множеством нестандартных шрифтов, используемых в различных предметных областях. 
При этом различные символы могут обладать сходными очертаниями.
\n * искажение изображений символов:
\nшумами печати, смещением символов, изменением их наклона и формы, эффектами освещения (тени, блики и т. п.) при съемке.
\n * вариации размеров и масштаба символов:
\nв зависимости от источника печати. 

\n**В общих словах, процесс оптического распознавания символов (OCP-pipeline) содержит следующие этапы:**

\n1. загрузка изображения/отсканированного документа;
\n2. извлечение слов и строк из изображения;
\n3. распознавание символов в словах и строках;
\n4. формирование электронного документа.

\n**К наиболее популярным сервисам по оптическому распознаванию символов относятся:**
\n**1. [Adobe Acrobat](https://www.adobe.com/)**
\nЭто пакет программ, выпускаемый с 1993 года компанией Adobe Systems и предназначенный для создания и просмотра электронных публикаций в формате PDF.
\n**Плюсы:** Простой в использовании, позволяет редактирвоать текст из pdf-документа, подходит для совместной работы
\n**Минусы**: Adobe Acrobat Pro DC - платная программа с ежемесячной подпиской.
\n**2. [ABBYY FineReader](https://pdf.abbyy.com/)**
\nABBYY FineReader – это универсальное программное приложение для распознавания текста, предназначенное для повышения производительности бизнеса, быстрого захвата документов на бумажных носителях и получения на выходе 
оцифрованных файлв в форматах PDF, DOC и прочих.
\n**Плюсы:** программный продукт предназначен для извлечения, оцифровки, преобразования, редактирования, защиты, совместного использования и совместнуой работы со всеми видами документов на цифровом рабочем месте, 
позволяя таким образом активно использовать данные отсканированных документов в цифровых рабочих процессах.
\n**Минусы**: приложение платное, открытого исходного кода нет.

\n**3. [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)**
\nПрограммное решение Tesseract (рус. Тессеракт) с открытым исходным кодом от компании Google предназначено для распознавания символов с поддержкой кодировки Unicode и возможностью распознавания более 130 языков, а также 
с возможностью дополнения для распознавания других языков. Программа распространяется бесплатно и доступна для использования 
по лицензии Apache 2. 0.
\n**Плюсы:** бесплатное распространение, открытый исходный код, может быть использовано при помощи API
\n**Минусы**: не имеет встроенного графического интерфейса (GUI), т.е. обращаться к программе придётся через написание кода, что совсем не удобно для рядового пользователя.

\n**4. [EasyOCR](https://www.jaided.ai/easyocr/)**
\n EasyOCR развивается как новая система оптического распознавания текста, поддерживающая более 80 языков, включая латынь, китайский, арабский языки и кириллицу. Код написан на языке Python c использованием фреймворка PyTorch и распространяется под лицензией Apache 2.0.
\n**Плюсы:** Точность определения свыше 99% (зависит от качества изображения). Устойчив к плохо пропечатанным, "ломаным" символам, разным шрифрам и их размерам. Также разделяет «связанные» символы и разделяет текст по параграфам. Бесплатное распространение, открытый исходный код, 
\n**Минусы**: так как это библиотека на языке Python, также не имеет встроенного графического интерфейса, но установка и работа с библиотекой достаточно легка.


\n**Полезные ссылки по теме:** [Наиболее распространённые варианты OCR](https://habr.com/ru/post/573030/), [о системе EasyOCR](https://www.jaided.ai/easyocr/tutorial/), [Документация EasyOCR](https://www.jaided.ai/easyocr/documentation/)

""")

# ---------------------Uploading img---------------------
st.markdown('''<h2 style='text-align: center; color: black;'
            >Блок 2: Распознавание текста 
            \n(c использованием библиотеки EasyOCR)</h2>''', 
            unsafe_allow_html=True) 
st.markdown('''##### В этом блоке вы попробуете использовать библиотеку EasyOCR для распознавания текста с изображений.
\nДля этого:
\n(1) Выберете и загрузите изображение в формате jpg, png или pdf. Это может быть скан документа, снимок страницы книги, фотография вывески и др.
\n(2) Выберете язык для распознавания. Библиотека EasyOCR работает более, чем с 80 языками. Для простоты, в нашей лабораторной работе мы ограничились 21 из них:''')
with st.expander('...список из 21 языка'):
    st.markdown('''
    \n'ar' - арабский,
    \n'az' - азербайджанский,
    \n'be' - беларусский,
    \n'bg' - болгарский,
    \n'ch_tra' - традиционный китайский,
    \n'che' - чеченский,
    \n'cs' - чешский,
    \n'de' - немецкий,
    \n'en' - английский,
    \n'es' - испанский,
    \n'fr' - французский,
    \n'hi' - хинди,
    \n'hu' - венгерский,
    \n'it' - итальянский,
    \n'ja' - японский, 
    \n'la' - латынь,
    \n'pl' - польский,
    \n'ru' - русский,
    \n'tr' - турецкий,
    \n'uk' - украинский,
    \n'vi' - вьетнамский.
    ''')
st.markdown('''Полный же список распознаваемых EasyOCR языков смотрите [тут](https://www.jaided.ai/easyocr/#Supported%20Languages).
\n(3) После выбора языка начнётся его распознавание на изображении. Это занимает некоторое время.
\nВ начале распознавания вы увидете обработанное изображение с ограничивающими рамками (bounding boxes) вокруг тех участков, где нейронная сеть нашла буквы. 
Далее выведется сам распознанный текст.

\n_Обратите внимание:_
1. чем чётче загруженное изображение, тем точнее будет определён текст на нём
2. учитывайте также и особенности изображения: старославянскую рукопись библиотека не распознает, это задача для нейронных сетей более сложной архитектуры
3. при загрузке больших документов, время обработки существенно увеличится
4. неверный выбор языка для определения также может быть причиной ошибок''')
uploaded_img = st.file_uploader("Ниже загрузите изображение с текстом:", type=['jpg', 'jpeg', 'png'])
if uploaded_img is not None: 
    st.image(uploaded_img, use_column_width='auto', caption=f'Загруженное изображение {uploaded_img.name}')
    file_bytes = np.asarray(bytearray(uploaded_img.read()), dtype=np.uint8) # переводим в numpy.ndarray
    bytearray_img = cv2.imdecode(file_bytes, 1) # переводим в numpy.ndarray
    # st.write(bytearray_img.shape)
    # st.write(type(bytearray_img))

# ---------------------Choosing language---------------------
languages = ['ar','az','be','bg','ch_tra','che','cs','de','en','es','fr','hi','hu','it','ja','la','pl','ru','tr','uk','vi']
chose_lang = st.multiselect('Выберите язык для распознавания:', languages)

if not chose_lang or not uploaded_img:
    st.write('_Обработка приостановлена: загрузите изображение и/или выберите язык для распознавания._')
else:
    reader = easyocr.Reader(chose_lang)
    bounds = reader.readtext(bytearray_img) # работает c bytearray_img

    draw_boxes(uploaded_img, bounds) # работает c im
    result = reader.readtext(bytearray_img, detail = 0, paragraph=True)
    
    st.markdown('**Распознанный текст:**')
    result


st.markdown('''<h2 style='text-align: center; color: black;'
            >Блок 3: Контрольные вопросы по лабораторной работе</h2>''', 
            unsafe_allow_html=True) 
st.markdown('''##### Выберете все правильные ответы и нажмите кнопку "Закончить тест и посмотреть результаты": ''')            
with st.form('Ответьте на все вопросы, чтобы успешно завершить лабораторную работу'):
    st.markdown('**Вопрос 1:** Где применяется оптическое распознавание символов?')
    question_1_right_1 = st.checkbox('В электронном документообороте', value=False, key='1')
    question_1_right_2 = st.checkbox('В юриспруденции', value=False, key='2')
    question_1_right_3 = st.checkbox('При оцифровке архивных документов', value=False, key='3')
    question_1_right_4 = st.checkbox('Для автоматизации рутинных процессов, связанных с поиском и индексированием отсканированного печатного материала', value=False, key='4')
    question_1_right_5 = st.checkbox('При редактировании pdf-документов', value=False, key='5')
    question_1_wrong_6 = st.checkbox('При посещении окулиста', value=False, key='55')

    st.markdown('**Вопрос 2:** В чём преимущества использования технологии OCR?')
    question_2_wrong_1 = st.checkbox('Экономия электроэнергии на предприятии', value=False, key='6')
    question_2_right_2 = st.checkbox('Высвобождение ресурсов, затраченных на рутинные процессы', value=False, key='7')
    question_2_wrong_3 = st.checkbox('Обучение персонала новым технологиям', value=False, key='8')
    question_2_right_4 = st.checkbox('Ускорение труда, ранее осуществляемого вручную', value=False, key='9')

    st.markdown('**Вопрос 3:** Что может понижать качество распознавания текста?')
    question_3_right_1 = st.checkbox('Нечёткая печать, неровные границы букв', value=False, key='10')
    question_3_right_2 = st.checkbox('Использование при печати нестандартных шрифтов', value=False, key='11')
    question_3_right_3 = st.checkbox('Шумы, тени и блики на изображении', value=False, key='12')
    question_3_wrong_4 = st.checkbox('Повышенная контрастность печати', value=False, key='13')

    st.markdown('**Вопрос 4:** Что из перечисленного относится к сервисам оптического распознавания символов?')
    question_4_wrong_1 = st.checkbox('OCR', value=False, key='14')
    question_4_right_2 = st.checkbox('Tesseract', value=False, key='15')
    question_4_right_3 = st.checkbox('ABBYY FineReader', value=False, key='16')
    question_4_right_4 = st.checkbox('EasyOCR', value=False, key='17')
    question_4_wrong_5 = st.checkbox('Computer Vision', value=False, key='18')

    st.markdown('**Вопрос 5:** Какие недостатки есть у библиотеки EasyOCR?')
    question_5_right_1 = st.checkbox('Нет отдельного графического интерфейса', value=False, key='19')
    question_5_wrong_2 = st.checkbox('Необходимо знание языка C++', value=False, key='20')
    question_5_wrong_3 = st.checkbox('Занимает много свободной памяти компьютера', value=False, key='21')
    question_5_wrong_4 = st.checkbox('Не поддерживает русский язык', value=False, key='22')

    if st.form_submit_button('Закончить тест и посмотреть результаты'):
        if question_1_right_1 and question_1_right_2 and question_1_right_3 and question_1_right_4 and question_1_right_5 and question_2_right_2 and question_2_right_4 and question_3_right_1 and question_3_right_2 and question_3_right_3 and question_4_right_2 and question_4_right_3 and question_4_right_4 and question_5_right_1:
            st.markdown('''<h3 style='text-align: left; color: green;'
            >Тест сдан! Лабораторная работа завершена.</h3>''', 
            unsafe_allow_html=True) 
        else:
            st.markdown('''<h3 style='text-align: left; color: red;'
            >Тест не сдан! Где-то была допущена ошибка.</h3>''', 
            unsafe_allow_html=True) 


    













        
        
        
       
