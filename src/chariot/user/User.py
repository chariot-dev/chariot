from chariot.user import UserConfiguration

class User:
    def __init__(self, config: UserConfiguration):
        self._config: UserConfiguration = config

    def getUserName(self) -> str:
        return self._config.username

    def getPassword(self) -> str:
        return self._config.password

    def getEmail(self) -> str:
        return self._config.eMail

    def getFullName(self) -> str:
        return self._config.fullName