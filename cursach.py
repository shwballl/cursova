import tkinter as tk
from tkinter import ttk, messagebox


def cross_product(x1, y1, x2, y2, x3, y3):
    return (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)


def on_segment(x1, y1, x2, y2, x3, y3):
    return (min(x1, x2) <= x3 <= max(x1, x2)) and (min(y1, y2) <= y3 <= max(y1, y2))


class SegmentIntersectionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Визначення кількості спільних точок відрізків")
        self.geometry("600x650")
        self.resizable(False, False)

        self._create_widgets()
        self._draw_grid()

    def _create_widgets(self):
        input_frame = ttk.LabelFrame(self, text="Вхідні дані (Координати точок)", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="Відрізок 1:").grid(row=0, column=0, sticky="w", pady=2)
        ttk.Label(input_frame, text="Ax:").grid(row=1, column=0)
        self.ax_entry = ttk.Entry(input_frame, width=6)
        self.ax_entry.insert(0, "50")
        self.ax_entry.grid(row=1, column=1)

        ttk.Label(input_frame, text="Ay:").grid(row=1, column=2)
        self.ay_entry = ttk.Entry(input_frame, width=6)
        self.ay_entry.insert(0, "50")
        self.ay_entry.grid(row=1, column=3)

        ttk.Label(input_frame, text="Bx:").grid(row=1, column=4)
        self.bx_entry = ttk.Entry(input_frame, width=6)
        self.bx_entry.insert(0, "350")
        self.bx_entry.grid(row=1, column=5)

        ttk.Label(input_frame, text="By:").grid(row=1, column=6)
        self.by_entry = ttk.Entry(input_frame, width=6)
        self.by_entry.insert(0, "350")
        self.by_entry.grid(row=1, column=7)

        ttk.Label(input_frame, text="Відрізок 2:").grid(row=2, column=0, sticky="w", pady=2)
        ttk.Label(input_frame, text="Cx:").grid(row=3, column=0)
        self.cx_entry = ttk.Entry(input_frame, width=6)
        self.cx_entry.insert(0, "50")
        self.cx_entry.grid(row=3, column=1)

        ttk.Label(input_frame, text="Cy:").grid(row=3, column=2)
        self.cy_entry = ttk.Entry(input_frame, width=6)
        self.cy_entry.insert(0, "350")
        self.cy_entry.grid(row=3, column=3)

        ttk.Label(input_frame, text="Dx:").grid(row=3, column=4)
        self.dx_entry = ttk.Entry(input_frame, width=6)
        self.dx_entry.insert(0, "350")
        self.dx_entry.grid(row=3, column=5)

        ttk.Label(input_frame, text="Dy:").grid(row=3, column=6)
        self.dy_entry = ttk.Entry(input_frame, width=6)
        self.dy_entry.insert(0, "50")
        self.dy_entry.grid(row=3, column=7)

        calc_button = ttk.Button(self, text="Розрахувати та побудувати", command=self.process_and_draw)
        calc_button.pack(pady=5)

        self.result_label = ttk.Label(
            self, text="Результат: Введіть координати та натисніть кнопку", font=("Helvetica", 10, "bold")
        )
        self.result_label.pack(pady=5)

        self.canvas = tk.Canvas(self, width=550, height=400, bg="#f0f0f0")
        self.canvas.pack(padx=10, pady=5)

    def _draw_grid(self):
        self.canvas.delete("all")
        width = 550
        height = 400

        for x in range(0, width, 50):
            self.canvas.create_line(x, 0, x, height, fill="#e0e0e0")
        for y in range(0, height, 50):
            self.canvas.create_line(0, y, width, y, fill="#e0e0e0")

    def process_and_draw(self):
        try:
            ax = float(self.ax_entry.get())
            ay = float(self.ay_entry.get())
            bx = float(self.bx_entry.get())
            by = float(self.by_entry.get())

            cx = float(self.cx_entry.get())
            cy = float(self.cy_entry.get())
            dx = float(self.dx_entry.get())
            dy = float(self.dy_entry.get())
        except ValueError:
            messagebox.showerror("Помилка введення", "Будь ласка, введіть числові значення для координат!")
            return

        d1 = cross_product(cx, cy, dx, dy, ax, ay)
        d2 = cross_product(cx, cy, dx, dy, bx, by)
        d3 = cross_product(ax, ay, bx, by, cx, cy)
        d4 = cross_product(ax, ay, bx, by, dx, dy)

        result_text = ""

        if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
           ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
            result_text = "Результат: 1 спільна точка (строгий перетин)."

        elif d1 == 0 and d2 == 0 and d3 == 0 and d4 == 0:
            if on_segment(ax, ay, bx, by, cx, cy) or on_segment(ax, ay, bx, by, dx, dy) or \
               on_segment(cx, cy, dx, dy, ax, ay) or on_segment(cx, cy, dx, dy, bx, by):

                if (ax == cx and ay == cy and not on_segment(ax, ay, bx, by, dx, dy)) or \
                   (ax == dx and ay == dy and not on_segment(ax, ay, bx, by, cx, cy)) or \
                   (bx == cx and by == cy and not on_segment(ax, ay, bx, by, dx, dy)) or \
                   (bx == dx and by == dy and not on_segment(ax, ay, bx, by, cx, cy)):
                    result_text = "Результат: 1 спільна точка (дотик кінцями на одній прямій)."
                else:
                    result_text = "Результат: Нескінченна кількість спільних точок (перекриття)."
            else:
                result_text = "Результат: 0 спільних точок (на одній прямій, без перекриття)."

        elif (d1 == 0 and on_segment(cx, cy, dx, dy, ax, ay)) or \
             (d2 == 0 and on_segment(cx, cy, dx, dy, bx, by)) or \
             (d3 == 0 and on_segment(ax, ay, bx, by, cx, cy)) or \
             (d4 == 0 and on_segment(ax, ay, bx, by, dx, dy)):
            result_text = "Результат: 1 спільна точка (дотик вершиною до відрізка)."

        else:
            result_text = "Результат: 0 спільних точок (паралельні або не перетинаються)."

        self.result_label.config(text=result_text)

        self._draw_grid()

        self.canvas.create_line(ax, ay, bx, by, fill="blue", width=3)
        self.canvas.create_text(ax + 8, ay - 8, text="A", fill="blue", font=("Helvetica", 10, "bold"))
        self.canvas.create_text(bx + 8, by - 8, text="B", fill="blue", font=("Helvetica", 10, "bold"))

        self.canvas.create_line(cx, cy, dx, dy, fill="red", width=3)
        self.canvas.create_text(cx + 8, cy - 8, text="C", fill="red", font=("Helvetica", 10, "bold"))
        self.canvas.create_text(dx + 8, dy - 8, text="D", fill="red", font=("Helvetica", 10, "bold"))


if __name__ == "__main__":
    app = SegmentIntersectionApp()
    app.mainloop()