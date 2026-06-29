from config.settings import Settings
settings = Settings()

def get_ollama_models_list():
    models_list = settings.OLLAMA_MODELS
    ollama_models = [models.strip() for models in models_list.split(",")]
    return ollama_models
