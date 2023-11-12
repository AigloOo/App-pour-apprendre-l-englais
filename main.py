import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk
import random
import pickle

class VocabApp:
    def __init__(self, master):
        self.master = master
        self.master.title("L'App de Vocab de Mr. Tam")

        try:
            with open("vocab_data.pkl", "rb") as file:
                self.words = pickle.load(file)
        except FileNotFoundError:
            self.words = {}

        # Créer les composants de l'interface
        self.style = ttk.Style()
        self.style.configure('TButton', padding=5, width=20)

        self.word_list_label = tk.Label(master, text="Liste des mots:")
        self.word_list_label.pack()

        self.word_listbox = tk.Listbox(master)
        self.word_listbox.pack(fill=tk.BOTH, expand=True)

        self.add_button = ttk.Button(master, text="Ajouter un mot", command=self.add_word)
        self.add_button.pack()

        self.remove_button = ttk.Button(master, text="Supprimer le mot sélectionné", command=self.remove_word)
        self.remove_button.pack()

        self.play_button = ttk.Button(master, text="Jouer", command=self.start_game)
        self.play_button.pack()

        self.quit_button = ttk.Button(master, text="Quitter", command=self.master.destroy)
        self.quit_button.pack()

        # Ajouter un bouton d'arrêt de jeu (invisible au début)
        self.stop_button = ttk.Button(master, text="Arrêter le jeu", command=self.stop_game)
        self.stop_button.pack_forget()

        # Remplir la liste des mots
        for word, translation in self.words.items():
            self.word_listbox.insert(tk.END, f"{word} - {translation}")

        self.master.geometry("400x450")

    def add_word(self):
        word = simpledialog.askstring("Ajouter un mot", "Entrez le mot en anglais:")
        if word:
            translation = simpledialog.askstring("Ajouter un mot", f"Traduction de '{word}' en français:")
            if translation:
                self.words[word] = translation
                self.word_listbox.insert(tk.END, f"{word} - {translation}")
                self.save_words()

    def remove_word(self):
        selected_index = self.word_listbox.curselection()
        if selected_index:
            selected_word = self.word_listbox.get(selected_index)
            word, _ = selected_word.split(" - ")
            del self.words[word]
            self.word_listbox.delete(selected_index)
            self.save_words()

    def start_game(self):
        if not self.words:
            messagebox.showinfo("Avertissement", "Ajoutez des mots avant de jouer.")
            return

        self.play_button.pack_forget()
        self.stop_button.pack()

        self.play_game()

    def play_game(self):
        random_word = random.choice(list(self.words.keys()))
        correct_translation = self.words[random_word]

        user_translation = simpledialog.askstring("Jeu", f"Traduction de '{random_word}' en français:")
        
        if user_translation is None:  # L'utilisateur a appuyé sur Annuler
            self.stop_game()
            return

        if user_translation == correct_translation:
            messagebox.showinfo("Bonne réponse", "Félicitations! Bonne réponse.")
        else:
            messagebox.showinfo("Réponse incorrecte", f"Réponse incorrecte. La réponse était: '{correct_translation}'.")
        
        self.play_game()

    def stop_game(self):
        self.play_button.pack()
        self.stop_button.pack_forget()

    def save_words(self):
        with open("vocab_data.pkl", "wb") as file:
            pickle.dump(self.words, file)

class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Application Principale")

        self.vocab_app = VocabApp(self.master)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
