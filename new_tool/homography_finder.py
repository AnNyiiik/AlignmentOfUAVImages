from abc import ABC, abstractmethod

class homography_finder(ABC):

    @abstractmethod
    def align(self, img_query, img_reference):
        pass
