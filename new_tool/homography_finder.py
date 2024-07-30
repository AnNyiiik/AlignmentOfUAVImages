from abc import ABC, abstractmethod

class homography_finder(ABC):

    @abstractmethod
    def align(self, img_query_path, img_reference_path):
        pass
