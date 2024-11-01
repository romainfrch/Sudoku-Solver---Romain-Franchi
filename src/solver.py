from deduction_rule import DR1, DR2, DR3

class SudokuSolver:
    def __init__(self, grid):
        self.grid = grid
        self.rules = [DR1(grid), DR2(grid), DR3(grid)]
        self.history = [] 
        self.intervention_count = 0 

    def get_candidates(self, index):
        row, col = divmod(index, 9)
        candidates = set(range(1, 10))

        for i in range(9):
            candidates.discard(self.grid.grid[row * 9 + i])
            candidates.discard(self.grid.grid[i * 9 + col])

        box_start = (row // 3) * 27 + (col // 3) * 3
        for i in range(3):
            for j in range(3):
                candidates.discard(self.grid.grid[box_start + i * 9 + j])

        return list(candidates)

    def save_last_state(self, index):
        self.history.append((self.grid.grid[:], index))

    def restore_last_state(self, steps=1):
        if len(self.history) >= steps:
            for _ in range(steps):
                grid_state, _ = self.history.pop()
            self.grid.grid = grid_state[:]
            return True
        return False

    def solve(self):
        print("\n\033[93mGrille initiale :\033[0m")
        print("")
        self.grid.display_grid()
        print("")
        input("\033[94;5m[Appuyer sur n'importe quelle touche pour commencer]\033[0m")
        print("\n\033[92mDébut de la résolution...\033[0m\n")

        while not self.grid.is_grid_full():
            progress = False
            for rule in self.rules:
                result = rule.apply_rule()
                if result:
                    progress = True
                    index, value = result
                    row, col = divmod(index, 9)
                    print(f"\033[93;3mCellule remplie : Ligne {row + 1}, Colonne {col + 1} avec la valeur {value}\033[0m")
                    print("-" * 53)
                    break

            if not progress:
                # Vérification préalable des candidats pour chaque cellule vide
                any_candidates_left = False
                for i in range(81):
                    if self.grid.grid[i] == 0:  # Cellule vide
                        candidates = self.get_candidates(i)
                        if candidates:  # Si des candidats existent, il y a encore des solutions possibles
                            any_candidates_left = True
                            break

                if not any_candidates_left:
                    print(f"\033[91mERREUR : Aucune solution possible pour les cellules vides restantes.\033[0m")
                    print("\033[91mVous pouvez essayer de corriger les cellules.\033[0m")

                    while True:
                        action = input("\033[95mSouhaitez-vous abandonner (A), corriger la cellule (C), ou corriger 2/3 étapes avant (C2 / C3) ? \033[0m").lower()
                        if action == 'a':
                            print("\033[91mLa résolution a été abandonnée.\033[0m")
                            return
                        elif action in ['c', 'c2', 'c3']:
                            steps = {'c': 1, 'c2': 2, 'c3': 3}[action]
                            if self.intervention_count < steps:
                                print(f"\033[91mERREUR : Vous ne pouvez pas restaurer {steps} étapes en arrière.\033[0m")
                                continue
                            print(f"\033[93mRestauration de {steps} étapes en arrière...\033[0m")
                            if not self.restore_last_state(steps):
                                print("\033[91mERREUR : Pas assez d'étapes enregistrées pour restaurer.\033[0m")
                                return 
                            self.intervention_count -= steps
                            break
                        else:
                            print("\033[91mErreur : Action non reconnue, veuillez réessayer.\033[0m")
                    continue

                while True:
                    try:
                        self.grid.display_grid()
                        print("")
                        row = int(input("\033[96mEntrez le numéro de la ligne (1-9) : \033[0m")) - 1
                        col = int(input("\033[96mEntrez le numéro de la colonne (1-9) : \033[0m")) - 1
                        if row < 0 or row >= 9 or col < 0 or col >= 9:
                            print("\033[91mErreur : Veuillez entrer un numéro de ligne et de colonne entre 1 et 9.\033[0m")
                            continue
                        index = row * 9 + col
                        if self.grid.grid[index] != 0:
                            print(f"\033[91mErreur : La cellule (Ligne {row + 1}, Colonne {col + 1}) est déjà remplie.\033[0m")
                            continue
                        break
                    except ValueError:
                        print("\033[91mErreur : Veuillez entrer des nombres valides pour la ligne et la colonne.\033[0m")

                self.grid.display_grid_with_highlight(index)
                candidates = self.get_candidates(index)

                self.save_last_state(index)
                value = None
                while True:
                    try:
                        print("")
                        value = int(input(f"\033[96mEntrez une valeur pour la cellule (Ligne {row + 1}, Colonne {col + 1}) entre {candidates}: \033[0m"))
                        print("")
                        if value not in candidates:
                            print(f"\033[91mValeur invalide. Veuillez entrer un nombre parmi {candidates}.\033[0m")
                            continue
                        if self.grid.set_value(index, value):
                            self.intervention_count += 1 
                            break
                    except ValueError:
                        print("")
                        print("\033[91mEntrée invalide. Veuillez entrer un nombre entier.\033[0m")

        print("\n\033[92mSudoku résolu !\033[0m\n")
        self.grid.display_grid()
        print("")
        input("\033[94;5m[Appuyer sur n'importe quelle touche pour fermer]\033[0m")
