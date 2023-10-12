import tkinter as tk
from tkinter import ttk
import time
from pso import PSO
from pso import animate_pso
from pso import f1
import ast
import numpy as np

cross_in_tray_string = "-0.0001 * (np.abs(np.sin(x) * np.sin(y) * np.exp(np.abs(100 - np.sqrt(x**2 + y**2) / np.pi))) + 1)**0.1"
cross_in_tray_range_nearby = "(-2, 2)"
cross_in_tray_range_distant = "(-10, 10)"

drop_wave_string = "-(1 + np.cos(12 * np.sqrt(x**2 + y**2))) / (0.5 * (x**2 + y**2) + 2)"
drop_wave_range_nearby = "(-1, 1)"
drop_wave_range_distant = "(-5, 5)"

holder_table_string = "-np.abs(np.sin(x) * np.cos(y) * np.exp(np.abs(1 - np.sqrt(x**2 + y**2) / np.pi)))"
holder_table_range = "(-10, 10)"

schaffer_n2_string = "0.5 + (np.sin(x**2 - y**2)**2 - 0.5) / (1 + 0.001 * (x**2 + y**2))**2"
schaffer_n2_range_nearby = "(-2, 2)"
schaffer_n2_range_distant = "(-50, 50)"

bukin_n6_string = "100 * np.sqrt(np.abs(y - 0.01 * x**2)) + 0.01 * np.abs(x + 10)"
bukin_n6_range = "(-15, 15)"

eggholder_string = "-(y + 47) * np.sin(np.sqrt(np.abs(x / 2 + (y + 47)))) - x * np.sin(np.sqrt(np.abs(x - (y + 47))))"
eggholder_range = "(-600, 600)"

levy_n13_string = "np.sin(3 * np.pi * x)**2 + (x - 1)**2 * (1 + np.sin(3 * np.pi * y)**2) + (y - 1)**2 * (1 + np.sin(2 * np.pi * y)**2)"
levy_n13_range = "(-10, 10)"

styblinski_tang_string = "(x**4 - 16 * x**2 + 5 * x) / 2 + (y**4 - 16 * y**2 + 5 * y) / 2"
styblinski_tang_range = "(-5, 5)"

predefined_function = "None"
predefined_range = "(-1000, 1000)"


def selectPredefinedFunction(event):
    global predefined_function
    global predefined_range
    selected_function = predefined_functions.get()

    if selected_function in list_of_predefined_functions and selected_function != "None":
        function_entry.config(state=tk.DISABLED)
        function_range_entry.config(state=tk.DISABLED)
    else:
        function_entry.config(state=tk.NORMAL)
        function_range_entry.config(state=tk.NORMAL)
        predefined_function = "None"
        predefined_range = "(-1000, 1000)"
        return

    if selected_function == "cross_in_tray_nearby":
        predefined_function = cross_in_tray_string
        predefined_range = cross_in_tray_range_nearby
    elif selected_function == "cross_in_tray_distant":
        predefined_function = cross_in_tray_string
        predefined_range = cross_in_tray_range_distant
    elif selected_function == "drop_wave_nearby":
        predefined_function = drop_wave_string
        predefined_range = drop_wave_range_nearby
    elif selected_function == "drop_wave_distant":
        predefined_function = drop_wave_string
        predefined_range = drop_wave_range_distant
    elif selected_function == "holder_table":
        predefined_function = holder_table_string
        predefined_range = holder_table_range
    elif selected_function == "schaffer_n2_nearby":
        predefined_function = schaffer_n2_string
        predefined_range = schaffer_n2_range_nearby
    elif selected_function == "schaffer_n2_distant":
        predefined_function = schaffer_n2_string
        predefined_range = schaffer_n2_range_distant
    elif selected_function == "bukin_n6":
        predefined_function = bukin_n6_string
        predefined_range = bukin_n6_range
    elif selected_function == "eggholder":
        predefined_function = eggholder_string
        predefined_range = eggholder_range
    elif selected_function == "levy_n13":
        predefined_function = levy_n13_string
        predefined_range = levy_n13_range
    elif selected_function == "styblinski_tang":
        predefined_function = styblinski_tang_string
        predefined_range = styblinski_tang_range

