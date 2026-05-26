import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class SurgiCheckApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SurgiCheck - 手術器械AI自動盤點系統")
        self.geometry("1000x650")
        self.configure(bg="#F7FAFC")
        
        self.current_user = ""
        self.has_model = True  # 可切換 True/False 測試畫面

        self.create_nav_bar()
        
        self.container = tk.Frame(self, bg="#F7FAFC")
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, SelectPackPage, RecognitionPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def create_nav_bar(self):
        """建立頂部導覽列"""
        self.nav_frame = tk.Frame(self, bg="#1A202C", height=50)
        self.nav_frame.pack(fill="x", side="top")
        self.nav_frame.pack_propagate(False)
        
        self.user_info_label = tk.Label(
            self.nav_frame, text=" 👤 系統狀態：尚未登入", 
            bg="#1A202C", fg="#A0AEC0", font=("微軟正黑體", 11, "bold")
        )
        self.user_info_label.pack(side="left", padx=20)
        
        btn_style = {"bg": "#2D3748", "fg": "white", "font": ("微軟正黑體", 10, "bold"), "relief": "flat", "bd": 0, "cursor": "hand2"}
        
        btn_exit = tk.Button(self.nav_frame, text="離開系統", command=self.quit, **btn_style)
        btn_exit.pack(side="right", padx=(5, 20), pady=10, ipadx=15)
        self._set_hover(btn_exit, "#2D3748", "#E53E3E")
        
        btn_login = tk.Button(self.nav_frame, text="登入頁", command=lambda: self.show_frame("LoginPage"), **btn_style)
        btn_login.pack(side="right", padx=5, pady=10, ipadx=15)
        self._set_hover(btn_login, "#2D3748", "#4A5568")
        
        btn_home = tk.Button(self.nav_frame, text="回首頁", command=lambda: self.show_frame("LoginPage"), **btn_style)
        btn_home.pack(side="right", padx=5, pady=10, ipadx=15)
        self._set_hover(btn_home, "#2D3748", "#4A5568")

    def update_user_info(self):
        if self.current_user:
            self.user_info_label.config(text=f" 🟢 當前登入帳號：{self.current_user}", fg="#48BB78")
        else:
            self.user_info_label.config(text=" 👤 系統狀態：尚未登入", fg="#A0AEC0")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

    def _set_hover(self, widget, normal_bg, hover_bg):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg))
        widget.bind("<Leave>", lambda e: widget.config(bg=normal_bg))


