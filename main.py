from gui import *


def main() -> None:
    """
    Creates Tkinter window and creates GUI to start GUI process
    :return: None
    """
    window = Tk()
    window.geometry('1150x600')
    window.resizable(False, False)

    GUI(window)
    window.mainloop()




if __name__ == '__main__':
    main()

