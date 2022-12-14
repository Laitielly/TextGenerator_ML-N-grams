# TextGenerator_ML-N-grams
## Требования к заданию для поступление на Тинькофф Поколение (курсы по МЛ):
Напишите утилиту, которая на основе заданных текстов генерирует новые. 

**Обучение:**
- Считать входные данные из файлов.
- Очистить тексты: выкидывать неалфавитные символы, приводить к lowercase.
- Разбить тексты на слова (в ML это называется токенизацией).
- Сохранить модель в каком-нибудь формате, который позволяет восстановить её в утилите генерации.

**Параметры `train.py`:**
- `--input-dir` − путь к директории, в которой лежит коллекция документов. Если данный аргумент не задан, считать, что тексты вводятся из stdin.
- `--model` − путь к файлу, в который сохраняется модель.

**Генерация:**
- Загрузить модель.
- Инициализировать её каким-нибудь сидом.
- Сгенерировать последовательность нужной длины.
- Вывести её на экран.

**Параметры `generate.py`:**
- `--model` − путь к файлу, из которого загружается модель.
- `--prefix` − необязательный аргумент. Начало предложения (одно или несколько слов). Если не указано, выбираем начальное слово случайно из всех слов.
- `--length` − длина генерируемой последовательности.
- `--seed` − параметр начального номера генератора случайных чисел.

## Детали реализации:
- Консольный интерфейс реализован через `argparse`.
- Для работы с текстами использована библиотека регулярных выражений `re`.
- Для сохранения модели был использован `pickle`.
- Созданы файлы `train.py`, `generate.py`, папка `data` с текстом для обучения 'M_M.txt' и обученная модель `model.pkl`.
- Модель обучена произведениями русских классиков, среди них: "Война и мир", "Мастер и Маргарита", "Евгений Онегин", "Мы" и многие другие.

В работе использованны триграммы, основная идея кода прокомментирована и готова к изучению :)

## Краткая справка: 
### Обучение
Читается файл - текст обрабатывается согласно правилам - делится на триплеты - создается словарь (триграмма) типа {(префикс1, префикс2):[(вероятное слово, вероятность)...],...} - сохраняем обученную модель.
### Генерация
От юзера получают данные про длину, префикс, сид и файл модели - распаковывается модель - согласно префиксу выбирается ключ в модели - генерируется текст.
