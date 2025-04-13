import tkinter as tk
from tkinter import filedialog, messagebox


class Notatnik:
    '''Klasa odpowiadajaca za wswietlanie i dzialanie samego programu'''
    def __init__(self, root):
        '''Wykorzystwane do stworzenia calej strukuty notatika'''
        self.root = root
        self.root.title("Mini Notatnik")
        self.root.geometry("600x400")

        self.tekst = tk.Text(root, wrap="word")
        self.tekst.pack(fill="both", expand=True)

        self.menu = tk.Menu(root)
        root.config(menu=self.menu)

        self.plik_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Plik", menu=self.plik_menu)
        self.plik_menu.add_command(label="Nowy", command=self.nowy_plik)
        self.plik_menu.add_command(label="Otwórz...", command=self.otworz_plik)
        self.plik_menu.add_command(label="Zapisz", command=self.zapisz_plik)
        self.plik_menu.add_separator()
        self.plik_menu.add_command(label="Wyjście", command=self.zamknij)

        self.edytuj_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Edycja", menu=self.edytuj_menu)
        self.edytuj_menu.add_command(label="Cofnij", command=self.tekst.edit_undo)
        self.edytuj_menu.add_command(label="Ponów", command=self.tekst.edit_redo)
        self.edytuj_menu.add_separator()
        self.edytuj_menu.add_command(
            label="Wytnij",
            command=lambda: self.root.focus_get().event_generate("<<Cut>>"),
        )
        self.edytuj_menu.add_command(
            label="Kopiuj",
            command=lambda: self.root.focus_get().event_generate("<<Copy>>"),
        )
        self.edytuj_menu.add_command(
            label="Wklej",
            command=lambda: self.root.focus_get().event_generate("<<Paste>>"),
        )

    def nowy_plik(self):
        '''Wykorzystywana do tworzenia nowego pliku'''
        if self.czy_zapisac():
            self.tekst.delete(1.0, tk.END)

    def otworz_plik(self):
        ''' Wykorzystywana do otwierania pliku'''
        if not self.czy_zapisac():
            return
        sciezka = filedialog.askopenfilename(
            filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")]
        )
        if sciezka:
            with open(sciezka, "r", encoding="utf-8") as plik:
                self.tekst.delete(1.0, tk.END)
                self.tekst.insert(tk.END, plik.read())

    def zapisz_plik(self):
        ''' Wykorzysytwana do zapisu '''
        sciezka = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Pliki tekstowe", "*.txt")]
        )
        if sciezka:
            with open(sciezka, "w", encoding="utf-8") as plik:
                plik.write(self.tekst.get(1.0, tk.END))

    def czy_zapisac(self):
        ''' Wykorzystywana do zapytania uzytkownika czy zapisac dany projekt '''
        if self.tekst.edit_modified():
            odp = messagebox.askyesnocancel("Zapisz", "Czy chcesz zapisać zmiany?")
            if odp:
                self.zapisz_plik()
            return odp is not None
        return True

    def zamknij(self):
        ''' Wykorzystywana do zamkniecia programu po wcześniejszym zaptaniu uzytknownika o zapis '''
        if self.czy_zapisac():
            self.root.destroy()
    
    def zaznacz_wszystko(self):
        '''Zaznaczanie całego tekstu w edytorze'''
        self.tekst.tag_add("sel", "1.0", "end-1c")
        self.tekst.mark_set("insert", "1.0")
        self.tekst.see("insert")


if __name__ == "__main__":
    root = tk.Tk()
    app = Notatnik(root)
    root.mainloop()
