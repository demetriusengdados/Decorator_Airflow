def infer_manual_data_interval(self, run_after: DateTime) -> DataInterval:
    delta = timedelta(days=1)
    # If time is between 6:00 and 16:30, period ends at 6am and starts at 16:30 previous day
    if run_after >= run_after.set(hour=6, minute=0) and run_after <= run_after.set(hour=16, minute=30):
        start = (run_after-delta).set(hour=16, minute=30, second=0).replace(tzinfo=UTC)
        end = run_after.set(hour=6, minute=0, second=0).replace(tzinfo=UTC)
    # If time is after 16:30 but before midnight, period is between 6:00 and 16:30 the same day
    elif run_after >= run_after.set(hour=16, minute=30) and run_after.hour <= 23:
        start = run_after.set(hour=6, minute=0, second=0).replace(tzinfo=UTC)
        end = run_after.set(hour=16, minute=30, second=0).replace(tzinfo=UTC)
    # If time is after midnight but before 6:00, period is between 6:00 and 16:30 the previous day
    else:
        start = (run_after-delta).set(hour=6, minute=0).replace(tzinfo=UTC)
        end = (run_after-delta).set(hour=16, minute=30).replace(tzinfo=UTC)
    return DataInterval(start=start, end=end)