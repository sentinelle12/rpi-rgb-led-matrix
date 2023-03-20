


# ------------------------ OTHER APPROACH : UI SETUP -------------------

# class MainApplication(tk.Frame):
#     def __init__(self, parent, *args, **kwargs):
#         tk.Frame.__init__(self, parent, *args, **kwargs)
#         self.parent = parent
#
#         self.parent.title("NHL Game Display")
#         self.parent.config(padx=5, pady=5, bg='#000000')
#         self.parent.geometry('640x640')
#         self.canvas_width = 640
#         self.canvas_height = 640
#         self.canvas = tk.Canvas(parent, width=self.canvas_width, height=self.canvas_height, bg="#000000", highlightthickness=0)
#         self.canvas.pack()
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     MainApplication(root).pack(side="top", fill="both", expand=True)
#     root.mainloop()
