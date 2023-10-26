import mysql.connector
from PyQt5 import uic, QtWidgets

numero_id = 0

conexao = mysql.connector.connect(
    host= 'localhost',
    user= 'root',
    password= '1234',
    database= 'cadastro_pessoas'
)

def principal():
    nome = cadastro.lineEdit.text()
    email = cadastro.lineEdit_2.text()
    idade = cadastro.lineEdit_3.text()
    print("nome", nome)
    print("email", email)
    print("idade", idade)
    
    genero = ""
    
    if cadastro.radioButton.isChecked():
        print("Feminino")
        genero = "Feminino"
    elif cadastro.radioButton_2.isChecked():
        print("Masculino")
        genero = "Maculino"
    else: 
        print("Prefiro não responder")
        genero = "Prefiro não responder"
        
    cursor = conexao.cursor()
    
    comando = 'INSERT INTO pessoas (nome, email, idade, genero) VALUES (%s, %s, %s, %s)'
    dados = (str(nome), str(email), str(idade), genero)
    cursor.execute(comando, dados)
    conexao.commit()
    
    cadastro.lineEdit.setText("")
    cadastro.lineEdit_2.setText("")
    cadastro.lineEdit_3.setText("")

def tela_lista():
    lista.show()    
    cursor = conexao.cursor()
    comando = 'SELECT * FROM pessoas'
    cursor.execute(comando)   
    dados = cursor.fetchall()
    print(dados) 
    
    lista.tableWidget.setRowCount(len(dados))
    lista.tableWidget.setColumnCount(5)

    for i in range(0, len(dados)):
        for j in range(0, 5):
            lista.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados[i][j])))
    
def tela_editar():
    global numero_id
    linha = lista.tableWidget.currentRow()
    cursor = conexao.cursor()
    cursor.execute('SELECT id FROM pessoas')
    dados = cursor.fetchall()
    valor_id = dados[linha][0]
    cursor.execute('SELECT * FROM pessoas WHERE id='+str(valor_id))
    nome = cursor.fetchall()
    
    genero = ""
    
    numero_id = valor_id
    
    editar.lineEdit.setText(str(nome[0][1]))
    editar.lineEdit_2.setText(str(nome[0][2]))
    #editar.lineEdit_4.setText(str(nome[0][1]))
    editar.lineEdit_3.setText(str(nome[0][3]))
    
    conexao.commit()
    editar.show()
    

def salvar_dados():
    global numero_id
    nome = editar.lineEdit.text()
    email = editar.lineEdit_2.text()
    idade = editar.lineEdit_3.text()
   
    if editar.radioButton.isChecked():
        genero = "Feminino"
    elif editar.radioButton_2.isChecked():
        genero = "Masculino"
    else:
        genero = "Prefiro não responder"
    
    cursor = conexao.cursor()
    cursor.execute(f'UPDATE pessoas SET nome = "{nome}", email = "{email}", idade = "{idade}", genero = "{genero}" WHERE id = {numero_id}')
    
    editar.close()
    lista.close()
    tela_lista()
    conexao.commit()
    
def excluir_dados():
    linha = lista.tableWidget.currentRow()
    lista.tableWidget.removeRow(linha)
    
    cursor = conexao.cursor()
    cursor.execute('SELECT id FROM pessoas')
    dados = cursor.fetchall()
    valor_id = dados[linha][0]
    cursor.execute('DELETE FROM pessoas WHERE id='+str(valor_id))
    conexao.commit()

app = QtWidgets.QApplication([])
cadastro = uic.loadUi("cadastro.ui")
lista = uic.loadUi("lista.ui")
editar = uic.loadUi("editar.ui")
cadastro.pushButton.clicked.connect(principal)
cadastro.pushButton_2.clicked.connect(tela_lista)
lista.pushButton.clicked.connect(tela_editar)
editar.pushButton.clicked.connect(salvar_dados)
lista.pushButton_2.clicked.connect(excluir_dados)

cadastro.show()
app.exec()