class LoginPage(tk.Frame):
    """第一個畫面：登入頁面"""
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F7FAFC")
        self.controller = controller
        
        left_frame = tk.Frame(self, bg="#FFFFFF")
        left_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1)
        
        right_frame = tk.Frame(self, bg="#2B6CB0")
        right_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        # -- 左側元件 --
        login_container = tk.Frame(left_frame, bg="#FFFFFF")
        login_container.place(relx=0.5, rely=0.45, anchor="center")

        tk.Label(login_container, text="SurgiCheck", font=("Helvetica", 28, "bold"), fg="#2B6CB0", bg="#FFFFFF").pack(pady=5)
        tk.Label(login_container, text="手術器械AI自動盤點系統", font=("微軟正黑體", 14, "bold"), fg="#4A5568", bg="#FFFFFF").pack(pady=(0, 30))
        
        tk.Label(login_container, text="員工編號 (Root: SurgiCheck)", font=("微軟正黑體", 10, "bold"), fg="#718096", bg="#FFFFFF").pack(anchor="w", padx=5)
        self.entry_user = tk.Entry(login_container, font=("微軟正黑體", 12), bg="#EDF2F7", fg="#2D3748", relief="flat", justify="center", width=28)
        self.entry_user.pack(pady=(5, 15), ipady=8)

        tk.Label(login_container, text="安全密碼 (Root: aiot0721)", font=("微軟正黑體", 10, "bold"), fg="#718096", bg="#FFFFFF").pack(anchor="w", padx=5)
        self.entry_pwd = tk.Entry(login_container, font=("微軟正黑體", 12), bg="#EDF2F7", fg="#2D3748", relief="flat", show="*", justify="center", width=28)
        self.entry_pwd.pack(pady=(5, 25), ipady=8)

        self.btn_submit = tk.Button(
            login_container, text="驗證並登入系統", font=("微軟正黑體", 12, "bold"), 
            bg="#2B6CB0", fg="white", relief="flat", bd=0, cursor="hand2", width=26, command=self.login
        )
        self.btn_submit.pack(ipady=8)
        self.controller._set_hover(self.btn_submit, "#2B6CB0", "#2C5282")

        # -- 右側元件：Logo 圖片與說明文字 --
        logo_container = tk.Frame(right_frame, bg="#2B6CB0")
        logo_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # 嘗試載入實際的 Logo 圖片
        try:
            # 開啟圖片並縮放到適合大小 (例如 140x140 像素)
            img_open = Image.open("logo.png").resize((140, 140), Image.Resampling.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(img_open)
            
            self.logo_label = tk.Label(logo_container, image=self.logo_image, bg="#2B6CB0")
            # pady=(0, 40) 代表圖片上方不留空，下方留 40 像素的間距，成功將下方的字體往下移
            self.logo_label.pack(pady=(0, 40))
        except Exception:
            # 備用方案：若找不圖片檔案，則顯示原本的 Emoji 以免程式出錯
            self.logo_label = tk.Label(logo_container, text="🏥", font=("Segoe UI Emoji", 58), fg="#EBF8FF", bg="#2B6CB0")
            self.logo_label.pack(pady=(0, 40))
        
        tk.Label(logo_container, text="臺灣基督教門諾會醫療財團法人", font=("微軟正黑體", 15, "bold"), fg="#EBF8FF", bg="#2B6CB0").pack(pady=4)
        tk.Label(logo_container, text="門諾醫院 智慧醫療專案團隊", font=("微軟正黑體", 12), fg="#90CDF4", bg="#2B6CB0").pack(pady=4)

    def login(self):
        user = self.entry_user.get()
        pwd = self.entry_pwd.get()
        
        if user == "SurgiCheck" and pwd == "aiot0721":
            self.controller.current_user = user
            self.controller.update_user_info()
            messagebox.showinfo("安全認證成功", "歡迎進入門諾醫院智慧醫療工作台")
            self.controller.show_frame("SelectPackPage")
        else:
            messagebox.showerror("憑證錯誤", "無效的員工編號或密碼，請重試。")


class SelectPackPage(tk.Frame):
    """第二個畫面：手術包選擇頁面"""
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F7FAFC")
        self.controller = controller
        
        left_frame = tk.Frame(self, bg="#F7FAFC")
        left_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1)
        
        right_frame = tk.Frame(self, bg="#2B6CB0")
        right_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        # -- 左側：卡片選擇區 --
        tk.Label(left_frame, text="請選擇待盤點手術器械包", font=("微軟正黑體", 18, "bold"), fg="#2D3748", bg="#F7FAFC").pack(pady=(40, 20), anchor="w", padx=50)
        
        self.selected_pack = tk.StringVar(value="None")
        packs = [
            ("一般外科基礎包", "CSSD-GEN-01"),
            ("骨科基礎器械包", "CSSD-ORTH-02"),
            ("開腹手術器械包", "CSSD-LAP-05"),
            ("顯微手術器械包", "CSSD-MIC-09")
        ]
        
        for name, code in packs:
            card = tk.Frame(left_frame, bg="#FFFFFF", highlightbackground="#E2E8F0", highlightthickness=1, bd=0)
            card.pack(fill="x", padx=50, pady=6, ipady=8)
            
            rb = tk.Radiobutton(
                card, text=f" {name} ({code})", variable=self.selected_pack, value=name,
                font=("微軟正黑體", 11, "bold"), fg="#4A5568", bg="#FFFFFF", 
                activebackground="#FFFFFF", selectcolor="#2B6CB0", cursor="hand2"
            )
            rb.pack(side="left", padx=15)

        self.btn_next = tk.Button(
            left_frame, text="確認結構並開啟邊緣AI辨識", font=("微軟正黑體", 12, "bold"),
            bg="#319795", fg="white", relief="flat", bd=0, cursor="hand2", width=32, command=self.proceed
        )
        self.btn_next.pack(pady=30, ipady=10)
        self.controller._set_hover(self.btn_next, "#319795", "#285E61")

        # -- 右側元件：同樣載入 Logo 圖片並將字體下移 --
        logo_container = tk.Frame(right_frame, bg="#2B6CB0")
        logo_container.place(relx=0.5, rely=0.5, anchor="center")

        try:
            # 使用與登入頁相同的圖片物件（或重新讀取）
            img_open = Image.open("logo.png").resize((140, 140), Image.Resampling.LANCZOS)
            self.logo_image_page2 = ImageTk.PhotoImage(img_open)
            self.logo_label_page2 = tk.Label(logo_container, image=self.logo_image_page2, bg="#2B6CB0")
            self.logo_label_page2.pack(pady=(0, 40))
        except Exception:
            self.logo_label_page2 = tk.Label(logo_container, text="🏥", font=("Segoe UI Emoji", 58), fg="#EBF8FF", bg="#2B6CB0")
            self.logo_label_page2.pack(pady=(0, 40))

        tk.Label(logo_container, text="門諾醫院 | 智慧醫療自動化盤點", font=("微軟正黑體", 14, "bold"), fg="#EBF8FF", bg="#2B6CB0").pack()

    def proceed(self):
        if self.selected_pack.get() == "None":
            messagebox.showwarning("提示", "請先點選一個器械包以進行辨識。")
        else:
            self.controller.show_frame("RecognitionPage")


