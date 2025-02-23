from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import time

# Initialize Google Trends
py_trends = TrendReq(hl='en-US', tz=360)

# Define keywords
keywords = ["donut shop", "vintage store"]  # Shorter queries work better

# Build payload (state-level, city-level may not always work)
py_trends.build_payload(keywords, cat=0, timeframe='today 12-m', geo='US-GA', gprop='')

# Get interest over time
interest_over_time_df = py_trends.interest_over_time()
print("Interest Over Time:")
print(interest_over_time_df)

# Check if data exists before plotting
if not interest_over_time_df.empty:
    interest_over_time_df.drop(columns=['isPartial'], errors='ignore').plot(figsize=(10, 5))
    plt.title('Interest Over Time')
    plt.xlabel('Date')
    plt.ylabel('Interest')
    plt.show()
else:
    print("No data available for the selected keywords and region.")

# Get interest by region
interest_by_region_df = py_trends.interest_by_region()
print("Interest By Region:")
print(interest_by_region_df.head())

# Get related queries
related_queries = py_trends.related_queries()
print("Related Queries:")
print(related_queries)
