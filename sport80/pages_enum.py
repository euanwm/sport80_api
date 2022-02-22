""" Throw all the endpoint strings in here """
import enum


class EndPoint(enum.Enum):
    """ As mentioned before... """
    EVENT_INDEX = "event_results?id_ranking=8"
    EVENT_RESULTS = f"{EVENT_INDEX}&resource="

if __name__ == '__main__':
    print(EndPoint.EVENT_RESULTS.value)