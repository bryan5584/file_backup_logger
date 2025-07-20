from backup import BackupManager

if __name__ == "__main__":
    source = input("Chemin du dossier à sauvegarder : ")
    destination = input("Chemin de destination de la sauvegarde : ")
    compress_input = input("Voulez-vous compresser la sauvegarde en ZIP ? (o/n) : ").lower()
    compress = compress_input == 'o'

    manager = BackupManager(source, destination)
    try:
        backup_path, file_count, duration = manager.perform_backup(compress=compress)
        print(f"Sauvegarde réussie dans : {backup_path}")
        print(f"Fichiers copiés : {file_count}")
        print(f"Durée : {duration:.2f} secondes")
    except Exception as e:
        print(f"Erreur : {e}")
