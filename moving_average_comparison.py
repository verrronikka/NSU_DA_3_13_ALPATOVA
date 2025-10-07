import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse
from pathlib import Path

def create_time_series(file_path, date_col, value_col):
    """
    Читает временной ряд из файла csv, xlsx, xls, txt
    
    Args:
        file_path (str): путь к файлу с данными
        date_col (str): название столбца с датами
        value_col (str): название столбца со значениями
    Returns:
        pd.DataFrame: DataFrame с колонками 'date' и 'value'
    Raises:
        FileNotFoundError: если файл не существует
        ValueError: если не поддерживается формат файла
        KeyError: если отсутствуют необходимые колонки
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден")

    file_ext = os.path.splitext(file_path)[1]

    try: 
        if file_ext == '.csv':
            df = pd.read_csv(file_path, parse_dates=[date_col])
        elif file_ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path, parse_dates=[date_col])
        elif file_ext == '.txt':
            df = pd.read_csv(file_path, sep=None, engine='python', parse_dates=[date_col])
        else:
            raise ValueError(f"Неподдерживаемый формат файла: {file_ext}")
        
        if date_col not in df.columns:
            raise KeyError(f"Колонка {date_col}  не найдена в файле")
        if value_col not in df.columns:
            raise KeyError(f"Колонка {value_col} не найдена в файле")
        df[date_col] = pd.to_datetime(df[date_col])

        return df
    except Exception as e:
        raise Exception(f"Ошибка чтения файла: {str(e)}")


def calculation_moving_average(df, windows, value_col, new_col=None):
    """
    Считает скользящее среднее
    
    Args:
        df (pd.DataFrame): DataFrame
        windows (list): размеры окон
        value_col (str): название столбца с значениями
        new_col (str): название для нового столбца
    Returns:
        pd.DataFrame: DataFrame с новыми колонками
    Raises:
        TypeError: если значения не числовые
    """
    try:
        numeric_values = pd.to_numeric(df[value_col], errors='raise')
    except ValueError as e:
        raise TypeError(f"Столбец {value_col} содержит нечисловые значения: {e}")

    for window in windows:
        df[f'{new_col}_{window}'] = df[value_col].rolling(window=window, min_periods=1).mean()

    return df

def calculation_ewm_moving_average(df, spans, value_col, new_col=None):
    """
    Считает экспоненциальное скользящее среднее
    
    Args:
        df (pd.DataFrame): DataFrame
        windows (list): размеры окон
        value_col (str): название столбца с значениями
        new_col (str): название для нового столбца
    Returns:
        pd.DataFrame: DataFrame с новыми колонками
    Raises:
        TypeError: если значения не числовые
    """
    try:
        numeric_values = pd.to_numeric(df[value_col], errors='raise')
    except ValueError as e:
        raise TypeError(f"Столбец {value_col} содержит нечисловые значения: {e}")

    for span in spans:
        df[f'{new_col}_{span}'] = df[value_col].ewm(span=span).mean()

    return df


def create_new_graphic(df, output_file, format_file, date_col, value_col, new_col):
    """
    Создает и сохраняет один график для конкретной статистики
    
    Args:
        df (pd.DataFrame): DataFrame с данными
        output_path (Path): путь для сохранения файла
        format_file (str): формат файла
        date_col (str): название столбца с датами
        value_col (str): название столбца с исходными значениями
        new_col (str): название статистики
        
    Returns:
        plt.Figure: объект фигуры matplotlib
    """

    fig = plt.figure(figsize=(12,6))
    plt.plot(df[date_col], df[value_col], label='Исходные данные', linewidth=2)
    plt.plot(df[date_col], df[new_col], label=new_col, linewidth=2)

    plt.title(f'Временной ряд и {new_col}')
    plt.xlabel(date_col)
    plt.ylabel(value_col)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)

    # создаём полный путь к файлу
    output_path = Path(output_file) / f"{new_col}.{format_file}"

    # убедимся, что директория существует
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # сохраняем график
    plt.savefig(output_path, format=format_file, dpi=300)
    plt.show()

    return fig


def build_graphics(df, output_file, format_file, date_col, value_col, windows, new_col):
    """
    Строит и сохраняет график временного ряда и скользящего среднего (в формате jpg, pdf, png с названием moving_average)
    
    Args:
        df (pd.DataFrame): DataFrame с данными
        output_file (str): директория для сохранения файла
        format_file (str): формат файла
        date_col (str): название столбца с датами
        value_col (str): название столбца с исходными значениями
        windows (list): размеры окон 
        new_col (str): название нового столбца
    Returns:
        list: список объектов фигур matplotlib
    """
    
    figures = []

    for window in windows:

            full_col_name = f'{new_col}_{window}'
            new_fig = create_new_graphic(df, output_file, format_file, date_col, value_col, full_col_name)
            figures.append(new_fig)

    return figures

def main():

    # создание временного ряда

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='Путь к входному файлу')
    parser.add_argument('-o', '--output', default='output', help='Директория для результатов')

    parser.add_argument('-w', '--windows', nargs='+', type=int, default=[5], help='Размеры окон для скользящего среднего (по умолчанию: 5)')
    parser.add_argument('-s', '--spans', nargs='+', type=int, default=[5], help='Значения span для ewm скользящего среднего (по умолчанию: 5)')
    parser.add_argument('--format', default='png', choices=['png', 'pdf', 'jpg'], help='Формат графика')
    parser.add_argument('--date-col', default='date', help='Название столбца с датами (по умолчанию: date)')
    parser.add_argument('--value-col', default='value', help='Название столбца с числовыми значениями (по умолчанию: value)')

    parser.add_argument('--mov-avg', type=str, help='Скользящее среднее с названием столбца')
    parser.add_argument('--ewm-avg', type=str, help='Экспоненциальное скользящее среднее с названием столбца')

    args = parser.parse_args()

    # чтение данных

    df = create_time_series(args.input_file, args.date_col, args.value_col)

    # вычисление скользящих статистик

    df = calculation_moving_average(df, args.windows, args.value_col, args.mov_avg)
    df = calculation_ewm_moving_average(df, args.spans, args.value_col, args.ewm_avg)

    # Построение графиков
    if args.mov_avg:
        figures1 = build_graphics(df, args.output, args.format, args.date_col, args.value_col, args.windows, args.mov_avg)

    if args.ewm_avg:
        figures2 = build_graphics(df, args.output, args.format, args.date_col, args.value_col, args.spans, args.ewm_avg)   

if __name__ == "__main__":
    main()