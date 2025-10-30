import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import numpy as np


# Функция частотного теста
def frequency_test(sequence):
    X = [(2 * bit - 1) for bit in sequence]
    Sn = sum(X)
    n = len(sequence)
    S = abs(Sn) / (n ** 0.5)
    return S <= 1.82138636, S


# Функция теста на последовательность одинаковых бит
def runs_test(sequence):
    n = len(sequence)
    ones_count = sum(sequence)
    pi = ones_count / n

    if pi == 0 or pi == 1:
        return False, float('inf')  # Невозможная статистика в этом случае

    vn = 1
    for i in range(n - 1):
        if sequence[i] != sequence[i + 1]:
            vn += 1

    s = abs(vn - 2 * n * pi * (1 - pi)) / (2 * np.sqrt(2 * n * pi * (1 - pi)))
    return s <= 1.82138636, s


# Функция для генерации последовательности и сохранения в файл
def generate_and_save_sequence(n, filename="numbers.txt"):
    sequence = [random.choice([0, 1]) for _ in range(n)]
    with open(filename, 'w') as f:
        f.write(''.join(map(str, sequence)))
    return sequence


# Функция для загрузки последовательности из файла
def load_sequence(filename="numbers.txt"):
    try:
        with open(filename, 'r') as f:
            content = f.read().strip()
            return [int(bit) for bit in content]
    except FileNotFoundError:
        return None


# Функция для запуска тестов с учетом примечания
def run_tests():
    try:
        n = int(entry.get())
        if n < 10000:
            messagebox.showwarning("Предупреждение", "Рекомендуемая длина последовательности не менее 10 000 бит")

        # Генерация последовательности
        test_sequence = generate_and_save_sequence(n)

        # Частотный тест (основной тест)
        freq_result, S_freq = frequency_test(test_sequence)

        # Формирование строки с результатами
        results_str = (
            f"Длина последовательности: {n} бит\n"
            f"Сгенерированная последовательность сохранена в файл 'numbers.txt'\n\n"
            f"1. Частотный тест: S = {S_freq:.6f}, {'ПРОШЛА' if freq_result else 'НЕ ПРОШЛА'}.\n"
        )

        # Проверка примечания: если частотный тест не пройден, остальные тесты не выполняются
        if not freq_result:
            results_str += (
                f"\nПРИМЕЧАНИЕ: Последовательность не прошла частотный тест.\n"
                f"Остальные тесты не выполняются, так как последовательность\n"
                f"не является равномерно распределенной.\n\n"
                f"ОБЩИЙ РЕЗУЛЬТАТ: Последовательность НЕСЛУЧАЙНАЯ\n"
            )
        else:
            # Если частотный тест пройден, выполняем тест на последовательность одинаковых бит
            runs_result, S_runs = runs_test(test_sequence)

            results_str += (
                f"2. Тест на последовательность одинаковых бит: S = {S_runs:.6f}, {'ПРОШЛА' if runs_result else 'НЕ ПРОШЛА'}.\n\n"
            )

            # Общий результат
            if runs_result:
                results_str += "ОБЩИЙ РЕЗУЛЬТАТ: Последовательность прошла все тесты\n"
            else:
                results_str += "ОБЩИЙ РЕЗУЛЬТАТ: Последовательность не прошла тесты\n"

        results_text.delete(1.0, tk.END)
        results_text.insert(tk.END, results_str)

    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректное число")


# Функция для загрузки и тестирования последовательности из файла
def load_and_test():
    sequence = load_sequence()
    if sequence is None:
        messagebox.showerror("Ошибка", "Файл 'numbers.txt' не найден")
        return

    n = len(sequence)

    # Частотный тест (основной тест)
    freq_result, S_freq = frequency_test(sequence)

    # Формирование строки с результатами
    results_str = (
        f"Загружена последовательность из файла 'numbers.txt'\n"
        f"Длина последовательности: {n} бит\n\n"
        f"1. Частотный тест: S = {S_freq:.6f}, {'ПРОШЛА' if freq_result else 'НЕ ПРОШЛА'}.\n"
    )

    # Проверка примечания: если частотный тест не пройден, остальные тесты не выполняются
    if not freq_result:
        results_str += (
            f"\nПРИМЕЧАНИЕ: Последовательность не прошла частотный тест.\n"
            f"Остальные тесты не выполняются, так как последовательность\n"
            f"не является равномерно распределенной.\n\n"
            f"ОБЩИЙ РЕЗУЛЬТАТ: Последовательность НЕСЛУЧАЙНАЯ\n"
        )
    else:
        # Если частотный тест пройден, выполняем тест на последовательность одинаковых бит
        runs_result, S_runs = runs_test(sequence)

        results_str += (
            f"2. Тест на последовательность одинаковых бит: S = {S_runs:.6f}, {'ПРОШЛА' if runs_result else 'НЕ ПРОШЛА'}.\n\n"
        )

        # Общий результат
        if runs_result:
            results_str += "ОБЩИЙ РЕЗУЛЬТАТ: Последовательность прошла все тесты\n"
        else:
            results_str += "ОБЩИЙ РЕЗУЛЬТАТ: Последовательность не прошла тесты\n"

    results_text.delete(1.0, tk.END)
    results_text.insert(tk.END, results_str)


# Функция для отображения последовательности
def show_sequence():
    sequence = load_sequence()
    if sequence is None:
        messagebox.showerror("Ошибка", "Файл 'numbers.txt' не найден")
        return

    # Показываем только первые 100 бит для удобства просмотра
    preview = ''.join(map(str, sequence[:100]))
    if len(sequence) > 100:
        preview += f"... (всего {len(sequence)} бит)"

    results_text.delete(1.0, tk.END)
    results_text.insert(tk.END, f"Последовательность (первые 100 бит):\n{preview}")


# Создание главного окна
root = tk.Tk()
root.title("Тестирование псевдослучайных последовательностей")
root.geometry("600x500")

# Создание и размещение элементов интерфейса
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

label = tk.Label(frame_top, text="Введите количество бит для генерации:", padx=10, pady=5)
label.pack()

entry = tk.Entry(frame_top, width=15, bg='beige')
entry.pack(pady=5)

# Фрейм для кнопок
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

btn_generate = tk.Button(frame_buttons, text="Сгенерировать и протестировать",
                         command=run_tests, padx=10, pady=5, bg="lightgreen")
btn_generate.pack(side=tk.LEFT, padx=5)

btn_load = tk.Button(frame_buttons, text="Загрузить и протестировать",
                     command=load_and_test, padx=10, pady=5, bg="lightblue")
btn_load.pack(side=tk.LEFT, padx=5)

btn_show = tk.Button(frame_buttons, text="Показать последовательность",
                     command=show_sequence, padx=10, pady=5, bg="lightyellow")
btn_show.pack(side=tk.LEFT, padx=5)

# Текстовое поле для вывода результатов
results_text = scrolledtext.ScrolledText(root, width=70, height=20, wrap=tk.WORD)
results_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Информация о программе
info_label = tk.Label(root, text="Программа тестирования псевдослучайных последовательностей",
                      font=("Arial", 8), fg="gray")
info_label.pack(side=tk.BOTTOM, pady=5)

# Запуск главного цикла
root.mainloop()