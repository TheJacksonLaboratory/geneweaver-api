"""A namespace for the initialized Geneweaver API configuration."""
from geneweaver.db.core.settings_class import Settings as DBSettings

from geneweaver.api.core.config_class import GeneweaverAPIConfig

settings = GeneweaverAPIConfig()

db_settings = DBSettings()
