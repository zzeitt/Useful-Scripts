import tkinter as tk
from PIL import Image, ImageTk


class ImageDisplayer:
    def __init__(self, s_winname='Image Displayer'):
        self._init_ui()
        self.load_image()
    
    def _init_ui(self):
        self._init_window()
        self._init_widgets()
        self._init_layout()
    
    def _init_window(self):
        self.win = tk.Tk()
        self.win.title('Image Displayer')
        self.win.geometry("720x900+1000+120")

    def _init_widgets(self):
        self.frm_all = tk.Frame(self.win, relief=tk.RAISED, borderwidth=1)
        
        self.frm_image = tk.Frame(self.frm_all, relief=tk.RAISED, borderwidth=1)
        self.lbl_image = tk.Label(self.frm_image, text='Image')
        
        self.frm_btns = tk.Frame(self.frm_all, relief=tk.RAISED, borderwidth=1)
        self.btn_prev = tk.Button(self.frm_btns, text='Previous', height=2)
        self.btn_next = tk.Button(self.frm_btns, text='Next', height=2)
        self.btn_quit = tk.Button(self.frm_btns, text='Quit', height=2, command=self.win.destroy)
        self.win.bind('q', lambda x: self.win.destroy())
        
    def _init_layout(self):
        self.frm_all.grid(row=1, column=1, sticky='news', padx=5, pady=5)
        self._stretch(self.frm_all, r=1, c=1)
        
        self.frm_image.grid(row=1, column=1, sticky='news', padx=5, pady=10)
        self._stretch(self.frm_image, r=1, c=1)
        self.lbl_image.grid(row=1, column=1, sticky='news')
        self._stretch(self.lbl_image, r=1, c=1)
        
        self.frm_btns.grid(row=2, column=1, sticky='news', padx=5, pady=10)
        self.btn_prev.grid(row=1, column=1, sticky='news')
        self._stretch(self.btn_prev, c=1)
        self.btn_next.grid(row=1, column=2, sticky='news')
        self._stretch(self.btn_next, c=2)
        self.btn_quit.grid(row=1, column=3, sticky='news')
        self._stretch(self.btn_quit, c=3)
        
    def _stretch(self, widget, r=None, c=None):
        if r:
            widget.master.rowconfigure(r, weight=1)
        if c:
            widget.master.columnconfigure(c, weight=1)
        
    def load_image(self):
        s_image = 'Assets/bash_boss_watching.png'
        pil_image = Image.open(s_image)
        self.tk_image = ImageTk.PhotoImage(pil_image)
        self.lbl_image.configure(image=self.tk_image)
        self._tk_image = self.tk_image
        
    def run(self):
        self.win.mainloop()
        
        
if __name__ == '__main__':
    ImageDisplayer().run()