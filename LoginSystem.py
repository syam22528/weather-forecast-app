# Imports:
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from win32api import GetSystemMetrics
import smtplib
import PythonSQLConnection
import SendMail
import SearchResults
import UrlScrapper
import WeatherForecast
import Getlocation
import json
import time

# Lists & Variables:
login_entries = []
signup_entries = []
login_info = {}
comparitive_info = {}
signup_comp = {}
pass_check = {}
existing_usernames = []
existing_mails = []
default_location = Getlocation.get_location()
logged_in = False
guest = False
func_called = 2
screen_width = GetSystemMetrics(0)
screen_height = GetSystemMetrics(1)
no_place = None
list_box = None
extend_menu = None


# Classes:
class TopLevel:
    def __init__(self, title, geometry):
        self.title = title
        self.geometry = geometry

    def create_toplevel(self, master):
        global top_level
        top_level = tk.Toplevel(master)
        top_level.grab_set()
        top_level.title(self.title)
        top_level.geometry(self.geometry)
        top_level.resizable(False, False)


class AddButtons:
    def __init__(self, master, text, width=None, command=None, height=1, font=None):
        self.master = master
        self.text = text
        self.width = width
        self.height = height
        self.command = command
        self.font = font

    def create_buttons(self, rely=0.5, relx=0.5, image=None, bd=1):
        global button
        button = tk.Button(
            self.master,
            text=self.text,
            width=self.width,
            height=self.height,
            bg="#e3d6d6",
            command=self.command,
            font=self.font,
            image=image,
            bd=bd,
        )
        button.place(relx=relx, rely=rely, anchor=tk.CENTER)


class AddCanvas:
    def __init__(self, master, width=None, height=None):
        self.master = master
        self.width = width
        self.height = height

    def create_canvas(self, image=None, side=tk.LEFT):
        global canvas
        canvas = tk.Canvas(self.master, width=self.width, height=self.height)
        canvas.pack(expand=True, fill=tk.BOTH, side=side)
        if image is not None:
            canvas.create_image(screen_width / 2, screen_height / 2, image=image)


# Functions:
def quit(*window):
    for instance in window:
        instance.destroy()


def start_root_window(
    window_width=None, window_height=None, window_title="The Weather Forecast App"
):
    global root
    root = tk.Tk()
    root.title(window_title)
    root.attributes("-fullscreen", True)
    # if window_width is None and window_height is None:
    #     root.geometry('{}x{}'.format(screen_width, screen_height))
    # else:
    #     root.geometry('{}x{}'.format(window_width, window_height))
    # root.resizable(False, False)


