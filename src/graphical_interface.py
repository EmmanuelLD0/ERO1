from drone_flight.flight_creator import *
from tools.display import display, graph_images, update_image
from demo import demo

"""
! this file will handle the user interface for our demo
"""

import tkinter as tk
from customtkinter import *
import sys
import threading

class RediectStdout:
    """
    This class will redirect the stdout to the terminal
    """

    def __init__(self, terminal):
        self.terminal = terminal

    def write(self, message):
        self.terminal.insert(tk.END, message)
        # self.terminal.update_idletasks();

    def flush(self):
        pass


current_index = 0
fixed_cost = 100
cost_km = 0.01
speed = 4


def save_settings(pop_up: tk.Toplevel, _fixed_cost: str, _cost_km: str, _speed: str):
    """
    ! This function will save the settings of the drones
    @param pop_up: tk.Toplevel: the popup window
    @param fixed_cost: str: the fixed cost of the drones
    @param cost_km: str: the cost per km of the drones
    @param speed: str: the speed of the drones
    """
    global fixed_cost, cost_km, speed
    fixed_cost = float(_fixed_cost)
    cost_km = float(_cost_km)
    speed = float(_speed)
    print("Settings saved")
    print("----------------")
    print(f"Fixed cost: {fixed_cost}")
    print(f"Cost per km: {cost_km}")
    print(f"Speed: {speed}")
    print("----------------")
    pop_up.destroy()


def open_popup(root: tk.Tk):
    popup = tk.Toplevel(root)
    popup.title("Settings")

    # Labels
    tk.Label(popup, text="Fixed Cost:").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(popup, text="Cost per km:").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(popup, text="Speed:").grid(row=2, column=0, padx=5, pady=5)

    # Entry widgets
    fixed_cost_entry = tk.Entry(popup)
    fixed_cost_entry.grid(row=0, column=1, padx=5, pady=5)
    cost_per_km_entry = tk.Entry(popup)
    cost_per_km_entry.grid(row=1, column=1, padx=5, pady=5)
    speed_entry = tk.Entry(popup)
    speed_entry.grid(row=2, column=1, padx=5, pady=5)

    # Button to submit values
    submit_btn = tk.Button(
        popup,
        text="Submit",
        command=lambda: save_settings(
            popup, fixed_cost_entry.get(), cost_per_km_entry.get(), speed_entry.get()
        ),
    )
    submit_btn.grid(row=3, column=0, columnspan=2, padx=5, pady=5)


def show_graph(screen: tk.Label, title_label: tk.Label, direction: int):
    """
    ! This function will show the next or previous graph images
    @param screen: tk.Label: the screen
    @param title_label: tk.Label: the title label
    @param direction: int: the direction of the graph images
    """
    global current_index
    current_index += direction
    current_index = max(0, min(current_index, len(graph_images) - 1))
    img, title = graph_images[current_index]
    update_image(img, screen)
    title_label.config(text=title)

def main():
    """
    This function will create the main window for the user interface
    """
    # screen setup
    root = CTk()
    root.title("ERO")
    set_appearance_mode('dark')
    root.geometry("800x600")

    # title
    title = CTkLabel(root, text="ERO1 PING 39", font=("Helvetica", 24))
    title.pack()

    # Graph title
    graph_title = CTkLabel(root, text="")
    graph_title.pack()

    # settings button
    settings_button = CTkButton(master=root, text="Customize Parameters", font=('Arial', 15),
                                command=lambda: open_popup(root))
    # settings_button.pack(padx=10, pady=10)
    settings_button.pack()

    #dw about this it's too fool it
    image_label = tk.Label(root)

    #create the thread for launching the demo
    thread = threading.Thread(target=demo, args=(image_label, graph_title, fixed_cost, cost_km, speed, graph_images))

    # navigation buttons
    prev_button = CTkButton(
        master=root, text="Previous", font=("Arial", 15),
        fg_color="grey",
        command=lambda: show_graph(image_label, image_label, -1)
    )
    prev_button.pack(side=tk.LEFT, padx=10)

    next_button = CTkButton(
        root, text="Next", font=("Arial", 15),
        fg_color="grey",
        command=lambda: show_graph(image_label, image_label, 1)
    )
    next_button.pack(side=tk.RIGHT, padx=10)

    # image label
    image_label.pack()

    # debug interface
    # debug_terminal = tk.Text(root, font=('Arial', 12), width=80, height=15)
    debug_terminal = CTkTextbox(master=root, bg_color="black", fg_color="white", text_color="black")
    # debug_terminal.pack()
    debug_terminal.pack(fill=BOTH, expand=True, padx=10, pady=10)

    # demo button
    demo_button = CTkButton(
        master=root, text="RUN PROGRAM", font=('Helvetica', 18),
        fg_color="green",
        command=lambda: thread.start() 
    )
    demo_button.pack()

    # catching all stdout and stderr
    OriginalStdout = sys.stdout
    sys.stdout = RediectStdout(debug_terminal)

    root.mainloop()

    # reset stdout
    sys.stdout = OriginalStdout


if __name__ == "__main__":
    main()
