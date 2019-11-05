import pandas as pd
import sys, os
sys.path.insert(0,'/home/nathan/Documents/codes/darf/darf-stock-back/model')
sys.path.insert(0,'/home/nathan/Documents/codes/darf/darf-stock-back/service')
from financial_operation import FinancialOperation
from taxes import TaxCalculator
import tabula
class XPFlavor:
    
    def read_pdf(self,file):
        filename = file
        multiple_tables = tabula.read_pdf(filename, 
                                          stream=True, 
                                          guess=False, 
                                          multiple_tables=True, 
                                          area=(30,1,50,100), 
                                          relative_area=True)
        print(multiple_tables)
        return multiple_tables[0]
        # 1 - Op_type
        # 3 - Name
        # 6 - Quantidade
        # 7 - preco
        # print(multiple_tables[0][7])
    def read_test(self): 
        dados = [['C','AES TIETE E',2000,10.0],['V','AES TIETE E',2000,30.0], ['V','VALE TIETE E',2000,30.0]]
        return pd.DataFrame(dados, columns = ['0', '1', '2', '3'])
        

    def create_financial_op(self, line):
        # return FinancialOperation(line[1], line[3], line[6], line[7])
        return FinancialOperation(line[0],line[1],line[2],line[3])

if __name__ == "__main__":
    file = 'samples/xp-2.pdf'
    # print (sys.path)
    xp = XPFlavor()
    # data_matrix = xp.read_pdf(file)
    # xp.read_test()
    data_matrix =xp.read_test()
    lines = data_matrix.apply(xp.create_financial_op, axis=1)
    TaxCalculator.calculate_tax(lines)
    #print(lines)