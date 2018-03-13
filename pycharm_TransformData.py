import csv
import os


cwd = os.getcwd()

data_type = 'real' #select 'real' or 'test' data

source1 = cwd + '/' + data_type + 'data/companylist.csv'
source2 = cwd + '/' + data_type + 'data/ratios.csv'
output_path = cwd + '/output/output.csv'

##IMPORT
with open(source1, 'r') as fp:
    reader = csv.reader(fp, delimiter=',', quotechar='"')
    company_list = [row for row in reader]

with open(source2, 'r') as fp:
    reader = csv.reader(fp, delimiter=',', quotechar='"')
    ratios = [row for row in reader]

#Add PRC row to the table
output = ratios #store in modifyable table to not corrupt inital values
output[0].append(company_list[0][6]) #adds price header to list
#loop through both tables
for rowR in output:
    for rowC in company_list:
        if rowR[0] == rowC[0]: #company code must be the same
            if rowC[1][3:] == rowR[3][3:]: #public_date(ratios) must be the same as date(companylist) only looking at month and year (publishing dates by actual day can differ)
                rowR.append(rowC[6])



#Store modified data in a .csv file, which can then be used for analysis
def export_matrix_to_csv(output_path, matrix):
    with open(output_path, "w") as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n')
        writer.writerows(matrix)
    print('export done successfully')


#transpose a matrix
def transpose_matrix(matrix):
    N = len(matrix)
    C = len(matrix[0])
    column_list = [[matrix[row][column] for row in range(N)] for column in range(C)]
    return column_list

#TODO 1 converts matrix into floats from strings, if headerrow is not available headerrow = 0
def convert_matrix_to_float(matrix, headerrow_available = 1):
    return None


#extracts a column from matrix with header = columnheader and returns it as an array
def extract_column(matrix, columnheader):
    i = 1
    #calculates position in which the column with columnheader is located in the original matrix
    for item in matrix[0]:
        if item == columnheader:
            column_position = i
        i += 1
    t_matrix = transpose_matrix(matrix)
    column = t_matrix[column_position-1]
    column = column[1:] #remove header
    c_column = [float(numeric_string) for numeric_string in column] #convert string array into float array TODO 2 remove after TODO 1
    return c_column


def calculate_return(price, months = 1):
    i = 0
    k = 0
    z = 0
    data_range_per_permo = 120
    r3turn = []
    r3turn.append('return' + str(months) + 'months')
    while i in range(0,len(price)):
        if i in range (data_range_per_permo*k,data_range_per_permo*k+months):
            r3turn.append('NaN')
            z += 1
            if z == months:
                z = 0
                k += 1
        else:
            r3turn.append((price[i]/price[i-months])-1)
        i += 1
    return r3turn

def add_return_to_output(r3turn, output):
    i = 0
    for row in output:
        row.append(r3turn[i])
        i += 1
    print(output)
    return None

price = extract_column(ratios, 'PRC')
add_return_to_output(calculate_return(price,2),output)
add_return_to_output(calculate_return(price,3),output)
export_matrix_to_csv(output_path,output)