def stringToFunction(expression):
    try:
        func = lambda x, y: eval(expression)
        return func
    except Exception as e:
        print(f"Error: {e}")
        return None

def stringToTuple(input_string):
    try:
        result_tuple = ast.literal_eval(input_string)

        if isinstance(result_tuple, tuple):
            return result_tuple
        else:
            raise ValueError("The input is not a valid tuple representation.")
    except (ValueError, SyntaxError) as e:
        raise ValueError(f"Error: {e}")

def stringToFloat(input_string):
    try:
        result_float = float(input_string)
        return result_float
    except ValueError as e:
        raise ValueError(f"Error: {e}")

def stringToInt(input_string):
    try:
        result_int = int(input_string)
        return result_int
    except ValueError as e:
        raise ValueError(f"Error: {e}")

def run_algorithm():
    if predefined_function == "None":
        function_string = function_entry.get()
        function_range_string = function_range_entry.get()
    else:
        function_string = predefined_function
        function_range_string = predefined_range

    function = stringToFunction(function_string)

    function_range = stringToTuple(function_range_string)

    n_particles_string = n_particles_entry.get()
    n_particles = stringToInt(n_particles_string)

    n_iteractions_string = n_iteractions_entry.get()
    n_iteractions = stringToInt(n_iteractions_string)

    inertia_w_string = inertia_w_entry.get()
    inertia_w = stringToFloat(inertia_w_string)

    cognitive_w_string = cognitive_w_entry.get()
    cognitive_w = stringToFloat(cognitive_w_string)

    social_w_string = social_w_entry.get()
    social_w = stringToFloat(social_w_string)

    start_x_v_string = start_x_v_entry.get()
    start_x_v = stringToFloat(start_x_v_string)

    start_y_v_string = start_y_v_entry.get()
    start_y_v = stringToFloat(start_y_v_string)

    pso = PSO(function, function_range, n_particles, n_iteractions, inertia_w, cognitive_w, social_w, start_x_v, start_y_v)
    start_time = time.time()
    pso.run()
    end_time = time.time()

    global_best = pso.getGlobalBestX()
    global_best_string = f"x = {global_best[0]: .3f}, y = {global_best[1]: .3f}, f(x, y) = {pso.getFunction()(*global_best): .3f}"
    result_text.config(font="Helvetica 20 bold")
    result_text.delete(1, tk.END)
    result_text.insert(tk.END, global_best_string)

    elapsed_time = end_time - start_time
    time_string = f"t = {elapsed_time*1000: .3f}ms"
    time_text.config(font="Helvetica 20 bold")
    time_text.delete(1, tk.END)
    time_text.insert(tk.END, time_string)

    animate_pso(pso)

window = tk.Tk()
window.title("Find the minimum of a function with PSO")

window.geometry("1200x300")
window.resizable(True, False)

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=14)
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=1)
window.rowconfigure(3, weight=1)
window.rowconfigure(4, weight=1)
window.rowconfigure(5, weight=1)
window.rowconfigure(6, weight=1)
window.rowconfigure(7, weight=1)
window.rowconfigure(8, weight=1)
window.rowconfigure(9, weight=1)
window.rowconfigure(10, weight=1)
window.rowconfigure(11, weight=1)
window.rowconfigure(12, weight=4)

window.option_add("*Font", "Helvetica 16 bold")

predefined_functions_label = ttk.Label(window, text="Classical optimization functions:")
predefined_functions_label.grid(row=0, column=0, sticky="e")
list_of_predefined_functions = ["None", "cross_in_tray_nearby", "cross_in_tray_distant",  "drop_wave_nearby", "drop_wave_distant", "holder_table", "schaffer_n2_nearby", "schaffer_n2_distant", "bukin_n6", "eggholder", "levy_n13", "styblinski_tang"]
predefined_functions = ttk.Combobox(window, values=list_of_predefined_functions)
predefined_functions.set("None")
predefined_functions.grid(row=0, column=1, columnspan=2, sticky="ew")
predefined_functions.bind("<<ComboboxSelected>>", selectPredefinedFunction)

