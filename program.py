import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser


class Notatnik:
    """
    Prosty edytor tekstu oparty na tkinter.
    Pozwala użytkownikowi tworzyć, otwierać, edytować i zapisywać pliki tekstowe.
    Zawiera funkcje edycji oraz możliwość kolorowego zaznaczania tekstu.
    """

    def __init__(self, root):
        """
        Inicjalizuje interfejs aplikacji: tworzy pole tekstowe i menu.
        """
        self.root = root
        self.root.title("Mini Notatnik")
        self.root.geometry("600x400")

        # Główne pole tekstowe
        self.tekst = tk.Text(root, wrap="word", undo=True)
        self.tekst.pack(fill="both", expand=True)

        # Pasek menu
        self.menu = tk.Menu(root)
        root.config(menu=self.menu)

        # Menu "Plik"
        self.plik_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Plik", menu=self.plik_menu)
        self.plik_menu.add_command(label="Nowy", command=self.nowy_plik)
        self.plik_menu.add_command(label="Otwórz...", command=self.otworz_plik)
        self.plik_menu.add_command(label="Zapisz", command=self.zapisz_plik)
        self.plik_menu.add_separator()
        self.plik_menu.add_command(label="Wyjście", command=self.zamknij)

        # Menu "Edycja"
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

        # Menu "Narzędzia"
        self.narzedzia_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Narzędzia", menu=self.narzedzia_menu)
        self.narzedzia_menu.add_command(
            label="Zaznacz kolorem", command=self.zaznacz_tekst_kolorem
        )

    def nowy_plik(self):
        """
        Tworzy nowy dokument. Pyta o zapisanie zmian, jeśli są niezapisane.
        """
        if self.czy_zapisac():
            self.tekst.delete(1.0, tk.END)

    def otworz_plik(self):
        """
        Otwiera istniejący plik tekstowy. Pyta o zapisanie zmian przed otwarciem.
        """
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
        """
        Zapisuje aktualną zawartość edytora do pliku tekstowego.
        """
        sciezka = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Pliki tekstowe", "*.txt")]
        )
        if sciezka:
            with open(sciezka, "w", encoding="utf-8") as plik:
                plik.write(self.tekst.get(1.0, tk.END))

    def czy_zapisac(self):
        """
        Sprawdza, czy użytkownik chce zapisać zmiany przed kontynuacją.
        Zwraca True jeśli można kontynuować, False jeśli użytkownik anulował.
        """
        if self.tekst.edit_modified():
            odp = messagebox.askyesnocancel("Zapisz", "Czy chcesz zapisać zmiany?")
            if odp:
                self.zapisz_plik()
            return odp is not None
        return True

    def zamknij(self):
        """
        Zamyka aplikację po zapytaniu o zapis niezapisanych zmian.
        """
        if self.czy_zapisac():
            self.root.destroy()

    def zaznacz_tekst_kolorem(self):
        """
        Pozwala użytkownikowi wybrać kolor i zaznaczyć nim aktualnie wybrany tekst.
        Jeśli nie zaznaczono tekstu, wyświetla komunikat.
        """
        try:
            start = self.tekst.index(tk.SEL_FIRST)
            end = self.tekst.index(tk.SEL_LAST)
        except tk.TclError:
            messagebox.showinfo("Brak zaznaczenia", "Zaznacz tekst, który chcesz pokolorować.")
            return

        kolor = colorchooser.askcolor(title="Wybierz kolor zaznaczenia")[1]
        if kolor:
            tag = f"kolor_{kolor}"
            self.tekst.tag_config(tag, background=kolor)
            self.tekst.tag_add(tag, start, end)


if __name__ == "__main__":
    # Uruchomienie aplikacji
    root = tk.Tk()
    app = Notatnik(root)
    root.mainloop()
