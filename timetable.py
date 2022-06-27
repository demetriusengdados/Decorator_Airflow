def next_dagrun_info(
    self,
    *,
    last_automated_data_interval: Optional[DataInterval],
    restriction: TimeRestriction,
) -> Optional[DagRunInfo]:
    if last_automated_data_interval is not None:  # There was a previous run on the regular schedule.
        last_start = last_automated_data_interval.start
        delta = timedelta(days=1)
        if last_start.hour == 6: # If previous period started at 6:00, next period will start at 16:30 and end at 6:00 following day
            next_start = last_start.set(hour=16, minute=30).replace(tzinfo=UTC)
            next_end = (last_start+delta).replace(tzinfo=UTC)
        else: # If previous period started at 14:30, next period will start at 6:00 next day and end at 14:30
            next_start = (last_start+delta).set(hour=6, minute=0).replace(tzinfo=UTC)
            next_end = (last_start+delta).replace(tzinfo=UTC)
    else:  # This is the first ever run on the regular schedule. First data interval will always start at 6:00 and end at 16:30
        next_start = restriction.earliest
        if next_start is None:  # No start_date. Don't schedule.
            return None
        if not restriction.catchup: # If the DAG has catchup=False, today is the earliest to consider.
            next_start = max(next_start, DateTime.combine(Date.today(), Time.min).replace(tzinfo=UTC))
        next_start = next_start.set(hour=6, minute=0).replace(tzinfo=UTC)
        next_end = next_start.set(hour=16, minute=30).replace(tzinfo=UTC)
    if restriction.latest is not None and next_start > restriction.latest:
        return None  # Over the DAG's scheduled end; don't schedule.
    return DagRunInfo.interval(start=next_start, end=next_end)