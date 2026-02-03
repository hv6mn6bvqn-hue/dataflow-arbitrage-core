import datetime

# Example of publicly reported values
source_a_value = 92.31
source_b_value = 92.27

timestamp_a = datetime.datetime.utcnow()
timestamp_b = timestamp_a - datetime.timedelta(seconds=45)

difference = round(abs(source_a_value - source_b_value), 4)

print("DataFlow Arbitrage — Signal Example")
print(f"Source A value: {source_a_value} at {timestamp_a}")
print(f"Source B value: {source_b_value} at {timestamp_b}")
print(f"Observed divergence: {difference}")
