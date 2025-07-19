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
        self.data_path = os.path.join(r'/home/oa/projects/uni/data', f"{file_name}")
        self.data_folder = r'/home/oa/projects/uni/data'
        self.original_name = file_name
        self.updated_path = os.path.join(self.data_folder, f"{file_name}_updated.csv")

        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"No se encontró el archivo: {self.data_path}")

        
        try:
            self.df = pd.read_csv(self.updated_path)
            self.df = self.format_data(self.df)
            logging.info(f"Loaded updated data from: {self.updated_path}")
        
        except Exception as e:
            logging.error(f"Failed to load updated data, falling back to PDF: {e}")
            self.df = self.load_from_pdf_and_format()
    
            
            
        

    def save(self):
        self.df.to_csv(self.updated_path, index=False)

    def remove_accents(self,input_str):
        # Normaliza a forma decomposed (NFD), separa letras de acentos y elimina los acentos
        nfkd_form = unicodedata.normalize('NFD', input_str)
        only_ascii = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
        return only_ascii

    def load_from_pdf_and_format(self):
        self.pattern = r"([A-Z]{3,}-\d{3})\s+(.+?)\s+(\d{1,2})\s+([A-Z\-0-9,]*)"
        self.data = []
        with pdfplumber.open(self.data_path) as pdf:
            full_text = "\n".join(page.extract_text() for page in pdf.pages)
        matches = re.findall(self.pattern, full_text)
        for match in matches:
            clave, nombre, credito, pre_req = match
            self.data.append({
                "clave": clave.strip(),
                "asignatura": nombre.strip(),
                "credito": credito.strip(),
                "pre_req": pre_req.strip()
            })
        df = pd.DataFrame(self.data)
        return self.format_data(df)


    def format_data(self, df):
        df['completo'] = pd.Series([False]*len(df), dtype='bool')  # default False
        df['mes_cursado'] = pd.Series([pd.NaT]*len(df), dtype='datetime64[ns]')
        df['nota'] = pd.Series([np.nan]*len(df), dtype='float')
        df['clave'] = df['clave'].astype(str)
        df['asignatura'] = df['asignatura'].astype(str)
        df['credito'] = df['credito'].astype(int)
        df['pre_req'] = df['pre_req'].astype(str)
        empty_req = df['pre_req'] == '-'
        df.loc[empty_req, 'pre_req'] = "" 
        return df
    
    def __str__(self):
        return self.df
    
    def completed_summary(self):
        avg = self.df['nota'].mean()
        total = len(self.df)
        completed_x = len(self.df[self.df['completo'] == True])
        missing = len(self.df[self.df['completo'] != True])

        mapping = {
            'avg' : avg,
            'total' : total,
            'completed' : completed_x,
            'missing' : missing
        }
        return mapping

    
    def edit_record(self, subject, month, grade: float):
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
            self.df.at[idx, 'completo'] = True
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
    print(loader.df) 