class RecognitionPage(tk.Frame):
    """第三個畫面：器械辨識主頁面"""
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F7FAFC")
        self.controller = controller
        self.dynamic_main_frame = None

    def on_show(self):
        if self.dynamic_main_frame:
            self.dynamic_main_frame.destroy()
            
        self.dynamic_main_frame = tk.Frame(self, bg="#F7FAFC")
        self.dynamic_main_frame.pack(fill="both", expand=True)

        if not self.controller.has_model:
            self._render_no_model_ui()
        else:
            self._render_active_recognition_ui()

    def _render_no_model_ui(self):
        error_card = tk.Frame(self.dynamic_main_frame, bg="#FFFFFF", highlightbackground="#FED7D7", highlightthickness=2, relief="flat")
        error_card.place(relx=0.5, rely=0.5, anchor="center", width=550, height=300)
        
        tk.Label(error_card, text="⚠️", font=("Segoe UI Emoji", 48), fg="#E53E3E", bg="#FFFFFF").pack(pady=(40, 10))
        tk.Label(error_card, text="核心邊緣運算提示", font=("微軟正黑體", 16, "bold"), fg="#2D3748", bg="#FFFFFF").pack()
        tk.Label(error_card, text="還未有模型建立\n\n請確認邊緣主機（Jetson Orin Nano）本機端是否已載入權重檔。", 
                 font=("微軟正黑體", 11), fg="#718096", bg="#FFFFFF", justify="center").pack(pady=15)

    def _render_active_recognition_ui(self):
        top_bar = tk.Frame(self.dynamic_main_frame, bg="#E2E8F0", height=40)
        top_bar.pack(fill="x", side="top")
        tk.Label(top_bar, text="🟢 邊緣運算串流正常 | 相機已就緒", 
                 font=("微軟正黑體", 10, "bold"), fg="#2B6CB0", bg="#E2E8F0").pack(side="left", padx=15, pady=10)

        body_frame = tk.Frame(self.dynamic_main_frame, bg="#F7FAFC")
        body_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        left_view = tk.Frame(body_frame, bg="#2D3748", highlightbackground="#CBD5E0", highlightthickness=1)
        left_view.place(relx=0, rely=0, relwidth=0.52, relheight=0.85)
        
        right_table_frame = tk.Frame(body_frame, bg="#FFFFFF", highlightbackground="#CBD5E0", highlightthickness=1)
        right_table_frame.place(relx=0.55, rely=0, relwidth=0.45, relheight=0.85)

        # -- 左側：影像串流 --
        tk.Label(left_view, text="【 影像辨識即時結果串流 】", font=("微軟正黑體", 12, "bold"), fg="#A0AEC0", bg="#2D3748").pack(pady=15)
        
        mock_canvas = tk.Canvas(left_view, bg="#1A202C", bd=0, highlightthickness=0)
        mock_canvas.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        mock_canvas.create_rectangle(40, 40, 200, 130, outline="#48BB78", width=2)
        mock_canvas.create_text(95, 55, text="Towel clamp: 96%", fill="#48BB78", font=("Helvetica", 9, "bold"))
        mock_canvas.create_rectangle(220, 80, 400, 220, outline="#48BB78", width=2)
        mock_canvas.create_text(270, 95, text="Mosquito: 94%", fill="#48BB78", font=("Helvetica", 9, "bold"))

        # -- 右側：數據表格 --
        tk.Label(right_table_frame, text="品項盤點對照清單", font=("微軟正黑體", 13, "bold"), fg="#2B6CB0", bg="#FFFFFF").pack(pady=10, anchor="w", padx=15)
        
        th_frame = tk.Frame(right_table_frame, bg="#EDF2F7")
        th_frame.pack(fill="x", padx=10)
        tk.Label(th_frame, text="器械品項 (Item Name)", font=("微軟正黑體", 10, "bold"), bg="#EDF2F7", fg="#4A5568", width=22, anchor="w").pack(side="left", padx=5, pady=5)
        tk.Label(th_frame, text="應有數量", font=("微軟正黑體", 10, "bold"), bg="#EDF2F7", fg="#4A5568", width=8).pack(side="left", pady=5)
        tk.Label(th_frame, text="AI 辨識數", font=("微軟正黑體", 10, "bold"), bg="#EDF2F7", fg="#4A5568", width=8).pack(side="left", pady=5)

        instrument_data = [
            ("Towel clamp", "7", "7"),
            ("Kocker", "2", "2"),
            ("Mosquito", "7", "7"),
            ("N.H (Needle Holder)", "5", "5"),
            ("Addson Teeth", "1", "1"),
            ("UV.K long Tooth", "1", "1"),
            ("Thread scissors", "1", "1")
        ]

        for idx, (name, target, detected) in enumerate(instrument_data):
            row_bg = "#FFFFFF" if idx % 2 == 0 else "#F7FAFC"
            row = tk.Frame(right_table_frame, bg=row_bg)
            row.pack(fill="x", padx=10)
            
            tk.Label(row, text=f" • {name}", font=("Helvetica", 10), bg=row_bg, fg="#2D3748", width=24, anchor="w").pack(side="left", padx=5, pady=4)
            tk.Label(row, text=target, font=("Helvetica", 10, "bold"), bg=row_bg, fg="#4A5568", width=8).pack(side="left", pady=4)
            tk.Label(row, text=detected, font=("Helvetica", 10, "bold"), bg=row_bg, fg="#3182CE", width=8).pack(side="left", pady=4)

        bottom_actions = tk.Frame(body_frame, bg="#F7FAFC")
        bottom_actions.place(relx=0, rely=0.88, relwidth=1, relheight=0.12)
        
        btn_re = tk.Button(bottom_actions, text="🔄 重新辨識", font=("微軟正黑體", 11, "bold"), bg="#E2E8F0", fg="#4A5568", relief="flat", bd=0, cursor="hand2")
        btn_re.pack(side="left", padx=10, ipadx=20, ipady=5)
        self.controller._set_hover(btn_re, "#E2E8F0", "#CBD5E0")
        
        btn_confirm = tk.Button(bottom_actions, text="✔ 盤點無誤，上傳大數據平台", font=("微軟正黑體", 11, "bold"), bg="#2B6CB0", fg="white", relief="flat", bd=0, cursor="hand2")
        btn_confirm.pack(side="right", padx=10, ipadx=20, ipady=5)
        self.controller._set_hover(btn_confirm, "#2B6CB0", "#2C5282")


if __name__ == "__main__":
    app = SurgiCheckApp()
    app.mainloop()
