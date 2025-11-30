import os
import zipfile

def zip_project(project_dir: str) -> str:
    zip_path = f"{project_dir}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(project_dir):
            for f in files:
                full = os.path.join(root, f)
                arc = os.path.relpath(full, project_dir)
                zf.write(full, arc)
    return zip_path
