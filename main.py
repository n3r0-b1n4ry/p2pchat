import threading
import time

# import module GUI
from tkinter import *
from tkinter.font import *

# internal module
from p2pchat import *

__version__ = "0.1-beta"

def rgb2hex(r , g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

def window_create_connection(event = None):
    # some special function
    def submitConnection(event = None):
        client = addrclient_input_entry.get()
        addrclient_input_entry.unbind("<Return>")

        state.set("Connecting...")
        addrclient_input_state.update()
        if _send.create_connection(client) == True:
            addrclient_input_state.config(fg="Spring Green")
            state.set("Connect to {} successfully!".format(client))
        else:
            addrclient_input_state.config(fg="Red")
            state.set("Connect to {} failed!".format(client))
        addrclient_input_state.update()
        time.sleep(1)

        win_conn.destroy()
        win_conn.update()

    # config var
    w_win_conn = 270
    h_win_conn = 50
    # Create Window container
    win_conn = Toplevel()
    win_conn.title("Create connection")
    win_conn.config(bg=theme_color, width=w_win_conn, height=h_win_conn)
    win_conn.minsize(w_win_conn,h_win_conn)
    win_conn.resizable(False, False)
    # Create Connection input
    conn_frame = LabelFrame(win_conn, text = "Connection")
    conn_frame.config(bg=theme_color, fg=font_color, font=font, width=w_win_conn)
    conn_frame.pack(fill="both", expand=True)
    addrclient_input_label = Label(conn_frame, text = "Create Connections")
    addrclient_input_label.config(bg=theme_color, fg=font_color, font=font)
    addrclient_input_label.pack(side="left")
    addrclient_input_entry = Entry(conn_frame)
    addrclient_input_entry.config(bg=theme_color, fg=font_color, insertbackground=font_color, font=font, width=17)
    addrclient_input_entry.focus_set()
    addrclient_input_entry.bind("<Return>", submitConnection)
    addrclient_input_entry.pack(side="right", padx=5, pady=5)
    # Create State of connection
    state_frame = LabelFrame(win_conn, text = "Status")
    state_frame.config(bg=theme_color, fg=font_color, font=font, width=w_win_conn)
    state_frame.pack(fill="both", expand=True)
    state = StringVar()
    state.set("Insert IP Address")
    addrclient_input_state = Label(state_frame, textvariable=state)
    addrclient_input_state.config(bg=theme_color, fg=font_color, justify=CENTER, font=font)
    addrclient_input_state.pack()

    return

def printRecvMessage():
    _recv.listen()
    while True:
        # get message from receive stream
        _message = _recv.recv_msg()
        # print message to the content box
        if _message != None:
            mess_content_box.config(state=NORMAL)
            mess_content_box.insert(INSERT, _message + "\n")
            mess_content_box.config(state=DISABLED)
            mess_content_box.see(END)
        # check and connect to remote connection
        if _recv.client_addr != None and _send.client_addr == None:
            _send.create_connection(_recv.client_addr[0])

def printSendMessage(event = None):
    # some special function
    def formatString(msg):
        _msg = []
        wordlist = (' ', '\t')
        def toString(arr):
            str1 = ""
            return str1.join(arr)

        for i in range(1,len(msg)):
            if i == len(msg) - 1 and msg[i] in wordlist:
                break
            if msg[i] == msg[i-1] and msg[i] in wordlist:
                continue

            _msg.append(msg[i-1])

        msg = toString(_msg)
        wordlist = (' ', '\t','\n')
        for i in range(1,len(msg)):
            if msg[-i] in wordlist:
                continue
            else:
                if i == 1:
                    return msg
                msg = msg[0:-i]
                break
        return msg

    # get message from the input box
    _message = formatString(str(mess_input_box.get("1.0", END)))
    mess_input_box.delete("1.0", END)

    # print message to the content box
    if not _message == "":
        _send.send_msg(_message)

        mess_content_box.config(state=NORMAL)
        mess_content_box.insert(INSERT, "{}: {}".format(_send.host_user,_message + "\n"))
        mess_content_box.config(state=DISABLED)
        mess_content_box.see(END)

    return "break" # Prevent tkinter insert newline

def createShortcutKey():
    mainWindow.bind("<Control-n>", window_create_connection)
    mainWindow.bind("<Control-q>", lambda e:mainWindow.quit())

def createMenu():
    # some special function
    def show_About():
        w_win_about = 215
        h_win_about = 40
        win_about = Toplevel(mainWindow)
        win_about.title("About")
        win_about.config(bg=theme_color)
        win_about.minsize(w_win_about, h_win_about)
        win_about.resizable(False, False)

        author_frame = LabelFrame(win_about, text="Author")
        author_frame.config(bg=theme_color, fg=font_color, font=font, width=w_win_about)
        author_frame.pack(fill="both", expand=True)
        author = Label(author_frame, text="n3r0")
        author.config(bg=theme_color, fg=font_color, font=font)
        author.pack()
        ver_frame = LabelFrame(win_about, text="Version")
        ver_frame.config(bg=theme_color, fg=font_color, font=font, width=w_win_about)
        ver_frame.pack(fill="both", expand=True)
        ver = Label(ver_frame, text=__version__)
        ver.config(bg=theme_color, fg=font_color, font=font)
        ver.pack()

    # create the menu container
    menubar = Menu(mainWindow)

    # create Preference menu
    prefmenu = Menu(menubar, tearoff = 0)
    # add option to Preference menu
    prefmenu.add_command(label="New Connect  Ctrl+N", command=window_create_connection)
    prefmenu.add_separator()
    prefmenu.add_command(label="Quit                  Ctrl+Q", command=mainWindow.quit)

    # create Help menu
    helpmenu = Menu(menubar, tearoff = 0)
    # add option to Help menu
    helpmenu.add_command(label="About", command=show_About)

    # add child menus to menu bar
    menubar.add_cascade(label="Preference", menu = prefmenu)
    menubar.add_cascade(label="Help", menu = helpmenu)

    mainWindow.config(menu = menubar)


def createMainLayout():
    # some special function
    def insertNewline(event = None):
        return

    # create the container
    mainLayout = Frame(mainWindow)
    mainLayout.pack(fill="both", expand=True)

    # create content box 
    h_mess_content_box = 20 #lines not pixels
    global mess_content_box
    mess_content_box = Text(mainLayout, width=w_mainWindow, height=h_mess_content_box)
    # mess_content_box = Text(mainWindow, width=w_mainWindow, height=h_mess_content_box)
    mess_content_box.config(state=DISABLED, bg=theme_color, fg=font_color, font=font)
    mess_content_box.pack(side=TOP)

    # create input box
    h_mess_input_box = 2 #lines not pixels
    global mess_input_box
    mess_input_box = Text(mainLayout, width=w_mainWindow, height=h_mess_input_box)
    # mess_input_box = Text(mainWindow, width=w_mainWindow, height=h_mess_input_box)
    mess_input_box.config(bg=theme_color, fg=font_color, insertbackground=font_color, font=font)
    mess_input_box.focus_set()
    mess_input_box.bind("<Return>", printSendMessage)
    mess_input_box.bind("<Shift-Return>", insertNewline)
    mess_input_box.pack(side=BOTTOM)


try:
    _send = send_session()
    _recv = recv_session()

    mainWindow = Tk()
    # global var
    w_mainWindow = "660"
    h_mainWindow = "360"

    theme_color = "#0e1621"
    font_color = "white"
    font = Font(family="sans-serif", size=10)
    # Init for main window
    mainWindow.resizable(False, False)
    mainWindow.title("P2PChatBox")
    mainWindow.geometry("{}x{}".format(w_mainWindow,h_mainWindow))
    # Init function for render main Window
    createShortcutKey()
    createMenu()
    createMainLayout()

    # Special event
    th = threading.Thread(target=printRecvMessage, daemon=True)
    th.start()

    mainWindow.mainloop()
except Exception as e:
    print(e)