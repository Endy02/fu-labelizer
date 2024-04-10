import glob
import json
import os
from tkinter.messagebox import *
from tkinter import filedialog

import customtkinter
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #############################################
        #       APP CONFIGURATION
        #############################################
        #getting screen width and height of display
        width= self.winfo_screenwidth()
        height= self.winfo_screenheight()
        #setting tkinter window size
        self.geometry("%dx%d" % (width, height))
        self.title("Fu-Labelizer")

        # configure grid layout (0x3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)

        #############################################
        #       FRAME DECLARATION
        #############################################
        # create sidebar
        self.sidebar_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        self.sidebar_frame.grid_rowconfigure(10, weight=1)

        # create right sidebar frame
        self.right_sidebar_frame = customtkinter.CTkFrame(self, corner_radius=0, width=400)
        self.right_sidebar_frame.grid(row=0, column=2, rowspan=4, sticky="nsew")
        self.right_sidebar_frame.grid_columnconfigure(0, weight=1)
        self.right_sidebar_frame.grid_rowconfigure(10, weight=1)

        # create Image Canvas frame
        self.outer_frame = customtkinter.CTkCanvas(self)
        self.outer_frame.grid(row=0, column=1,padx=(30, 30), pady=(30, 30), rowspan=1, sticky="nsew")
        self.outer_frame.grid_columnconfigure(0, weight=1)
        self.outer_frame.grid_rowconfigure(0, weight=1)

        # create Info frame
        self.info_frame = customtkinter.CTkFrame(self, corner_radius=20)
        self.info_frame.grid(row=1, column=1,padx=(30, 30), pady=(30, 30), rowspan=1, sticky="nsew")
        self.info_frame.grid_columnconfigure(3, weight=1)
        self.info_frame.grid_rowconfigure(0, weight=1)

        #############################################
        #       LEFT SIDEBAR
        #############################################
        logo = os.path.dirname(os.path.abspath('assets'))+ "/assets/images/logo_v2.png"
        self.logo_image = customtkinter.CTkImage(Image.open(logo), size=(110, 110))
        self.real_logo_label = customtkinter.CTkLabel(self.sidebar_frame, image=self.logo_image, text="")
        self.real_logo_label.grid(row=0, column=0, pady=(20, 20), padx=(20, 20))
        
        # Appearence selectbox
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Theme :", anchor="w")
        self.appearance_mode_label.grid(row=17, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=18, column=0, padx=20, pady=(10, 20))

        # create scrollable frame
        self.sidebar_scrollable_frame = customtkinter.CTkScrollableFrame(self.sidebar_frame, label_text="Images", corner_radius=20, width=250, height=500)
        self.sidebar_scrollable_frame.grid(row=5, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.sidebar_scrollable_frame.grid_columnconfigure(0, weight=1)
        self.sidebar_selected_var = customtkinter.StringVar()

        #############################################
        #       RIGHT SIDEBAR
        #############################################
        self.main_button_1 = customtkinter.CTkButton(master=self.right_sidebar_frame, text='Open folder', fg_color="transparent", command=self.open_folder_event, border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=0, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

         # create tabview
        self.tabview = customtkinter.CTkTabview(self.right_sidebar_frame, corner_radius=20, width=300,  height=300)
        self.tabview.grid(row=2, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        # ----------- Folder Tab -----------
        
        self.tabview.add("Folder")
        self.tabview.tab("Folder").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Folder").grid_rowconfigure(3, weight=1)  # configure grid of individual tabs

        # ----------- Information Tab -----------
        self.tabview.add("Informations")
        self.tabview.tab("Informations").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Informations").grid_rowconfigure(4, weight=1)  # configure grid of individual tabs

        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.right_sidebar_frame, label_text="Categories", corner_radius=20, width=250, height=400)
        self.scrollable_frame.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.selected_var = customtkinter.StringVar()
        
        if os.path.exists(os.path.dirname(os.path.abspath("data")) + "/data/labelizer_data.json") and os.path.exists(os.path.dirname(os.path.abspath("data")) + "/data/dataset_infos.json"):
            self.__update_elements()
        # # create radiobutton frame
        # self.radiobutton_frame = customtkinter.CTkFrame(self.right_sidebar_frame)
        # self.radiobutton_frame.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        # self.radio_var = tkinter.IntVar(value=0)
        # self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Categories :")
        # self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        # self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=0)
        # self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        # self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=1)
        # self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        # self.radio_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=2)
        # self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        #############################################
        #       IMAGE FRAME
        #############################################
        self.x = self.y = 0
        self.rect = None
        self.rect_data = []
        self.start_x = None
        self.start_y = None
        self.outer_frame.bind('<Configure>', self.resize_image)
        # self.outer_frame.bind('<ButtonPress-1>', self.on_button_press)
        # self.outer_frame.bind('<B1-Motion>', self.on_move_press)
        # self.outer_frame.bind('<ButtonRelease-1>', self.on_button_release)
        #############################################
        #       INFO FRAME
        #############################################
        # self.tabview = customtkinter.CTkTabview(self, width=300)
        # self.tabview.grid(row=0, column=2, padx=(30, 30), pady=(30, 30), sticky="nsew")
        # self.tabview.add("CTkTabview")
        # self.tabview.add("Tab 2")
        # self.tabview.add("Tab 3")
        # self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        # self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

        # self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
        #                                                 values=["Value 1", "Value 2", "Value Long Long Long"])
        # self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        # self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"),
        #                                             values=["Value 1", "Value 2", "Value Long....."])
        # self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        # self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",
        #                                                    command=self.open_input_dialog_event)
        # self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        # self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
        # self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

    #     # create slider and progressbar frame
    #     # self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
    #     # self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
    #     # self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
    #     # self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
    #     # self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
    #     # self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
    #     # self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
    #     # self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
    #     # self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
    #     # self.progressbar_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
    #     # self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=4)
    #     # self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
    #     # self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
    #     # self.slider_2.grid(row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")
    #     # self.progressbar_3 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
    #     # self.progressbar_3.grid(row=0, column=2, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns")

        # # create scrollable frame
        # self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="CTkScrollableFrame")
        # self.scrollable_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        # self.scrollable_frame.grid_columnconfigure(0, weight=1)
        # self.scrollable_frame_switches = []
        # for i in range(10):
        #     switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"CTkSwitch {i}")
        #     switch.grid(row=i, column=0, padx=10, pady=(0, 20))
        #     self.scrollable_frame_switches.append(switch)

    #     # create checkbox and switch frame
    #     self.checkbox_slider_frame = customtkinter.CTkFrame(self)
    #     self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
    #     self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
    #     self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
    #     self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
    #     self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
    #     self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
    #     self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")

    #     # set default values
    #     self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
    #     self.checkbox_3.configure(state="disabled")
    #     self.checkbox_1.select()
    #     self.scrollable_frame_switches[0].select()
    #     self.scrollable_frame_switches[4].select()
    #     self.radio_button_3.configure(state="disabled")
    #     self.appearance_mode_optionemenu.set("Dark")
    #     self.scaling_optionemenu.set("100%")
    #     self.optionmenu_1.set("CTkOptionmenu")
    #     self.combobox_1.set("CTkComboBox")
    #     # self.slider_1.configure(command=self.progressbar_2.set)
    #     # self.slider_2.configure(command=self.progressbar_3.set)
    #     # self.progressbar_1.configure(mode="indeterminnate")
    #     # self.progressbar_1.start()
    #     self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)
    #     # self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
    #     # self.seg_button_1.set("Value 2")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def open_folder_event(self):
        folder = filedialog.askdirectory()
        if len(folder) > 0:
            scan = glob.glob(folder+"/*")
            data = {}
            cat_count = 0
            image_count = 0
            labels_count = 0
            for item in scan:
                category = item.split('/')[-1] # Get category name
                cat_count += 1
                if os.path.isdir(item):
                    sub_items = glob.glob(item+"/*") # get category image
                    images = []
                    for sub_item in sub_items:
                        image_count += 1
                        labels_count += 1 if os.path.exists(item + "/labels/" +sub_item.split('.')[0] + ".json") else 0
                        # Build Image data
                        images.append({
                            'image' : sub_item,
                            'name': sub_item.split('/')[-1],
                            'done' : True if os.path.exists(item + "/labels/" +sub_item.split('.')[0] + ".json") else False,
                            'label': json.dumps(open(item + "/labels/" +sub_item.split('.')[0] + ".json")) if os.path.exists(item + "/labels/" +sub_item.split('.')[0] + ".json") else None
                        })
                    # Build Categories data
                    data[category] = {
                        "category": category.lower(),
                        "link": item,
                        "done": False,
                        "image_number": len([image['done'] for image in images if image['done'] == False]),
                        "labels": len([image['done'] for image in images if image['done'] == True]),
                        "images" : images
                        }
            data_info = {
                "folder" : folder,
                "categories": cat_count,
                "images": image_count,
                "labels": labels_count
            }
            # Get the data folder link to register the new json file
            data_link = self.__check_data_folder()
            
            # Save dataset informations
            with open(data_link + '/dataset_infos.json', 'w') as outdatafile:
                json.dump(data_info, outdatafile, indent=4)
                outdatafile.close()

            # Save folder scan into json file
            with open(data_link + '/labelizer_data.json', 'w') as outfile:
                json.dump(data, outfile, indent=4)
                outfile.close()

            self.__update_elements() # Update Frames
    
    def __update_elements(self):
        data_link = self.__check_data_folder()
        file = open(data_link + '/labelizer_data.json')
        info_file = open(data_link + '/dataset_infos.json')
        data = json.load(file)
        infos = json.load(info_file)

        self.folder_tab_entry=customtkinter.CTkEntry(self.tabview.tab("Folder"), width= 250, font=('Helvetica', 16), textvariable=customtkinter.StringVar(self, infos['folder']))
        self.folder_tab_entry.grid(row=0, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.folder_tab_entry.configure(state= "disabled")

        self.folder_tab_button = customtkinter.CTkButton(self.tabview.tab("Folder"), text="Resize dataset", width=250, corner_radius=20)
        self.folder_tab_button.grid(row=1, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.folder_tab_label=customtkinter.CTkLabel(self.tabview.tab("Folder"), width= 250, font=('Helvetica', 16), textvariable=customtkinter.StringVar(self, f"Missing Labels : {str(infos['images'] - infos['labels'])}"))
        self.folder_tab_label.grid(row=4, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.folder_tab_cat=customtkinter.CTkLabel(self.tabview.tab("Informations"), width= 250, font=('Helvetica', 16), textvariable=customtkinter.StringVar(self, f"Categories : {str(infos['categories'])}"))
        self.folder_tab_cat.grid(row=1, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.folder_tab_image=customtkinter.CTkLabel(self.tabview.tab("Informations"), width= 250, font=('Helvetica', 16), textvariable=customtkinter.StringVar(self, f"Images : {str(infos['images'])}"))
        self.folder_tab_image.grid(row=2, column=3, padx=(15, 15), pady=(20, 20), sticky="nsew")

        self.folder_tab_label=customtkinter.CTkLabel(self.tabview.tab("Informations"), width= 250, font=('Helvetica', 16), textvariable=customtkinter.StringVar(self, f"Labels : {str(infos['labels'])}"))
        self.folder_tab_label.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        real_data = {}
        for item, value in data.items():
            if value['done'] == False:
                real_data[item] = value
            
        # Fill the categories option menu
        for i, cat in enumerate(real_data.keys()):
            self.radio_button_1 = customtkinter.CTkRadioButton(master=self.scrollable_frame, text=f"{cat} ({str(real_data[cat]['image_number'])})", command=self.radio_button_event, variable=self.selected_var, value=i, width=200)
            self.radio_button_1.grid(row=i, column=0, pady=10, padx=20, sticky="n")

    def radio_button_event(self):
        data_link = self.__check_data_folder()
        data = json.load(open(data_link + '/labelizer_data.json'))
        index = int(self.selected_var.get())
        keys = list(data.keys())

        category = data[keys[index]]

        # Fill the categories option menu
        for i, cat in enumerate(category['images']):
            self.radio_button_1 = customtkinter.CTkRadioButton(master=self.sidebar_scrollable_frame, text=cat["name"], command=self.sidebar_radio_button_event, variable=self.sidebar_selected_var, value=i, width=200)
            self.radio_button_1.grid(row=i, column=0, pady=10, padx=20, sticky="n")

    def draw_rectangle(self, event):
        x, y = event.x, event.y
        self.inner_frame.create_rectangle(x, y, x+10, y+10, fill='blue')

    def on_button_press(self, event):
        self.start_x = self.inner_frame.canvasx(event.x)
        self.start_y = self.inner_frame.canvasx(event.y)

        if not self.rect:
            self.rect = self.inner_frame.create_rectangle(self.x, self.y, 1, 1, width=3, outline='blue')

    def on_move_press(self, event):
        self.curX = self.inner_frame.canvasx(event.x)
        self.curY = self.inner_frame.canvasx(event.y)

        # w, h = self.outer_frame.winfo_width(), self.outer_frame.winfo_height()
        # if event.x > 0.9*w:
        #     self.outer_frame.xview_scroll(1, 'units')
        # elif event.x < 0.1*w:
        #     self.outer_frame.xview_scroll(-1, 'units')
        # if event.y > 0.9*w:
        #     self.outer_frame.yview_scroll(1, 'units')
        # elif event.y < 0.1*w:
        #     self.outer_frame.yview_scroll(-1, 'units')
        
        self.inner_frame.coords(self.rect, self.start_x, self.start_y, self.curX, self.curY)

    def on_button_release(self, event):
        res = askokcancel("Label saving","Save the rectangle ?")
        if res:
            data_link = self.__check_data_folder()
            data = json.load(open(data_link + '/labelizer_data.json'))
            index = int(self.selected_var.get())
            image_index = int(self.sidebar_selected_var.get())
            keys = list(data.keys())

            category = data[keys[index]]

            image = category['images'][image_index]
            
            obj_list = []
            final_link = None

            if image['label'] is not None:
                final_link = image['label']
                with open(image['label']) as f:
                    obj_list = json.load(f)
                obj_list.append({
                    'order': len(image['label']) + 1,
                    'start': {
                        'x': self.start_x,
                        'y': self.start_y
                    },
                    'end': {
                        'x': self.curX,
                        'y': self.curY
                    }
                })
            else:
                label_link = image['image'].split('/')[-1]
                label_name = label_link.split('.')[0]+".json"
                final_link = '/'.join(image['image'].split('/')[:-1])+ f"/labels/{label_name}"
                obj_list.append({
                    'order': len(image['label']) + 1 if image['label'] else 1,
                    'start': {
                        'x': self.start_x,
                        'y': self.start_y
                    },
                    'end': {
                        'x': self.curX,
                        'y': self.curY
                    }
                })
            
            with open(final_link, 'w+') as outdatafile:
                json.dump(obj_list, outdatafile, indent=4)
                outdatafile.close()

            self.__update_elements() # Update Frames

            print(final_link)
            print(json.dumps(obj_list, indent=4))

            print(" -------- Inner Canvas size (self.canvas_image_tk)")
            print(f"Width : {self.inner_frame.winfo_width()} | Height : {self.inner_frame.winfo_height()}")
            print(" -------- Image Real size (self.canvas_image_tk)")
            print(f"Width : {self.canvas_image.width} | Height : {self.canvas_image.height}")
            print(" -------- Image Resized size (self.canvas_image_tk)")
            print(f"Width : {self.canvas_image_tk.width()} | Height : {self.canvas_image_tk.height()}")
            print(" -------- Rectangle coords")
            print(f"first point : {self.start_x} | second : {self.start_y} | third : {self.curX} | Fourth : {self.curY}")

        else:
            self.inner_frame.delete(self.rect)
            self.x = self.y = 0
            self.rect = None
            self.start_x = None
            self.start_y = None
            self.inner_frame.bind('<ButtonPress-1>', self.on_button_press)
            self.inner_frame.bind('<B1-Motion>', self.on_move_press)
            self.inner_frame.bind('<ButtonRelease-1>', self.on_button_release)

    def sidebar_radio_button_event(self):
        data_link = self.__check_data_folder()
        data = json.load(open(data_link + '/labelizer_data.json'))
        index = int(self.selected_var.get())
        image_index = int(self.sidebar_selected_var.get())
        keys = list(data.keys())

        category = data[keys[index]]

        image = category['images'][image_index]

        self.canvas_image = Image.open(image['image'])
        self.wazil, self.lard = self.canvas_image.size
        self.outer_frame.configure(scrollregion=(0,0, self.wazil, self.lard))
        self.canvas_image_ratio = self.canvas_image.size[0] / self.canvas_image.size[1]
        self.canvas_image_tk = ImageTk.PhotoImage(self.canvas_image)

        self.canvas_ratio = self.image_width / self.image_height

        if self.canvas_ratio > self.canvas_image_ratio:
            real_image_height = int(self.image_height) 
            real_image_width = int(self.image_height * self.canvas_image_ratio)
        else:
            real_image_height = int(self.image_width / self.canvas_image_ratio)
            real_image_width = int(self.image_width)
        
        
        if self.rect is not None:
            self.inner_frame.delete("all")
        self.x = self.y = 0
        self.rect = None
        self.start_x = None
        self.start_y = None

        self.inner_frame = customtkinter.CTkCanvas(self.outer_frame, width=real_image_width, height=real_image_height)
        self.inner_frame.grid(row=0, column=0,padx=(0, 0), pady=(0, 0))
        self.inner_frame.grid_columnconfigure(0, weight=2)
        self.inner_frame.grid_rowconfigure(0, weight=2)
        self.inner_frame.bind('<ButtonPress-1>', self.on_button_press)
        self.inner_frame.bind('<B1-Motion>', self.on_move_press)
        self.inner_frame.bind('<ButtonRelease-1>', self.on_button_release)

        self.resized_image = self.canvas_image.resize((real_image_width, real_image_height))
        self.canvas_image_tk = ImageTk.PhotoImage(self.resized_image)
        self.inner_frame.create_image(real_image_width/2, real_image_height/2, image=self.canvas_image_tk)

    def resize_image(self, event):
        self.image_width = event.width
        self.image_height = event.height

    def __check_data_folder(self):
        root = os.path.dirname(os.path.abspath('assets'))
        if not os.path.exists(root + "/data"):
            os.makedirs(root + "/data")
        return root + "/data"

if __name__ == "__main__":
    app = App()
    app.mainloop()
