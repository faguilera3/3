from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    
    if file and file.filename.endswith('.xlsx'):
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        transform_data(file_path)
        return redirect(url_for('download'))
    else:
        return 'Invalid file format. Only .xlsx files are allowed.', 400

def transform_data(file_path):
    # Cargar el archivo de Excel
    df = pd.read_excel(file_path)

    # Definir la cantidad de columnas por bloque
    columns_per_block = 3

    # Crear un DataFrame vacío para los datos transformados
    transformed_data = pd.DataFrame()

    # Rellenar los encabezados y mover los datos
    for i in range(len(df)):
        block_number = i + 1
        col_names = [f"Plato {block_number}", f"Precio {block_number}", f"Descripcion {block_number}"]
        transformed_data = pd.concat([transformed_data, pd.DataFrame([df.iloc[i].values], columns=col_names)], axis=1)

    # Guardar los resultados en un nuevo archivo Excel
    new_excel_path = 'uploads/Precios-casino-transformado.xlsx'
    transformed_data.to_excel(new_excel_path, index=False)

    # Convertir el DataFrame a un archivo delimitado por tabulaciones
    new_txt_path = 'uploads/Precios-casino-transformado.txt'
    transformed_data.to_csv(new_txt_path, sep='\t', index=False, encoding='windows-1252', errors='ignore')

@app.route('/download')
def download():
    return render_template('download.html')

if __name__ == '__main__':
    app.run(debug=True)