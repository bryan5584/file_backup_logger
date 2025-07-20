from backup import BackupManager

if __name__ == "__main__":
    source = input("Path of the folder to backup: ")
    destination = input("Backup destination path: ")
    compress_input = input("Do you want to compress the backup as ZIP? (y/n): ").lower()
    compress = compress_input == 'y'

    manager = BackupManager(source, destination)
    try:
        backup_path, file_count, duration = manager.perform_backup(compress=compress)
        print(f"Backup successful at: {backup_path}")
        print(f"Files copied: {file_count}")
        print(f"Duration: {duration:.2f} seconds")
    except Exception as e:
        print(f"Error: {e}")
