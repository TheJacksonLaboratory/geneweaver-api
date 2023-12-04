"""A namespace for the initialized Geneweaver API configuration."""
from geneweaver.api.core.config_class import GeneweaverAPIConfig
from geneweaver.db.core.settings_class import Settings as DBSettings

settings = GeneweaverAPIConfig()

db_settings = DBSettings()
