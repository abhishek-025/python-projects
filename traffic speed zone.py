class SpeedData:
    def _init_(self):
        self.speed_entries = {}

    def create_speed_entry(self, zone, vehicle_id, speed):
        if zone not in self.speed_entries:
            self.speed_entries[zone] = {}
        self.speed_entries[zone][vehicle_id] = speed

    def read_speed_entries(self, zone):
        return self.speed_entries.get(zone, {})

    def update_speed_entry(self, zone, vehicle_id, new_speed):
        if zone in self.speed_entries and vehicle_id in self.speed_entries[zone]:
            self.speed_entries[zone][vehicle_id] = new_speed
            return True
        return False

    def delete_speed_entry(self, zone, vehicle_id):
        if zone in self.speed_entries and vehicle_id in self.speed_entries[zone]:
            del self.speed_entries[zone][vehicle_id]
            return True
        return False


class SpeedMonitorSystem:
    def _init_(self):
        self.speed_data = SpeedData()

    def monitor_vehicle_speeds(self, zone, vehicle_id, speed):
        self.speed_data.create_speed_entry(zone, vehicle_id, speed)

    def issue_speeding_tickets(self, zone, legal_speed_limit):
        tickets = {}
        entries = self.speed_data.read_speed_entries(zone)
        for vehicle_id, speed in entries.items():
            if speed > legal_speed_limit:
                tickets[f"{zone}-{vehicle_id}"] = speed
        return tickets


# Unit Testing
import unittest

class TestSpeedMonitoringSystem(unittest.TestCase):
    def setUp(self):
        self.system = SpeedMonitorSystem()
        self.system.monitor_vehicle_speeds("zone1", "001", 55)
        self.system.monitor_vehicle_speeds("zone1", "002", 60)

    def test_monitor_vehicle_speeds(self):
        self.assertEqual(len(self.system.speed_data.read_speed_entries("zone1")), 2)

    def test_issue_speeding_tickets(self):
        tickets = self.system.issue_speeding_tickets("zone1", 50)
        self.assertEqual(len(tickets), 2)
        self.assertTrue("zone1-001" in tickets)
        self.assertTrue("zone1-002" in tickets)

    def test_speed_update_and_delete(self):
        updated = self.system.speed_data.update_speed_entry("zone1", "001", 45)
        self.assertTrue(updated)
        self.system.speed_data.delete_speed_entry("zone1", "001")
        self.assertEqual(len(self.system.speed_data.read_speed_entries("zone1")), 1)

if _name_ == '_main_':
    unittest.main()
