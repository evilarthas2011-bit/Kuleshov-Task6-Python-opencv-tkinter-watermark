#TASK6
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import numpy as np

class VisionProcessor:
    def __init__(self):
        self._image = None          
        self.processed_image = None  

    def load_image(self, path):
        self._image = cv2.imread(path)
        return self._image is not None

    def get_center_coordinates(self):
        """Задача 2: Вычисление центра матрицы для позиционирования"""
        if self._image is None:
            return None
        h, w = self._image.shape[:2]
        center_x, center_y = w // 2, h // 2
        return center_x, center_y

    def apply_watermark_effect(self, text, blur_strength):
        """Задача 3: Конвейер OpenCV - размытие, маскирование центра и текст"""
        if self._image is None:
            return None

       
        result = cv2.blur(self._image, (blur_strength, blur_strength))
        
       
        h, w = self._image.shape[:2]
        cx, cy = self.get_center_coordinates()
        
        rw, rh = int(w * 0.35), int(h * 0.2)
        x1, y1 = cx - rw // 2, cy - rh // 2
        x2, y2 = cx + rw // 2, cy + rh // 2

      
        result[y1:y2, x1:x2] = self._image[y1:y2, x1:x2]

       
        font = cv2.FONT_HERSHEY_SIMPLEX
      
        font_scale = w / 1000.0 if w > 500 else 0.7
        thickness = max(1, int(font_scale * 2))
        
       
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x = cx - text_size[0] // 2
        text_y = cy + text_size[1] // 2

       
        cv2.putText(result, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
        
        self.processed_image = result
        return result

    def save_image(self, path):
        if self.processed_image is not None:
            return cv2.imwrite(path, self.processed_image)
        return False

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Вариант 12 — Водяной знак и Размытие")
        self.geometry("800x600")

        self.processor = VisionProcessor()
        self.file_path = None

    
        self.notebook = ttk.Notebook(self)
        self.tab_orig = ttk.Frame(self.notebook)
        self.tab_proc = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_orig, text="Оригинал")
        self.notebook.add(self.tab_proc, text="Обработка")
        self.notebook.pack(expand=True, fill="both", side=tk.TOP)

 
        self.control_panel = ttk.Frame(self)
        self.control_panel.pack(fill="x", padx=10, pady=10, side=tk.BOTTOM)

        # Кнопка загрузки
        self.btn_load = ttk.Button(self.control_panel, text="Загрузить картинку", command=self.open_file)
        self.btn_load.grid(row=0, column=0, padx=5)

  
        ttk.Label(self.control_panel, text="Текст знака:").grid(row=0, column=1, padx=5)
        self.entry_text = ttk.Entry(self.control_panel, width=15)
        self.entry_text.grid(row=0, column=2, padx=5)

       
        ttk.Label(self.control_panel, text="Размытие:").grid(row=0, column=3, padx=5)
        self.combo_blur = ttk.Combobox(self.control_panel, values=["15", "25", "45", "65"], width=5, state="readonly")
        self.combo_blur.current(1) # По умолчанию 25
        self.combo_blur.grid(row=0, column=4, padx=5)

        
        self.btn_process = ttk.Button(self.control_panel, text="Применить эффект", command=self.process_image)
        self.btn_process.grid(row=0, column=5, padx=5)

    
        self.btn_save = ttk.Button(self.control_panel, text="Сохранить результат", command=self.save_file)
        self.btn_save.grid(row=0, column=6, padx=5)

       
        self.lbl_img_orig = ttk.Label(self.tab_orig)
        self.lbl_img_orig.pack(expand=True)

        self.lbl_img_proc = ttk.Label(self.tab_proc)
        self.lbl_img_proc.pack(expand=True)

    def open_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Изображения", "*.jpg *.jpeg *.png *.bmp")])
        if self.file_path:
            if self.processor.load_image(self.file_path):
                self.display_image(self.processor._image, self.lbl_img_orig)
                messagebox.showinfo("Успех", "Изображение успешно загружено!")

    def process_image(self):
        """Задача 4: Комплексная связка виджетов и валидация"""
        if self.file_path is None:
            messagebox.showerror("Ошибка", "Сначала загрузите изображение!")
            return

        text = self.entry_text.get().strip()
        
        if not text:
            messagebox.showwarning("Предупреждение", "Поле ввода текста не должно быть пустым!")
            return

        blur_val = int(self.combo_blur.get())
        
      
        res_matrix = self.processor.apply_watermark_effect(text, blur_val)
        
        
        self.display_image(res_matrix, self.lbl_img_proc)
        self.notebook.select(self.tab_proc)

    def save_file(self):
        if self.processor.processed_image is None:
            messagebox.showerror("Ошибка", "Нет обработанного изображения для сохранения!")
            return
            
        save_path = filedialog.asksaveasfilename(defaultextension=".png", 
                                                 filetypes=[("PNG файл", "*.png"), ("JPEG файл", "*.jpg")])
        if save_path:
            if self.processor.save_image(save_path):
                messagebox.showinfo("Успех", f"Файл успешно сохранен:\n{save_path}")

    def display_image(self, cv_img, target_label):
        """Вспомогательный метод перевода матрицы BGR OpenCV в формат для Tkinter"""
     
        rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(rgb_img)
        
       
        img_pil.thumbnail((600, 450))
        
        img_tk = ImageTk.PhotoImage(image=img_pil)
        target_label.configure(image=img_tk)
        target_label.image = img_tk  

if __name__ == "__main__":
    app = App()
    app.mainloop()
