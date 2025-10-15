from repositories.media_repository import MediaRepository

class MediaService: 

    # Initializes the MediaService with the MediaRepository
    def __init__(self):
        self.media_repo = MediaRepository()
    
    """
    Saves media data to the repository
    Use the media repository to create and save the media data
    Return the result of the create operation
    """
    def saveMedia(self, data):

        return self.media_repo.create(data)
    




