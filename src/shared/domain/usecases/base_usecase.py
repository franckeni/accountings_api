from pydantic import BaseModel, ConfigDict, PrivateAttr

from shared.domain.repositories.base_repository import BaseRepository


class BaseUsecase(BaseModel):
    """Abstract Class for all Usecase

    Attributes
    ----------
    repo: BaseRepository
        A concrete implementation of BaseRepository class
        to interact with the database


    Methods
    -------
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    _repo: BaseRepository = PrivateAttr()

    def __init__(self, **datas):
        super().__init__(**datas)

        self._repo = datas["repo"]
