

class Workout():

    def __init__(self, name, date, status, id, wrkt_df=[]):
        self._name = name
        self._date = date
        self._status = status
        self._id = id
        self._wrkt_df = wrkt_df

    @property
    def name(self):
        return self._name

    @property
    def date(self):
        return self._date

    @property
    def status(self):
        return self._status

    @property
    def id(self):
        return self._id

    @property
    def wrkt_df(self):
        return self._wrkt_df

    @name.setter
    def name(self, x):
        self._name = x

    @date.setter
    def date(self, x):
        self._date = x

    @status.setter
    def status(self, x):
        self._status = x

    @id.setter
    def id(self, x):
        self._id = x

    @wrkt_df.setter
    def wrkt_df(self, x):
        self._wrkt_df = x