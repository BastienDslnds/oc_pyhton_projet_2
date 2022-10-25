from IPython.core.display_functions import clear_output

tournament = {
    "1": {'description': "créer un nouveau tournoi", 'on_choice': "A"},
    "2": {'description': "Reprendre un tournoi", 'on_choice': "B"}
}

round = {
    "1": {'description': "Créer un nouveau round", 'on_choice': "C"},
    "2": {'description': "Reprendre un round", 'on_choice': "D"}
}

match = {
    "1": {'description': "Sélectionner un type de match", 'on_choice': "E"},
    "2": {'description': "Assigner les scores", 'on_choice': "F"}
}

player = {
    "1": {'description': "Sélectionner des joueurs", 'on_choice': "G"},
    "2": {'description': "Créer de nouveaux joueurs", 'on_choice': "H"}
}

report = {
    "1": {'description': "Afficher le classement des joueurs", 'on_choice': "I"},
    "2": {'description': "Assigner les statistiques d'un tournoi", 'on_choice': "J"}
}

home = {
    "1": {'description': "Gérer les tournois", 'on_choice': tournament},
    "2": {'description': "Gérer les rounds", 'on_choice': round},
    "3": {'description': "Gérer les matchs", 'on_choice': match},
    "4": {'description': "Gérer les joueurs", 'on_choice': player},
    "5": {'description': "Afficher les rapports", 'on_choice': report}
}

main = home
while True:
    print(len(main))
    if len(main) == 1:
        break
    else:
        for element in main:
            print(element)
            print(main)
            print(f"Choice [{element}] - {main[element]['description']}")

        choice = input("Entrez un choix valide ou la lettre Q pour quitter l'application: ")

        if choice == 'Q':
            break
        elif choice in main:
            main = main[choice]['on_choice']
        else:
            print("Le choix n'est pas valide.")

print(main)
