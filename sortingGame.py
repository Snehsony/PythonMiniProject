import tkinter as tk
from tkinter import ttk
import random


class SortingGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Sneh Sony")

        # Set the window to full screen
        self.master.attributes('-fullscreen', True)
        self.master.bind("<Escape>", self.exit_fullscreen)  # Bind Escape key to exit full screen

        # Create a canvas
        self.canvas = tk.Canvas(self.master)
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Fill the entire window

        # Title
        self.title_label = tk.Label(self.master, text="Sneh Sony", bg='#f0f0f0',
                                    font=("Roboto", 32, "bold"))
        self.title_label.pack(pady=(30, 10))  # Increased padding for better positioning

        self.algorithm_label = tk.Label(self.master, text="", bg='#f0f0f0', font=("Arial", 24))
        self.algorithm_label.pack(pady=(10, 20))  # Add space above the algorithm label

        self.numbers = []
        self.sorted_bars = []  # To keep track of sorted bars
        self.is_stopped = False  # Variable to control the stop function
        self.is_paused = False  # Variable to control the resume function
        self.current_algorithm = None  # Variable to keep track of the current sorting algorithm
        self.current_index = None  # Index to resume from
        self.generate_numbers()

        # Create a gradient background
        self.draw_gradient_background('#58126a', '#f6b2e1')  # Gradient colors

        # Buttons
        self.button_frame = tk.Frame(self.master, bg='#f0f0f0')  # Frame for buttons with a different shade
        self.button_frame.pack(pady=20)

        # Style for circular buttons
        self.style = ttk.Style()
        self.style.configure('Circular.TButton', borderwidth=0, relief="flat", padding=10)
        self.style.map('Circular.TButton', background=[('active', '#4CAF50')],
                       foreground=[('active', 'Blue')])  # Change on hover

        # Creating buttons with rounded appearance
        self.bubble_sort_button = ttk.Button(self.button_frame, text="Bubble Sort", command=self.bubble_sort,
                                             style='Circular.TButton')
        self.bubble_sort_button.pack(side=tk.LEFT, padx=10)

        self.selection_sort_button = ttk.Button(self.button_frame, text="Selection Sort", command=self.selection_sort,
                                                style='Circular.TButton')
        self.selection_sort_button.pack(side=tk.LEFT, padx=10)

        self.insertion_sort_button = ttk.Button(self.button_frame, text="Insertion Sort", command=self.insertion_sort,
                                                style='Circular.TButton')
        self.insertion_sort_button.pack(side=tk.LEFT, padx=10)

        self.quick_sort_button = ttk.Button(self.button_frame, text="Quick Sort", command=self.quick_sort,
                                            style='Circular.TButton')
        self.quick_sort_button.pack(side=tk.LEFT, padx=10)

        self.merge_sort_button = ttk.Button(self.button_frame, text="Merge Sort", command=self.merge_sort,
                                            style='Circular.TButton')
        self.merge_sort_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = ttk.Button(self.button_frame, text="Stop", command=self.stop_sorting,
                                      style='Circular.TButton')
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.resume_button = ttk.Button(self.button_frame, text="Resume", command=self.resume_sorting,
                                        style='Circular.TButton')
        self.resume_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = ttk.Button(self.button_frame, text="Reset", command=self.generate_numbers,
                                       style='Circular.TButton')
        self.reset_button.pack(side=tk.LEFT, padx=10)

        # Speed control slider
        self.speed_label = tk.Label(self.master, text="Speed Control (milliseconds)", bg='#f0f0f0', font=("Arial", 12))
        self.speed_label.pack(pady=10)
        self.speed_slider = tk.Scale(self.master, from_=100, to=1000, orient=tk.HORIZONTAL, bg='#f0f0f0')
        self.speed_slider.set(500)  # Default speed
        self.speed_slider.pack(pady=10)

    def exit_fullscreen(self, event=None):
        self.master.attributes('-fullscreen', False)  # Exit full screen
        self.master.geometry('600x400')  # Set a default size for the window

    def draw_gradient_background(self, color1, color2):
        """ Create a gradient background on the canvas. """
        self.canvas.delete("all")  # Clear the canvas
        height = self.canvas.winfo_height()
        width = self.canvas.winfo_width()

        # Create gradient
        for i in range(height):
            r = int((i / height) * (int(color2[1:3], 16) - int(color1[1:3], 16)) + int(color1[1:3], 16))
            g = int((i / height) * (int(color2[3:5], 16) - int(color1[3:5], 16)) + int(color1[3:5], 16))
            b = int((i / height) * (int(color2[5:7], 16) - int(color1[5:7], 16)) + int(color1[5:7], 16))
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, width, i, fill=color)

    def generate_numbers(self):
        self.numbers = random.sample(range(10, 101), 60)  # Generate 60 random numbers between 10 and 100
        self.sorted_bars = []  # Reset sorted bars
        self.is_stopped = False  # Reset stop variable
        self.is_paused = False  # Reset paused variable
        self.current_algorithm = None  # Reset current algorithm
        self.current_index = None  # Reset index
        self.algorithm_label.config(text="")  # Clear the algorithm label
        self.draw_bars()

    def draw_bars(self):
        self.canvas.delete("all")  # Clear the canvas
        self.draw_gradient_background('#9a52c7', '#e5aac3')  # Redraw gradient background

        canvas_height = self.canvas.winfo_height()
        canvas_width = self.canvas.winfo_width()

        if canvas_height == 0 or canvas_width == 0:
            print("Canvas height or width is zero.")
            return  # If the canvas dimensions are not set yet, exit the function

        bar_width = canvas_width // len(self.numbers)  # Calculate bar width based on canvas width
        corner_radius = 25  # Radius for rounded corners

        for i, number in enumerate(self.numbers):
            x0 = i * bar_width  # Position each bar
            y0 = canvas_height - number * 4  # Scale down for better visibility
            x1 = x0 + bar_width - 1  # Slight adjustment for the width
            y1 = canvas_height  # Fixed bottom position of bars

            # Set the color for the bar
            if i in self.sorted_bars:  # Check if the bar is sorted
                color = '#800080'  # Purple for sorted bars
            else:
                color = f'#{random.randint(0, 0xFFFFFF):06x}'  # Random color for unsorted bars

            # Draw a rounded rectangle with black border
            self.draw_rounded_rectangle(x0, y0, x1, y1, corner_radius, color, outline='#000000', width=1)

            # Add text above the bars
            self.canvas.create_text(x0 + bar_width / 2, y1 + 10, text=str(number), font=("Arial", 10))

        print("Bars drawn:", self.numbers)  # Debug statement to confirm bars are drawn

    def draw_rounded_rectangle(self, x0, y0, x1, y1, radius, color, outline, width):
        """ Draw a rounded rectangle with the given parameters. """
        self.canvas.create_polygon(
            x0 + radius, y0,  # Top left
            x1 - radius, y0,  # Top right
            x1, y0 + radius,  # Right top corner
            x1, y1 - radius,  # Right bottom corner
            x1 - radius, y1,  # Bottom right
            x0 + radius, y1,  # Bottom left
            x0, y1 - radius,  # Left bottom corner
            x0, y0 + radius,  # Left top corner
            fill=color, outline=outline, width=width
        )

    def stop_sorting(self):
        """ Function to stop the sorting process. """
        self.is_stopped = True  # Set the stop variable to True
        self.is_paused = False  # Ensure it is not paused

    def resume_sorting(self):
        """ Function to resume the sorting process. """
        self.is_stopped = False  # Reset the stop variable
        self.is_paused = False  # Reset the paused variable
        if self.current_algorithm:
            # Continue from the last stopped position
            if self.current_algorithm == "bubble":
                self.bubble_sort()
            elif self.current_algorithm == "selection":
                self.selection_sort()
            elif self.current_algorithm == "insertion":
                self.insertion_sort()
            elif self.current_algorithm == "quick":
                self.quick_sort()
            elif self.current_algorithm == "merge":
                self.merge_sort()

    def bubble_sort(self):
        self.current_algorithm = "bubble"
        n = len(self.numbers)
        self.algorithm_label.config(text="Bubble Sort in progress...")
        for i in range(n):
            for j in range(0, n - i - 1):
                if self.numbers[j] > self.numbers[j + 1]:
                    self.numbers[j], self.numbers[j + 1] = self.numbers[j + 1], self.numbers[j]
                    self.draw_bars()  # Update bars after swap
                    self.master.update()  # Update the window
                    self.master.after(self.speed_slider.get())  # Delay based on slider value
                if self.is_stopped:
                    return
            self.sorted_bars.append(n - i - 1)  # Track sorted bars
            self.draw_bars()  # Redraw bars after sorting
        self.algorithm_label.config(text="Sorting Complete!")

    def selection_sort(self):
        self.current_algorithm = "selection"
        n = len(self.numbers)
        self.algorithm_label.config(text="Selection Sort in progress...")
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if self.numbers[j] < self.numbers[min_idx]:
                    min_idx = j
                if self.is_stopped:
                    return
            self.numbers[i], self.numbers[min_idx] = self.numbers[min_idx], self.numbers[i]
            self.sorted_bars.append(i)  # Track sorted bars
            self.draw_bars()  # Update bars after swap
            self.master.update()  # Update the window
            self.master.after(self.speed_slider.get())  # Delay based on slider value
        self.algorithm_label.config(text="Sorting Complete!")

    def insertion_sort(self):
        self.current_algorithm = "insertion"
        n = len(self.numbers)
        self.algorithm_label.config(text="Insertion Sort in progress...")
        for i in range(1, n):
            key = self.numbers[i]
            j = i - 1
            while j >= 0 and key < self.numbers[j]:
                self.numbers[j + 1] = self.numbers[j]
                j -= 1
                if self.is_stopped:
                    return
            self.numbers[j + 1] = key
            self.sorted_bars.append(i)  # Track sorted bars
            self.draw_bars()  # Update bars after swap
            self.master.update()  # Update the window
            self.master.after(self.speed_slider.get())  # Delay based on slider value
        self.algorithm_label.config(text="Sorting Complete!")

    def partition(self, low, high):
        pivot = self.numbers[high]
        i = low - 1
        for j in range(low, high):
            if self.numbers[j] < pivot:
                i += 1
                self.numbers[i], self.numbers[j] = self.numbers[j], self.numbers[i]
                self.draw_bars()  # Update bars after swap
                self.master.update()  # Update the window
                self.master.after(self.speed_slider.get())  # Delay based on slider value
            if self.is_stopped:
                return
        self.numbers[i + 1], self.numbers[high] = self.numbers[high], self.numbers[i + 1]
        self.draw_bars()  # Update bars after swap
        self.master.update()  # Update the window
        self.master.after(self.speed_slider.get())  # Delay based on slider value
        return i + 1

    def quick_sort(self, low=0, high=None):
        if high is None:
            high = len(self.numbers) - 1
        self.current_algorithm = "quick"
        self.algorithm_label.config(text="Quick Sort in progress...")
        if low < high:
            pi = self.partition(low, high)
            self.quick_sort(low, pi - 1)
            self.quick_sort(pi + 1, high)
        else:
            self.sorted_bars.append(low)  # Track sorted bars
            self.draw_bars()  # Update bars after sorting
            self.master.update()  # Update the window
            self.master.after(self.speed_slider.get())  # Delay based on slider value
        if not self.is_stopped:
            self.algorithm_label.config(text="Sorting Complete!")

    def merge(self, left, mid, right):
        n1 = mid - left + 1
        n2 = right - mid
        L = self.numbers[left:mid + 1]
        R = self.numbers[mid + 1:right + 1]

        i = 0  # Initial index of first sub-array
        j = 0  # Initial index of second sub-array
        k = left  # Initial index of merged sub-array

        while i < n1 and j < n2:
            if L[i] <= R[j]:
                self.numbers[k] = L[i]
                i += 1
            else:
                self.numbers[k] = R[j]
                j += 1
            k += 1
            self.draw_bars()  # Update bars after merge
            self.master.update()  # Update the window
            self.master.after(self.speed_slider.get())  # Delay based on slider value
            if self.is_stopped:
                return

        while i < n1:
            self.numbers[k] = L[i]
            i += 1
            k += 1
            self.draw_bars()  # Update bars after merge
            self.master.update()  # Update the window
            self.master.after(self.speed_slider.get())  # Delay based on slider value
            if self.is_stopped:
                return

        while j < n2:
            self.numbers[k] = R[j]
            j += 1
            k += 1
            self.draw_bars()  # Update bars after merge
            self.master.update()  # Update the window
            self.master.after(self.speed_slider.get())  # Delay based on slider value
            if self.is_stopped:
                return

    def merge_sort(self, left=0, right=None):
        if right is None:
            right = len(self.numbers) - 1
        self.current_algorithm = "merge"
        self.algorithm_label.config(text="Merge Sort in progress...")
        if left < right:
            mid = (left + right) // 2
            self.merge_sort(left, mid)
            self.merge_sort(mid + 1, right)
            self.merge(left, mid, right)
        else:
            self.sorted_bars.append(left)  # Track sorted bars
            self.draw_bars()  # Update bars after sorting
            self.master.update()  # Update the window
            self.master.after(self.speed_slider.get())  # Delay based on slider value
        if not self.is_stopped:
            self.algorithm_label.config(text="Sorting Complete!")


if __name__ == "__main__":
    root = tk.Tk()
    app = SortingGame(root)
    root.mainloop()
