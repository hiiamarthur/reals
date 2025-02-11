from app.controllers.data_controller import DataController
from app.models.itinerary import Itinerary

class ItineraryController(DataController):
    def __init__(self):
        super().__init__(Itinerary)