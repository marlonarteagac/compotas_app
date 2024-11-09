
import sqlite3

def Conexion(base_datos, consulta_sql, datos=None):
    try:
        conn = sqlite3.connect(base_datos)  # Conexión a la base de datos
        cursor = conn.cursor()
        
        if datos:
            cursor.execute(consulta_sql, datos)  # Ejecutar consulta con parámetros
        else:
            cursor.execute(consulta_sql)  # Ejecutar consulta sin parámetros

        if consulta_sql.strip().upper().startswith("SELECT"):
            resultado_consulta = cursor.fetchall()  # Obtener todos los resultados para SELECT
        else:
            conn.commit()  # Confirmar transacción para INSERT, UPDATE, DELETE
            resultado_consulta = cursor.rowcount  # Devolver número de filas afectadas

        cursor.close()  # Cerrar el cursor
        return resultado_consulta

    except sqlite3.Error as e:
        print(f"Error en la conexión a la base de datos : {e}")
        return None

    finally:
        conn.close()  # Cerrar la conexión a la base de datos