def write_json(data, filename="loginData.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def save_file():
    global data
    with open("loginData.json") as json_file:
        data = json.load(json_file)
        data.append(login_info)
    write_json(data)


def login_clicked():
    global login_window
    login_window = TopLevel("Login", "400x175")
    login_window.create_toplevel(root)

    label_user = tk.Label(top_level, text="Username", font=("Calibre", "14"))
    label_user.place(relx=0.25, rely=0.25, anchor=tk.CENTER)

    label_pass = tk.Label(top_level, text="Password", font=("Calibre", "14"))
    label_pass.place(relx=0.25, rely=0.45, anchor=tk.CENTER)

    username_input = tk.Entry(top_level)
    username_input.place(relx=0.65, rely=0.25, anchor=tk.CENTER)

    password_input = tk.Entry(top_level, show="*")
    password_input.place(relx=0.65, rely=0.45, anchor=tk.CENTER)

    login_entries.clear()
    login_entries.append(username_input)
    login_entries.append(password_input)

    forgot_password = AddButtons(top_level, "Forgot password?", 12, forgot_passkey)
    forgot_password.create_buttons(0.7, 0.25)

    login_btn = AddButtons(top_level, "Login", 10, get_login_input)
    login_btn.create_buttons(0.7, 0.65)

    top_level.bind("<Return>", get_login_input)


def get_login_input(event=None):
    global comparitive_info
    username = login_entries[0].get()
    password = login_entries[1].get()
    comparitive_info.update(Username=username, Password=password)
    print(comparitive_info)
    login()


def login():
    global logged_in
    file_data = json.load(open("loginData.json", "r"))
    for user in file_data:
        real_username = user.get("Username")
        real_password = user.get("Password")
        comp_username = comparitive_info.get("Username")
        comp_username = comp_username.lower()
        comp_password = comparitive_info.get("Password")
        if real_username == comp_username and real_password == comp_password:
            logged_in = True
            completeLabel = tk.Label(
                top_level, text="You Have Successfully Been Logged In.", fg="green"
            )
            completeLabel.place(relx=0.5, rely=0.125, anchor=tk.CENTER)
            top_level.update_idletasks()
            time.sleep(1.5)
            quit(root)
        else:
            try:
                incorrect_label.destroy()
            except Exception:
                pass
            try:
                incorrect_label = tk.Label(
                    top_level, text="Incorrect Username Or Password.", fg="red"
                )
                incorrect_label.place(relx=0.5, rely=0.125, anchor=tk.CENTER)
            except tk.TclError:
                pass


def forgot_passkey():
    reset_window = tk.Toplevel(root)
    reset_window.grab_set()
    reset_window.title("Reset Password")
    reset_window.geometry("300x200")
    reset_window.resizable(False, False)


def signup():
    signup_window = TopLevel("Sign Up", "400x325")
    signup_window.create_toplevel(root)

    username_label = tk.Label(top_level, text="Username:", font=("Calibre", "12"))
    username_label.place(relx=0.163, rely=0.075, anchor=tk.CENTER)

    new_user_input = tk.Entry(top_level)
    new_user_input.place(relx=0.5, rely=0.155, anchor=tk.CENTER, width=350)

    email_label = tk.Label(top_level, text="Email:", font=("Calibre", "12"))
    email_label.place(relx=0.12, rely=0.23, anchor=tk.CENTER)

    new_email_input = tk.Entry(top_level)
    new_email_input.place(relx=0.5, rely=0.305, anchor=tk.CENTER, width=350)

    password_label = tk.Label(top_level, text="Password:", font=("Calibre", "12"))
    password_label.place(relx=0.155, rely=0.38, anchor=tk.CENTER)

    new_passkey_input = tk.Entry(top_level)
    new_passkey_input.place(relx=0.5, rely=0.455, anchor=tk.CENTER, width=350)

    retype_pass_label = tk.Label(
        top_level, text="Confirm Password:", font=("Calibre", "12")
    )
    retype_pass_label.place(relx=0.226, rely=0.53, anchor=tk.CENTER)

    retype_pass_input = tk.Entry(top_level)
    retype_pass_input.place(relx=0.5, rely=0.605, anchor=tk.CENTER, width=350)

    signup_entries.clear()
    signup_entries.append(new_user_input)
    signup_entries.append(new_email_input)
    signup_entries.append(new_passkey_input)
    signup_entries.append(retype_pass_input)

    signup_button = AddButtons(top_level, "Create an account", 20, get_signup_input)
    signup_button.create_buttons(0.8)

    top_level.bind("<Return>", get_signup_input)


def get_signup_input(event=None):
    global signup_comp
    username = signup_entries[0].get()
    mailid = signup_entries[1].get()
    check_pass = signup_entries[2].get()
    confirm_pass = signup_entries[3].get()
    signup_comp.update(Username=username, MailId=mailid)
    pass_check.update(Password=check_pass, ConfirmPassword=confirm_pass)
    print(signup_comp)
    print(pass_check)
    signup_clicked()


def signup_clicked():
    global no_mailid
    global bad_mailid
    global used_mailid
    global used_username
    global no_username
    global diff_passwords
    global verification_box
    global comp_username
    global comp_mailid
    global comp_pass
    existing_usernames.clear()
    login_data = json.load(open("loginData.json", "r"))
    for user in login_data:
        existing_username = user.get("Username")
        existing_usernames.append(existing_username)
        existing_mail = user.get("MailId")
        existing_mails.append(existing_mail)
    comp_username = signup_comp.get("Username")
    comp_username = comp_username.lower()
    comp_mailid = signup_comp.get("MailId")
    comp_mailid = comp_mailid.lower()
    comp_pass = pass_check.get("Password")
    comp_confirm_pass = pass_check.get("ConfirmPassword")
    if comp_mailid != existing_mail and comp_mailid != "":
        if comp_username not in existing_usernames and comp_username != "":
            if comp_pass == comp_confirm_pass and comp_pass != "":
                try:
                    SendMail.new_mail = comp_mailid
                    message = SendMail.mail_sent_message
                    SendMail.sendMail()

                    global verification_window
                    verification_window = tk.Toplevel(root)
                    verification_window.grab_set()
                    verification_window.title("Enter Verification Code")
                    verification_window.geometry("300x200")
                    verification_window.resizable(False, False)

                    mail_sent = tk.Label(
                        verification_window, text=message, font=("Calibre", "12")
                    )
                    mail_sent.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

                    verification_box = tk.Entry(
                        verification_window, font=("Calibre", "16")
                    )
                    verification_box.place(
                        relx=0.5, rely=0.7, anchor=tk.CENTER, width=150
                    )

                    verification_window.bind("<Return>", verify_code)

                except smtplib.SMTPRecipientsRefused:
                    error_exception()
                    bad_mailid = tk.Label(
                        top_level,
                        text="Invalid MailId!",
                        font=("Calibre", "10"),
                        fg="red",
                    )
                    bad_mailid.place(relx=0.78, rely=0.235, anchor=tk.CENTER)
                    # print('invalid MailId')

                except smtplib.socket.gaierror:
                    messagebox.showwarning(
                        title="Internet Connection Error",
                        message="Check You Internet Connection.",
                    )
                    # print('Check your internet connection.')
            elif comp_pass != comp_confirm_pass:
                error_exception()
                diff_passwords = tk.Label(
                    top_level,
                    text="Passwords Don't Match!",
                    font=("Calibre", "10"),
                    fg="red",
                )
                diff_passwords.place(relx=0.75, rely=0.535, anchor=tk.CENTER)
        elif comp_username in existing_usernames:
            error_exception()
            used_username = tk.Label(
                top_level, text="Username Is In Use!", font=("Calibre", "10"), fg="red"
            )
            used_username.place(relx=0.81, rely=0.08, anchor=tk.CENTER)
        elif comp_username == "":
            error_exception()
            no_username = tk.Label(
                top_level, text="Enter A Username!", font=("Calibre", "10"), fg="red"
            )
            no_username.place(relx=0.81, rely=0.08, anchor=tk.CENTER)
    elif comp_mailid == existing_mail:
        error_exception()
        used_mailid = tk.Label(
            top_level, text="Mail-Id In Use!", font=("Calibre", "10"), fg="red"
        )
        used_mailid.place(relx=0.81, rely=0.235, anchor=tk.CENTER)
    elif comp_mailid == "":
        error_exception()
        no_mailid = tk.Label(
            top_level, text="Enter Your Mail-Id!", font=("Calibre", "10"), fg="red"
        )
        no_mailid.place(relx=0.81, rely=0.235, anchor=tk.CENTER)


def verify_code(event=None):
    comp_code = int(verification_box.get())
    if comp_code == SendMail.verificationCode:
        quit(verification_window)
        acc_created = tk.Label(
            top_level,
            text="Your Account Has Been Created.",
            font=("Calibre", "12"),
            fg="green",
        )
        acc_created.place(relx=0.5, rely=0.92, anchor=tk.CENTER)
        login_info.update(
            [
                ("Username", comp_username),
                ("Password", comp_pass),
                ("MailId", comp_mailid),
            ]
        )
        save_file()
    else:
        wrong_code = tk.Label(
            verification_window,
            text="Check Your Code!",
            font=("Calibre", "13"),
            fg="red",
        )
        wrong_code.place(relx=0.5, rely=0.9, anchor=tk.CENTER)


def error_exception():
    try:
        diff_passwords.destroy()
    except Exception:
        pass
    try:
        no_username.destroy()
    except Exception:
        pass
    try:
        used_username.destroy()
    except Exception:
        pass
    try:
        bad_mailid.destroy()
    except Exception:
        pass
    try:
        used_mailid.destroy()
    except Exception:
        pass
    try:
        no_mailid.destroy()
    except Exception:
        pass


def guest_login():
    global guest
    time.sleep(0.25)
    quit(root)
    guest = True


def confirm_dialog(window):
    quit_dialog = TopLevel("Quit Confirmation", "300x90")
    quit_dialog.create_toplevel(window)

    def cancel_quit():
        quit(top_level)

    ask_label = tk.Label(top_level, text="Are you sure you want to exit?")
    ask_label.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
    no_btn = tk.Button(top_level, text="Cancel", width=7, command=cancel_quit)
    no_btn.place(relx=0.35, rely=0.65, anchor=tk.CENTER)
    yes_btn = tk.Button(top_level, text="Exit", width=7, command=lambda: quit(root))
    yes_btn.place(relx=0.65, rely=0.65, anchor=tk.CENTER)


def search_input(event=None):
    global list_box
    global no_place
    global location
    global new_canvas
    if search_bar.get() != "":
        try:
            quit(no_place)
        except Exception:
            pass
        # SearchResults.list_of_places.clear()
        try:
            quit(list_box)
        except Exception:
            pass
        try:
            if len(new_canvas.find_all()) > 20:
                new_canvas.delete("all")
                home()
        except Exception:
            pass
        SearchResults.place = search_bar.get()
        UrlScrapper.place = search_bar.get()
        SearchResults.get_url()
        list_box = tk.Listbox(
            root, width=80, height=20, bd=0, bg="#f7f7f7", selectbackground="#0080ff"
        )
        list_box.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        for item in SearchResults.list_of_places:
            list_box.insert(tk.END, item)
        # print(list_box.size())

        def get_location_input():
            global location
            location = list_box.get(tk.ACTIVE)
            index = SearchResults.list_of_places.index(location)
            UrlScrapper.index = index
            UrlScrapper.scrape_url()
            WeatherForecast.url_prefix = UrlScrapper.url_prefix
            WeatherForecast.weatherData()
            quit(list_box)
            quit(button)
            search_bar.delete(0, "end")
            display_data(PythonSQLConnection.fname)

        get_location = AddButtons(root, "OK", command=get_location_input)
        get_location.create_buttons(0.8, bd=0)
    else:
        try:
            quit(no_place)
        except Exception:
            pass
        no_place = tk.Label(
            title_bar,
            text="Please Enter A Valid Place!",
            fg="yellow",
            bg="#71879C",
            font=("Calibre", "16"),
        )
        no_place.pack(side=tk.RIGHT)


def extend_menubar():
    global func_called
    global extend_menu
    func_called += 1
    remainder = func_called % 2
    if remainder != 0:
        extend_menu = tk.Frame(bg="#71879C")
        canvas.create_window(
            38,
            40,
            anchor=tk.NW,
            window=extend_menu,
            width=menu_bar_width * 4,
            height=menu_bar_height,
        )
        home_label = tk.Label(
            extend_menu, text="Home", font=("Calibre", "20"), bg="#71879C"
        )
        home_label.pack(side=tk.TOP)

        favourites_label = tk.Label(
            extend_menu, text="Favourites", font=("Calibre", "20"), bg="#71879C"
        )
        favourites_label.pack(side=tk.TOP, pady=12)

        graphs_label = tk.Label(
            extend_menu, text="Graphs", font=("Calibre", "20"), bg="#71879C"
        )
        graphs_label.pack(side=tk.TOP)

        settings_label = tk.Label(
            extend_menu, text="Settings", font=("Calibre", "20"), bg="#71879C"
        )
        settings_label.pack(side=tk.BOTTOM)

        signout_label = tk.Label(
            extend_menu, text="Sign out", font=("Calibre", "20"), bg="#71879C"
        )
        signout_label.pack(side=tk.BOTTOM, pady=12)

    elif remainder == 0:
        quit(extend_menu)


def primary_window():
    bg_image = ImageTk.PhotoImage(Image.open("CloudsBg.gif"))
    bg = AddCanvas(root)
    bg.create_canvas(image=bg_image)
    canvas.create_text(
        screen_width / 2,
        screen_height / 4,
        anchor=tk.CENTER,
        font=("Calibre", "28"),
        text="Weather Forecast - Login",
    )

    btn1 = AddButtons(canvas, "Login", 20, command=login_clicked)
    btn2 = AddButtons(canvas, "Sign Up", 20, command=signup)
    btn3 = AddButtons(canvas, "Continue Without Sign-In", 20, command=guest_login)
    btn4 = AddButtons(canvas, "Quit", 10, lambda: confirm_dialog(root))
    btn1.create_buttons(0.45)
    btn2.create_buttons(0.5)
    btn3.create_buttons(0.55)
    btn4.create_buttons(0.977, 0.96)

    root.mainloop()


def sign_out():
    quit(root)
    start_root_window()
    primary_window()


def main_interface():
    global search_bar
    global menu_bar_width
    global menu_bar_height
    global title_bar_height
    global title_bar
    global bg_image

    bg_image = ImageTk.PhotoImage(
        Image.open(f"Background Pics/DarkStormy{screen_width}x{screen_height}.jpg")
    )
    arrow_image = ImageTk.PhotoImage(Image.open("Buttons/ArrowButton.png"))
    search_image = ImageTk.PhotoImage(Image.open("Buttons/SearchButton.png"))
    settings_image = ImageTk.PhotoImage(Image.open("Buttons/SettingsButton.png"))
    account_image = ImageTk.PhotoImage(Image.open("Buttons/AccountButton.png"))
    home_image = ImageTk.PhotoImage(Image.open("Buttons/HomeButton.png"))
    favorites_image = ImageTk.PhotoImage(Image.open("Buttons/FavoritesButton.png"))
    graphs_image = ImageTk.PhotoImage(Image.open("Buttons/GraphsButton.png"))

    bg = AddCanvas(root)
    bg.create_canvas()

    title_bar_height = 40
    menu_bar_height = screen_height - title_bar_height - 2
    menu_bar_width = 38

    title_bar = tk.Frame(bg="#71879C")
    canvas.create_window(
        0,
        0,
        anchor=tk.NW,
        window=title_bar,
        width=screen_width,
        height=title_bar_height,
    )

    arrow_button = tk.Button(
        title_bar, bd=0, bg="#71879C", image=arrow_image, command=extend_menubar
    )
    arrow_button.pack(side=tk.LEFT)

    search_bar = tk.Entry(title_bar, font=("Calibre", "22"), width=17)
    search_bar.pack(side=tk.RIGHT)
    search_bar.bind("<Return>", search_input)

    search_button = tk.Button(title_bar, bd=0, image=search_image, command=search_input)
    search_button.pack(side=tk.RIGHT, padx=2)

    menu_bar = tk.Frame(bg="#71879C")
    canvas.create_window(
        0,
        40,
        anchor=tk.NW,
        window=menu_bar,
        width=menu_bar_width,
        height=menu_bar_height,
    )

    home_button = tk.Button(menu_bar, bd=0, bg="#71879C", image=home_image)
    home_button.pack(side=tk.TOP, pady=4)

    bookmarks_button = tk.Button(menu_bar, bd=0, bg="#71879C", image=favorites_image)
    bookmarks_button.pack(side=tk.TOP, pady=4)

    graph_button = tk.Button(menu_bar, bd=0, bg="#71879C", image=graphs_image)
    graph_button.pack(side=tk.TOP, pady=4)

    settings_button = tk.Button(menu_bar, bd=0, bg="#71879C", image=settings_image)
    settings_button.pack(side=tk.BOTTOM, pady=4)

    signout_button = tk.Button(
        menu_bar,
        bd=0,
        text="signout",
        bg="#71879C",
        image=account_image,
        command=sign_out,
    )
    signout_button.pack(side=tk.BOTTOM, pady=4)

    home()

    root.mainloop()


def home():
    global new_canvas
    frame = tk.Frame()
    canvas.create_window(
        38,
        40,
        anchor=tk.NW,
        window=frame,
        width=screen_width - menu_bar_width,
        height=screen_height - title_bar_height,
    )

    new_canvas = tk.Canvas(
        frame,
        width=screen_width - menu_bar_width,
        height=screen_height - title_bar_height,
    )
    new_canvas.pack(anchor=tk.CENTER)
    new_canvas.create_image(screen_width / 2, screen_height / 2, image=bg_image)

    # new_canvas.create_oval(180, 200, 400, 420, fill="#2F507D", outline="#000000")


def display_data(info):
    global new_canvas
    pos_x = 290
    pos_y = 320
    x = 0
    new_canvas.create_text(
        941,
        100,
        width=300,
        text="14 Day Forecast Of {}".format(
            WeatherForecast.url_prefix.split("/")[-1].capitalize()
        ),
        fill="#1ed760",
        font=("Arial 28"),
        justify="center",
    )
    new_canvas.create_oval(180, 200, 400, 420, width=2)
    new_canvas.create_oval(440, 200, 660, 420, width=2)
    new_canvas.create_oval(700, 200, 920, 420, width=2)
    new_canvas.create_oval(960, 200, 1180, 420, width=2)
    new_canvas.create_oval(1220, 200, 1440, 420, width=2)
    new_canvas.create_oval(1480, 200, 1700, 420, width=2)
    new_canvas.create_oval(180, 460, 400, 680, width=2)
    new_canvas.create_oval(440, 460, 660, 680, width=2)
    new_canvas.create_oval(700, 460, 920, 680, width=2)
    new_canvas.create_oval(960, 460, 1180, 680, width=2)
    new_canvas.create_oval(1220, 460, 1440, 680, width=2)
    new_canvas.create_oval(1480, 460, 1700, 680, width=2)
    new_canvas.create_oval(700, 720, 920, 940, width=2)
    new_canvas.create_oval(960, 720, 1180, 940, width=2)
    for i in info[0:14]:
        string = "\U0001F4C5: {}\n\U00002B81: {}\n\U0001F327: {}\n\U0001F4A8: {}\n\U0001F4A6: {}\n".format(
            info[info.index(i)][0],
            info[info.index(i)][1].replace("°C", "") + " / " + info[0][2],
            info[info.index(i)][7],
            info[info.index(i)][3],
            info[info.index(i)][4],
        )
        if pos_x <= 1850 and pos_y == 320:
            new_canvas.create_text(
                pos_x,
                pos_y,
                width=150,
                text=string,
                fill="#00f0ff",
                font=("Helvetica 16"),
            )
            pos_x += 260
            if pos_x == 1850:
                pos_y = 580
        elif pos_y == 580:
            if pos_x == 1850:
                pos_x = 290
            new_canvas.create_text(
                pos_x,
                pos_y,
                width=150,
                text=string,
                fill="#00f0ff",
                font=("Helvetica 16"),
            )
            pos_x += 260
            if pos_x == 1850:
                pos_y = 840
        elif pos_y == 840:
            if x == 0:
                pos_x = 810
            new_canvas.create_text(
                pos_x,
                pos_y,
                width=150,
                text=string,
                fill="#00f0ff",
                font=("Helvetica 16"),
            )
            pos_x += 260
            x += 1


if __name__ == "__main__":
    # Initial Log-In Window:
    start_root_window()
    primary_window()

    # Main Interface:
    while True:
        if logged_in is True or guest is True:
            if guest is True:
                guest = False
            else:
                logged_in = False
            time.sleep(1)
            start_root_window()
            main_interface()
