from dream.plugins import plugin
from dream.plugins.TimeSupport import TimeSupportMixin

class PostProcessOrderLateness(plugin.OutputPreparationPlugin, TimeSupportMixin):
  """ Postprocess order lateness for Input_viewResultOrderLateness
  """

  def postprocess(self, data):
    self.initializeTimeSupport(data)
    for result in data['result']['result_list']:
      order_lateness_dict = result[self.configuration_dict["output_id"]] = {}
      for obj in result['elementList']:
        if obj.get('_class') == "Dream.OrderDesign": # XXX How to find orders ?
          dueDate, = [order['dueDate'] for order in data['input']['BOM']['productionOrders'] if order['id'] == obj['id']]
          order_lateness_dict[obj["id"]] = {
            "dueDate": self.convertToFormattedRealWorldTime(dueDate),
            "delay": obj["results"].get("delay", 0), 
            "completionDate": self.convertToFormattedRealWorldTime(obj["results"]["completionTime"])
          }
        if obj.get('_class') == "Dream.CapacityProject": # XXX How to find orders ?
          dueDate, = [order['dueDate'] for order in data['input']['BOM']['productionOrders'] if order['id'] == obj['id']]
          if obj["results"]["schedule"]:
            completionTime = obj["results"]["schedule"][-1]["exitTime"]
            order_lateness_dict[obj["id"]] = {
              "dueDate": self.convertToFormattedRealWorldTime(dueDate),
              "delay": completionTime - dueDate,
              "completionDate": self.convertToFormattedRealWorldTime(completionTime)
            }
          else:
            order_lateness_dict[obj["id"]] = {
              "dueDate": self.convertToFormattedRealWorldTime(dueDate),
              "delay": 1000,
              "completionDate": "Unfinished"
            }

    return data