function_label = ttk.Label(window, text="Function:")
function_label.grid(row=1, column=0, sticky="e")
function_entry = ttk.Entry(window)
function_entry.grid(row=1, column=1, columnspan=2, sticky="ew")
default_function = "np.cos(np.sqrt(x**2 + y**2))*(x+y)"
function_entry.insert(0, default_function)

function_range_label = ttk.Label(window, text="Function Range:")
function_range_label.grid(row=2, column=0, sticky="e")
function_range_entry = ttk.Entry(window)
function_range_entry.grid(row=2, column=1, columnspan=2, sticky="ew")
function_range_entry.insert(0, "(-20, 20)")

n_particles_label = ttk.Label(window, text="N Particles:")
n_particles_label.grid(row=3, column=0, sticky="e")
n_particles_entry = ttk.Entry(window)
n_particles_entry.grid(row=3, column=1, columnspan=2, sticky="ew")
n_particles_entry.insert(0, "30")

n_iteractions_label = ttk.Label(window, text="N Iteractions:")
n_iteractions_label.grid(row=4, column=0, sticky="e")
n_iteractions_entry = ttk.Entry(window)
n_iteractions_entry.grid(row=4, column=1, columnspan=2, sticky="ew")
n_iteractions_entry.insert(0, "100")

inertia_w_label = ttk.Label(window, text="Inertia Weight:")
inertia_w_label.grid(row=5, column=0, sticky="e")
inertia_w_entry = ttk.Entry(window)
inertia_w_entry.grid(row=5, column=1, columnspan=2, sticky="ew")
inertia_w_entry.insert(0, "0.3") 

cognitive_w_label = ttk.Label(window, text="Cognitive Weight:")
cognitive_w_label.grid(row=6, column=0, sticky="e")
cognitive_w_entry = ttk.Entry(window)
cognitive_w_entry.grid(row=6, column=1, columnspan=2, sticky="ew")
cognitive_w_entry.insert(0, "0.9")

social_w_label = ttk.Label(window, text="Social Weight:")
social_w_label.grid(row=7, column=0, sticky="e")
social_w_entry = ttk.Entry(window)
social_w_entry.grid(row=7, column=1, columnspan=2, sticky="ew")
social_w_entry.insert(0, "0.9")

start_x_v_label = ttk.Label(window, text="Start X Velocity:")
start_x_v_label.grid(row=8, column=0, sticky="e")
start_x_v_entry = ttk.Entry(window)
start_x_v_entry.grid(row=8, column=1, columnspan=2, sticky="ew")
start_x_v_entry.insert(0, "0.5")

start_y_v_label = ttk.Label(window, text="Start Y Velocity:")
start_y_v_label.grid(row=9, column=0, sticky="e")
start_y_v_entry = ttk.Entry(window)
start_y_v_entry.grid(row=9, column=1, columnspan=2, sticky="ew")
start_y_v_entry.insert(0, "0.5")

result_label = ttk.Label(window, text="Minimum point found:", font='Helvetica 20 bold')
result_label.grid(row=10, column=0, sticky="e")
result_text = tk.Entry(window, state=tk.NORMAL, readonlybackground="lightgray")
result_text.grid(row=10, column=1, columnspan=3, sticky="ew")

time_label = ttk.Label(window, text="Time to execute:",font='Helvetica 20 bold')
time_label.grid(row=11, column=0, sticky="e")
time_text = tk.Entry(window, state=tk.NORMAL, readonlybackground="lightgray")
time_text.grid(row=11, column=1, columnspan=3, sticky="ew")

custom_style = ttk.Style()
custom_style.configure("Custom.TButton", background="green", font=("Helvetica", 18))

run_button = ttk.Button(window, text="Execute", command=run_algorithm, width=15, padding=10, style="Custom.TButton")
run_button.grid(row=12, column=1)

start_time = 0

window.mainloop()
