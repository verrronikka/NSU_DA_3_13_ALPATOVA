# About
Код задачи  выполняет следующее:
  - Создание или чтение временного ряда из файла
  - Вычисление скользящих среднего через rolling и ewm
  - Построение и сохранение графиков статистик

## Структура кода

- `create_time_series(file_path, date_col, value_col)` — чтение из файлов csv, xlsx, xls, txt
- `calculation_moving_average(df, windows, value_col, new_col=None)` — вычисление скользящего среднего через rolling
- `calculation_ewm_moving_average(df, windows, value_col, new_col=None)` — вычисление скользящего среднего через ewm
- `calculation_moving_min(df, window, value_col, new_col=None)` — вычисление скользящего минимума
- `create_new_graphic(df, output_file, format_file, date_col, value_col, new_col)` — создание и сохранение одного графика для конкретной статистики и окна
- `build_graphics(df, output_file, format_file, date_col, value_col, windows, new_col)` — многократный вызов функции для создания и сохранения графика
- `main()` — основная функция
  
## Rolling mean

  `df.rolling(window=5).mean()`
  
  Принцип работы:
-  Использует фиксированное окно из N последних точек
-  Все точки в окне имеют одинаковый вес
-  Начинает работать только после накопления N точек
-  Сильно сглаживает данные, но медленно реагирует на изменения

Формула:
  `Rolling_t = (x_t + x_{t-1} + ... + x_{t-N+1}) / N`
  
Подходит для:
- Анализа долгосрочных трендов
- Сильного сглаживания шумных данных
- Ситуаций, где все данные в периоде одинаково важны
  
## Exponential Moving Average

  `df.ewm(span=5).mean()`
  
   Принцип работы:
-  Экспоненциально убывающие веса - новые данные важнее старых
-  Начинает работать с первой точки
-  Быстро реагирует на изменения в данных
-  Сохраняет "память" о всех предыдущих значениях

Формула:
  `EMA_t = α × x_t + (1-α) × EMA_{t-1}
где α = 2 / (span + 1)`
  
Подходит для:
- Трейдинга и финансового анализа
- Быстрого обнаружения изменений тренда
- Ситуаций, где последние данные наиболее релевантны
  
## Разница между rolling и ewm
| Характеристика  | ROLLING | EWM  |
| ------------- | ------------- | ------------- |
| Память  | Текущее окно  | Все данные  |
| Сглаживание  | Быстрое  | Умеренное  |
| Зависимость  | window  | alpha  |
| Использование | Долгосрочные тренды | Кратковременные тренды |

## Зависимости
  pip install pandas matplotlib
  
## Запуск
  python moving_average.py test.csv -o output --mov-avg "mov_avg" --ewm-avg "ewm_avg" --w 5 --s 5 --format pdf
  
## Вывод программы
  Будет выводить набор графиков от статистик, которые мы указали
  
  Примеры графиков:

<img width="2233" height="1324" alt="image" src="https://github.com/user-attachments/assets/e6a1bbe9-7bfe-4a6b-a8d0-b0379c118836" />
<img width="2278" height="1314" alt="image" src="https://github.com/user-attachments/assets/41d7af2f-aa1c-4955-a312-b54c56ba4265" />


