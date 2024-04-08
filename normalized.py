import pymongo
from datetime import datetime

# Conectar ao banco de dados
client = pymongo.MongoClient("localhost", 27017)
db = client["8xesystem"]
collection = db["order"]

# Definir o novo valor para scheduled_at
novo_valor = datetime(2024, 4, 7, 0, 0, 0)

# Atualizar os documentos com scheduled_at igual a 2024-03-16T00:00:00.000Z
filtro = {"scheduled_at": datetime(2024, 3, 16, 0, 0, 0)}
atualizacao = {"$set": {"scheduled_at": novo_valor}}

# Executar a atualização
resultado = collection.update_many(filtro, atualizacao)

# Verificar o número de documentos atualizados
print("Documentos atualizados:", resultado.modified_count)

# Fechar a conexão com o banco de dados
client.close()
