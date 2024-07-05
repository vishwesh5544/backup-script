import os
import sys
import shutil
import datetime

class Backup:
    def __init__(self, source_dir, dest_dir):
        # set source and destination directories
        self.source_dir = os.path.abspath(os.path.expanduser(source_dir))
        self.dest_dir = os.path.abspath(os.path.expanduser(dest_dir))

    def append_timestamp(self, filename):
        # append timestamp to filename
        base, ext = os.path.splitext(filename)
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{base}_{timestamp}{ext}"

    def backup_files(self):
        # Check if source and destination directories exist
        if not os.path.isdir(self.source_dir):
            return

        if not os.path.isdir(self.dest_dir):
            os.makedirs(self.dest_dir)

        # traverse the source directory
        for root, _, files in os.walk(self.source_dir):
            for file in files:
                # Get the source and destination file paths
                src_file_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_file_path, self.source_dir)
                dest_file_path = os.path.join(self.dest_dir, rel_path)

                # Ensure the destination directory exists
                dest_file_dir = os.path.dirname(dest_file_path)
                if not os.path.exists(dest_file_dir):
                    os.makedirs(dest_file_dir)

                # If the file already exists in the destination, append a timestamp
                if os.path.exists(dest_file_path):
                    dest_file_path = os.path.join(dest_file_dir, self.append_timestamp(file))

                # Copy the file to the destination
                shutil.copy2(src_file_path, dest_file_path)

def main():
    # use absolute path
    if len(sys.argv) != 3:
        return

    source_dir = sys.argv[1]
    dest_dir = sys.argv[2]

    backup = Backup(source_dir, dest_dir)
    backup.backup_files()

if __name__ == "__main__":
    main()
