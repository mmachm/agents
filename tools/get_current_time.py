import datetime


def get_current_local_time(time_zone: str) -> str:
    """
    Gets the current time. The 'time_zone' parameter must be provided.
    For basic use, provide "UTC". This example primarily notes the timezone
    if it's not "UTC" and returns server's local time, or returns UTC time.

    Args:
        time_zone (str): The timezone for the time. The LLM must always provide this.
                         Instruct the LLM to use "UTC" if no other zone is specified by the user.
    Returns:
        str: A string representing the current time.
    """
    print(f"\n--- Tool Call: get_current_local_time (time_zone: '{time_zone}') ---")
    try:
        effective_time_zone_str = "UTC"  # Default assumption
        if time_zone and time_zone.strip():  # Ensure time_zone is not None or empty
            effective_time_zone_str = time_zone.strip().upper()

        if effective_time_zone_str != "UTC":
            now_local = datetime.datetime.now()
            return f"The current server local time (requested zone was '{time_zone}') is {now_local.strftime('%Y-%m-%d %H:%M:%S')}."
        else:
            now_utc = datetime.datetime.now(datetime.timezone.utc)
            return (
                f"The current UTC time is {now_utc.strftime('%Y-%m-%d %H:%M:%S %Z')}."
            )
    except Exception as e:
        print(f"[Tool Error - get_current_local_time]: {str(e)}")
        return f"Sorry, I couldn't retrieve the current time: {str(e)}"
