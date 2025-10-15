from repositories.base_repository import BaseRepository
from media.models import Media

class MediaRepository(BaseRepository[Media]):
    """
    Initializes the MediaRepository class, inheriting from BaseRepository and setting the model to Media.
    This repository handles CRUD operations for the Media model.
    """
    def __init__(self):
        super().__init__(Media)

    