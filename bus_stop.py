

class BusStop:

	def __init__(self, previous_stop, row):
		self.name = row['next_scheduled_stop_id']
		self.incoming_traffic = {previous_stop: row}

	def add_incoming_link(self, previous_stop, row):
		if previous_stop not in self.incoming_traffic:
			self.incoming_traffic[previous_stop] = row
		else:
			self.incoming_traffic[previous_stop] = self.incoming_traffic[previous_stop].append(row)
