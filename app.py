from flask import Flask, render_template, request, jsonify
import fdb
import sys

app = Flask(__name__)

DB_HOST = 'localhost' 
DB_PATH = r'C:\Reswincs\Banco\RESULTH.FB' 
DB_USER = 'SYSDBA'
DB_PASS = 'masterkey'

def get_db_connection():
    try:
        dsn = f"{DB_HOST}:{DB_PATH}"
        con = fdb.connect(dsn=dsn, user=DB_USER, password=DB_PASS, charset='UTF8')
        return con
    except Exception as e:
        print(f"Erro de Conexão Firebird: {e}")
        return None

# --- ROTAS ---

@app.route('/')
def hub():
    return render_template('index.html')

@app.route('/etiqueta-padrao')
def etiqueta_padrao():
    return render_template('padrao.html')

@app.route('/etiqueta-gondola')
def etiqueta_gondola():
    return render_template('gondola.html')

# --- API BUSCA PADRÃO (COM LOCALIZAÇÃO) ---
@app.route('/api/busca')
def busca_produto_padrao():
    termo = request.args.get('q', '').strip().upper()
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'erro': 'Erro de conexão com o Banco.'}), 500

    try:
        cur = conn.cursor()
        
        # SQL CORRIGIDO COM JOIN PARA BUSCAR O LOCAL
        sql = """
            SELECT FIRST 30 
                P.CODPROD, 
                P.DESCRICAO, 
                P.PRECO, 
                P.UNIDADESAIDA,
                L.DESCRICAO AS NOME_LOCAL
            FROM PRODUTO P
            LEFT JOIN LOCPROD L ON P.CODLOCAL = L.CODLOCAL
            WHERE 
                (UPPER(P.DESCRICAO) LIKE ?) 
                OR 
                (CAST(P.CODPROD AS VARCHAR(50)) LIKE ?)
            ORDER BY P.CODPROD ASC
        """
        termo_busca = f"%{termo}%"
        cur.execute(sql, (termo_busca, termo_busca))
        
        resultados = []
        for row in cur.fetchall():
            codigo_limpo = str(int(row[0])) if row[0] is not None else "0"
            resultados.append({
                'codigo': codigo_limpo,      
                'nome': row[1],             
                'preco': float(row[2]) if row[2] else 0.0, 
                'unidade': row[3],
                # Se row[4] (Local) vier vazio do banco, colocamos uma string vazia
                'local': row[4] if row[4] else "" 
            })
        return jsonify(resultados)

    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        conn.close()

# --- API 2: BUSCA PARA ETIQUETA DE GÔNDOLA ---
@app.route('/api/busca_gondola')
def busca_produto_gondola():
    termo = request.args.get('q', '').strip().upper()
    conn = get_db_connection()
    if not conn:
        return jsonify({'erro': 'Erro de conexão com o Banco.'}), 500

    try:
        cur = conn.cursor()
        
        # Relacionamento corrigido: P.ID_MARCA = M.ID
        sql = """
            SELECT FIRST 30 
                P.CODPROD, 
                P.DESCRICAO, 
                P.PRECO, 
                P.UNIDADESAIDA,
                CAST(P.REFERENCIA AS VARCHAR(100)) AS REFERENCIA,
                M.DESCRICAO AS NOME_MARCA
            FROM PRODUTO P
            LEFT JOIN CADMARCA M ON P.ID_MARCA = M.ID
            WHERE 
                (UPPER(P.DESCRICAO) LIKE ?) 
                OR 
                (CAST(P.CODPROD AS VARCHAR(50)) LIKE ?)
                OR
                (UPPER(CAST(P.REFERENCIA AS VARCHAR(100))) LIKE ?)
            ORDER BY P.CODPROD ASC
        """
        termo_busca = f"%{termo}%"
        cur.execute(sql, (termo_busca, termo_busca, termo_busca))
        
        resultados = []
        for row in cur.fetchall():
            codigo_limpo = str(int(row[0])) if row[0] is not None else "0"
            resultados.append({
                'codigo': codigo_limpo,      
                'nome': row[1],             
                'preco': float(row[2]) if row[2] else 0.0, 
                'unidade': row[3],
                'codbarras': row[4] if row[4] else "", 
                'marca': row[5] if row[5] else ""      
            })
        return jsonify(resultados)

    except Exception as e:
        print(f"Erro de SQL na busca da Gôndola: {str(e)}")
        return jsonify({'erro': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)