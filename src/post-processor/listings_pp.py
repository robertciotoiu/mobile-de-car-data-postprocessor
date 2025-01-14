class CarListingsProcessor:
    def __init__(self, collection, postprocessed_collection, batch_size=1000):
        self.collection = collection
        self.postprocessed_collection = postprocessed_collection
        self.batch_size = batch_size
        self.post_processors = []

    def add_post_processor(self, post_processor):
        self.post_processors.append(post_processor)

    def process_listings(self):
        processed_cars = []
        for car in self.collection:
            for post_processor in self.post_processors:
                car = post_processor.process(car)
            processed_cars.append(car)
            if len(processed_cars) == self.batch_size:
                self.postprocessed_collection.insert_many(processed_cars)
                processed_cars = []
        if processed_cars:
            self.postprocessed_collection.insert_many(processed_cars)