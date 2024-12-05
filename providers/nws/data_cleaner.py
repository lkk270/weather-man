def clean_weather_data(raw_data):
    cleaned_data = []
    for record in raw_data:
        if "temperature" in record and "humidity" in record and "timestamp" in record:
            cleaned_data.append({
                "location": record.get("location", "Unknown"),
                "temperature": float(record["temperature"]),
                "humidity": float(record["humidity"]),
                "timestamp": record["timestamp"]
            })
    return cleaned_data