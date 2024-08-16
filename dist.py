import shutil
import os

def prepare_dist():
    # Define os diretórios de origem e destino
    source_dirs = ['_pages', '_css', '_image', '_scripts', '_models_print']
    dest_dir = 'dist'
    
    # Verifica se o diretório dist existe
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Copia os diretórios para o dist
    for dir_name in source_dirs:
        src = os.path.join(dir_name)
        dst = os.path.join(dest_dir, dir_name)
        if os.path.exists(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            print(f"Diretório de origem não encontrado: {src}")

if __name__ == "__main__":
    prepare_dist()
    print("Preparação do diretório dist concluída!")
