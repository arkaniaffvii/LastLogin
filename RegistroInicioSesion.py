import win32evtlog
import tkinter as tk

LOG_NAME = "Security"
SERVER = "localhost"

def get_last_unlock():
    log = win32evtlog.OpenEventLog(SERVER, LOG_NAME)

    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

    found_latest = False

    while True:
        events = win32evtlog.ReadEventLog(log, flags, 0)
        if not events:
            break

        for event in events:
            event_id = event.EventID & 0xFFFF
            time = event.TimeGenerated.Format()

            if event_id == 4801:
                if not found_latest:
                    found_latest = True
                    continue

                return {
                    "method": "4801",
                    "time": time,
                    "user": event.StringInserts[1] if event.StringInserts else "Desconocido"
                }

    return None

def show_black_window(unlock):
    root = tk.Tk()
    root.iconbitmap(default="")
    root.resizable(False, False)
    root.title("Información de desbloqueo")
    root.configure(bg="black")
    root.attributes("-topmost",True)

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    win_w = int(screen_w*0.40)
    win_h = int(screen_h*0.25)

    x = (screen_w - win_w) // 2
    y = (screen_h - win_h) // 2

    root.geometry(f"{win_w}x{win_h}+{x}+{y}")

    if unlock:
        text=(
            "ÚLTIMO DESBLOQUEO ANTERIOR\n\n"
            f"Usuario: {unlock['user']}\n"
            f"Fecha  : {unlock['time']}"
        )
    else:
        text = "No se encontró un desbloqueo anterior \nPulsa ESC para cerrar"

    label = tk.Label(
        root,
        text=text,
        fg="white",
        bg="black",
        font=("Consolas",20),
        justify="center"
    )
    label.pack(expand=True)

    root.after(5000, root.destroy)
    root.mainloop()

if __name__ == "__main__":
    unlock = get_last_unlock()
    show_black_window(unlock)