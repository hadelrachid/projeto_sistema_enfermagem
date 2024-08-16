
class Update:
    def __init__(self, browsers):
        
        self.__browsers = browsers
        
        # Mapeando os campos principais para quando alternar as abas 
        # dos formulários 1 para o Formulário 3 e fazer uma atualização 
        # dos campos principais no formulário 3
        self.field_mapping = {
            "upa_selection": "upa_selection",
            "date_field": "date_field",
            "unit": "unit",
            "name": "name",
            "faa": "faa",
            "sector": "sector",
            "bed": "bed"
        }
        
        self.__updateForm3()
            
    # Função para obter o valor do campo do form1 e atualizar o form3    
    def __updateForm3(self): 
        # Iterar sobre o dicionário de mapeamento para obter e definir valores dos campos
        for form1_id, form3_id in self.field_mapping.items():
            self.__browsers[0].page().runJavaScript(
                f'document.getElementById("{form1_id}").value', lambda value, form3_id=form3_id: self.__setForm3Data(value, form3_id)
            )
            
    # Callback para definir o valor no form3 após obtê-lo do form1
    def __setForm3Data(self, value, form3_id):
        # Callback para definir o valor no form3 após obtê-lo do form1
        if value:
            self.__browsers[1].page().runJavaScript(f'document.getElementById("{form3_id}").value = "{value}";')
            