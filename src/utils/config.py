import os

documents_cache_file = os.path.join('cache', 'documents.joblib')

model_cache_file = os.path.join('cache', 'model.joblib')

document_dirs = os.getenv('DOCUMENT_DIRS').split(':')

bot_token = os.getenv('BOT_TOKEN')
