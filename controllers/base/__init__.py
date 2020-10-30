"""Base classes for the data controllers."""
from .config import MONGO_CLIENT
from .ctrl import BaseCollection
from .ctrl_lang import MultilingualDataController, MultilingualGetOneResult
from .ctrl_lang_post import MultilingualPostController, MultilingualPostKey
from .post_mod import ModifiableDataKey
