# backend/annotation_types/base.py

from abc import ABC, abstractmethod

class BaseAnnotation(ABC):
    """
    Interface or abstract base class for annotation types.
    Different annotation logic can inherit this class and implement their own methods.
    """

    @abstractmethod
    def get_next_data(self, username: str):
        """
        Get the next data that has not been annotated by the user.
        :param username: The username for assigning tasks.
        :return: dict or None
        """
        pass

    @abstractmethod
    def submit_annotation(self, data_id: int, username: str, score: int):
        """
        Submit the annotation result.
        """
        pass

    @abstractmethod
    def get_progress(self, username: str):
        """
        Get the annotation progress of the user.
        """
        pass
