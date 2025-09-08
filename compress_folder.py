import argparse
from pathlib import Path
import zipfile
from datetime import datetime
def compress_folder(folder: Path, out_path: Path = None, recursive: bool = True):
    folder = folder.expanduser().resolve()
    if out_path is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = folder / f"{folder.name}_archivos_{ts}.zip"
    else:
        out_path = out_path.expanduser().resolve()
    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        if recursive:
            for f in folder.rglob("*"):
                if f.is_file() and f != out_path:
                    zf.write(f, arcname=f.relative_to(folder))
        else:
            for f in folder.iterdir():
                if f.is_file() and f != out_path:
                    zf.write(f, arcname=f.name)
    print(f"Creado: {out_path}")
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--folder", "-f", default=".", help="Carpeta a comprimir")
    p.add_argument("--out", "-o", default=None, help="Ruta o nombre del zip de salida")
    p.add_argument("--no-recursive", action="store_true", help="No incluir subcarpetas")
    args = p.parse_args()
    folder = Path(args.folder)
    out = Path(args.out) if args.out else None
    compress_folder(folder, out, recursive=not args.no_recursive)
if __name__ == "__main__":
    main()
