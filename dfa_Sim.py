import tkinter as tk
from tkinter import messagebox

class DFA:
    def __init__(self, num_states, alphabet, initial_state, final_states, transition_relation):
        self.num_states = num_states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.final_states = final_states
        self.transition_relation = transition_relation

    def run(self, input_string):
        current_state = self.initial_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                raise ValueError("Symbol not in alphabet")
            current_state = self.transition_relation[(current_state, symbol)]
        return current_state in self.final_states


class DFAGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DFA Simulator")
        self.root.geometry("700x600")

        self.entries = {}
        self.transition_entries = {}

        self.build_main_inputs()

    def build_main_inputs(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        fields = [
            ("Number of States", "states"),
            ("Alphabet (space separated)", "alphabet"),
            ("Initial State", "initial"),
            ("Final States (space separated)", "final")
        ]

        for i, (label, key) in enumerate(fields):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky="w")
            entry = tk.Entry(frame, width=30)
            entry.grid(row=i, column=1, pady=5)
            self.entries[key] = entry

        tk.Button(
            self.root,
            text="Build DFA",
            command=self.build_transition_table,
            bg="#4CAF50",
            fg="white"
        ).pack(pady=10)

    def build_transition_table(self):
        try:
            self.num_states = int(self.entries["states"].get())
            self.alphabet = self.entries["alphabet"].get().split()
            self.initial_state = int(self.entries["initial"].get())
            self.final_states = list(map(int, self.entries["final"].get().split()))
        except:
            messagebox.showerror("Error", "Invalid DFA input")
            return

        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(pady=10)

        tk.Label(self.table_frame, text="Transition Table").grid(row=0, column=0, columnspan=5)

        for col, symbol in enumerate(self.alphabet):
            tk.Label(self.table_frame, text=symbol).grid(row=1, column=col + 1)

        for state in range(1, self.num_states + 1):
            tk.Label(self.table_frame, text=f"q{state}").grid(row=state + 1, column=0)
            for col, symbol in enumerate(self.alphabet):
                e = tk.Entry(self.table_frame, width=5)
                e.grid(row=state + 1, column=col + 1)
                self.transition_entries[(state, symbol)] = e

        self.build_test_section()

    def build_test_section(self):
        test_frame = tk.Frame(self.root)
        test_frame.pack(pady=20)

        tk.Label(test_frame, text="Input String").grid(row=0, column=0)
        self.test_entry = tk.Entry(test_frame, width=30)
        self.test_entry.grid(row=0, column=1, padx=10)

        tk.Button(
            test_frame,
            text="Test String",
            command=self.run_dfa,
            bg="#2196F3",
            fg="white"
        ).grid(row=0, column=2)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

    def run_dfa(self):
        try:
            transitions = {}
            for (state, symbol), entry in self.transition_entries.items():
                transitions[(state, symbol)] = int(entry.get())

            dfa = DFA(
                self.num_states,
                self.alphabet,
                self.initial_state,
                self.final_states,
                transitions
            )

            input_string = self.test_entry.get()
            result = dfa.run(input_string)

            if result:
                self.result_label.config(text="Accepted ✅", fg="green")
            else:
                self.result_label.config(text="Rejected ❌", fg="red")

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = DFAGUI(root)
    root.mainloop()
