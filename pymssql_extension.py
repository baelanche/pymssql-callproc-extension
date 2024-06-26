import pymssql
from typing import Union, Optional
from datetime import datetime
 
class Mssql:
    session: pymssql.Cursor
 
    def __init__(self):
        conn = pymssql.connect(
            r'(local)', #hostname
            'test',     #username
            'test',     #password
            'test'      #dbname
        )
        cursor = conn.cursor()
        self.session = cursor
 
    def __get_type__(self, value: Union[int, str, float, bool, datetime]) -> str:
        if isinstance(value, int):
            return 'INT'
        elif isinstance(value, str):
            return 'VARCHAR(MAX)'
        elif isinstance(value, float):
            return 'FLOAT'
        elif isinstance(value, bool):
            return 'BIT'
        elif isinstance(value, datetime):
            return 'DATETIME'
        else:
            raise ValueError(f"Unsupported type: {type(value)}")
         
    def query(self, query: str):
        self.session.execute(query)
        return self.session.fetchall()
     
    def stored_procedure(self, procedure_name: str, inputs: dict, outputs: Optional[dict] = None):
        if outputs is None:
            params = tuple(inputs.values())
            self.session.callproc(procedure_name, params)
            return self.session.fetchall()
        else:
            in_desc = ' '.join(f'DECLARE @{key} {self.__get_type__(value)} = {value}' for key, value in inputs.items())
            out_desc = ' '.join(f'DECLARE @{key} {self.__get_type__(value)}' for key, value in outputs.items())
            in_assign = ', '.join(f'@{key}' for key in inputs.keys())
            out_assign = ', '.join(f'@{key} OUTPUT' for key in outputs.keys())
            select = ', '.join(f'@{key} as {key}' for key in outputs.keys())

            query = f'{in_desc} {out_desc}; EXEC {procedure_name} {in_assign}, {out_assign}; SELECT {select};'

            self.session.execute(query)
            result = self.session.fetchall()
            while outputs:
                if self.session.nextset():
                    outputs = self.session.fetchall()
                else:
                    return result, outputs

            return result, None
        
def get_mssql_session():
    mssql = Mssql()
    try:
        yield mssql
    finally:
        mssql.session.close()
