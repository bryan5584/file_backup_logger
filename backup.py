import os
import shutil
from datetime import datetime
import time
import zipfile

class BackupManager:
    def __init__(self, source_folder, backup_root, log_file="backup.log"):
        self.source_folder = source_folder
        self.backup_root = backup_root
        self.log_file = log_file

    def perform_backup(self, compress=False):
        if not os.path.exists(self.source_folder):
            self.log_backup("ÉCHEC - Dossier source introuvable")
            raise FileNotFoundError(f"Le dossier source n'existe pas : {self.source_folder}")

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_folder_name = f"backup_{timestamp}_v1.0"
        backup_path = os.path.join(self.backup_root, backup_folder_name)

        start_time = time.time()
        try:
            shutil.copytree(self.source_folder, backup_path)
            file_count = self.count_files(self.source_folder)
            if compress:
                zip_path = self.compress_backup(backup_path)
                duration = time.time() - start_time
                self.log_backup(f"SUCCÈS - Sauvegarde compressée dans : {zip_path} | Fichiers copiés : {file_count} | Durée : {duration:.2f}s")
                shutil.rmtree(backup_path)
                return zip_path, file_count, duration
            else:
                duration = time.time() - start_time
                self.log_backup(f"SUCCÈS - Sauvegarde dans : {backup_path} | Fichiers copiés : {file_count} | Durée : {duration:.2f}s")
                return backup_path, file_count, duration
        except Exception as e:
            self.log_backup(f"ÉCHEC - Erreur : {e}")
            raise e

    def compress_backup(self, folder_path):
        zip_name = f"{folder_path}.zip"
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=folder_path)
                    backup_zip.write(file_path, arcname)
        return zip_name

    def count_files(self, folder):
        total_files = 0
        for root, dirs, files in os.walk(folder):
            total_files += len(files)
        return total_files

    def log_backup(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as log:
            log.write(f"[{timestamp}] {message}\n")
