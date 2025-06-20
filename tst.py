from codecarbon import OfflineEmissionsTracker
tracker = OfflineEmissionsTracker(country_iso_code="CAN")
tracker.start()
print("hello")
tracker.stop()
