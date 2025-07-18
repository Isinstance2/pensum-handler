import pdfplumber
import pandas as pd
import re
import numpy as np
import os
import logging
import unicodedata



# Define el formato con timestamp
log_format = "%(asctime)s - %(levelname)s - %(message)s"

# Configura el archivo de log con formato
logging.basicConfig(
    filename="PensumLoader.log",
    level=logging.INFO,
    format=log_format,  # <-- Añade esta línea
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Handler para la consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Usa el mismo formato con timestamp
formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")
console_handler.setFormatter(formatter)

# Añade el handler de consola al logger raíz
logging.getLogger().addHandler(console_handler)



class PensumLoaderUnicaribe():
    def __init__(self, file_name):
        self.data_path = os.path.join(os.getcwd(), "data", f"{file_name}.pdf")

        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"No se encontró el archivo: {self.data_path}")
        
        self.pattern = r"([A-Z]{3,}-\d{3})\s+(.+?)\s+(\d{1,2})\s+([A-Z\-0-9,]*)"
        self.data = []
        with pdfplumber.open(self.data_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                full_text += page.extract_text() + "\n"
        matches = re.findall(self.pattern, full_text)
        for match in matches:
            clave, nombre, credito,pre_req = match
            self.data.append({
            "clave" : clave.strip(),
            "asignatura": nombre.strip(),
            "credito" : credito.strip(),
            "pre_req" : pre_req.strip()
            })
        self.df = pd.DataFrame(self.data)
        self.df = self.format_data(self.df)
        

    def remove_accents(self,input_str):
        # Normaliza a forma decomposed (NFD), separa letras de acentos y elimina los acentos
        nfkd_form = unicodedata.normalize('NFD', input_str)
        only_ascii = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
        return only_ascii


    def format_data(self, df):
        self.df['completo'] = pd.Series([False]*len(self.df), dtype='bool')  # default False
        self.df['mes_cursado'] = pd.Series([pd.NaT]*len(self.df), dtype='datetime64[ns]')
        self.df['nota'] = pd.Series([np.nan]*len(self.df), dtype='float')
        self.df['clave'] = self.df['clave'].astype(str)
        self.df['asignatura'] = self.df['asignatura'].astype(str)
        self.df['credito'] = self.df['credito'].astype(int)
        self.df['pre_req'] = self.df['pre_req'].astype(str)
        empty_req = self.df['pre_req'] == '-'
        self.df.loc[empty_req, 'pre_req'] = "" 
        return self.df
    
    def add_record(self, subject, month, grade: float):
        try:
            # Aplica remove_accents a toda la columna solo una vez y guarda en columna auxiliar
            if 'asignatura_limpia' not in self.df.columns:
                self.df['asignatura_limpia'] = self.df['asignatura'].apply(self.remove_accents).str.lower()

            # Limpia el argumento de búsqueda también (sin acentos y en minúsculas)
            subject_clean = self.remove_accents(subject).lower()

            # Busca en la columna limpia
            matches = self.df[self.df['asignatura_limpia'].str.contains(subject_clean, na=False)]

            if matches.empty:
                logging.warning(f"No match found for: {subject}")
                return

            if len(matches) > 1:
                logging.warning(f"Multiple matches found for '{subject}': {[m for m in matches['asignatura']]}")

            # Aplica solo a la primera coincidencia
            idx = matches.index[0]
            self.df.at[idx, 'nota'] = grade
            self.df.at[idx, 'mes_cursado'] = month
            logging.info(f"Assigned grade {grade} to subject: {self.df.at[idx, 'asignatura']}")
    
        except Exception as e:
            logging.error(f"Error assigning grade: {e}")


        

    
class PensumLoaderFactory:
    @staticmethod
    def get_loader(universidad, file_name):
        if universidad == "unicaribe":
            return PensumLoaderUnicaribe(file_name)
        elif universidad == "pucmm":
            pass
        else:
            raise ValueError("Universidad no soportada.")

if __name__ == '__main__':
    loader = PensumLoaderFactory.get_loader('unicaribe', 'PENSUM-Ingenieria-de-Datos-e-Inteligencia-Organizacional')
    print(loader.df.head())  # Para chequear que cargó bien