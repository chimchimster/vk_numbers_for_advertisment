class StatisticsManager:
    def __init__(self):
        self.statistics = {}

    def update_statistics(self, **kwargs):
        group_name, items = kwargs.popitem()

        if group_name not in self.statistics:
            self.statistics[group_name] = items
        else:
            self.statistics[group_name] += items

    def get_statistics(self):
        stats = ''
        for group_name, items in self.statistics.items():
            stats += f'VK_PHONES: {items} of {group_name} has been send to database.\n'

        return stats