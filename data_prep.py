import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

mental_health = pd.read_csv("dataset_mood_smartphone.csv")
pd.set_option("display.float_format", lambda x: "%.2f" % x)
print(mental_health)
# print("\n--Info--")
# print(mental_health.info())
# print("\n--Describe--")
# print(mental_health.describe())
# print("\n--IsNull--")
# print(mental_health.isnull().sum())
# print("\n--Unique--")
# print(mental_health.nunique())
# print("\n--Correlation--")
# print(mental_health.corr(numeric_only=True))

df_byVar = mental_health.groupby("variable")["value"].describe()
fig, ax = plt.subplots(figsize=(30, 6))
ax.plot(df_byVar)
ax.set_title("Value by Variable")
fig.savefig("graph.png")

print("\n --Unique--")
print(mental_health.groupby("id").nunique())

df_pooledMood = mental_health[mental_health["variable"] == "mood"]
fig, ax = plt.subplots()
ax.hist(df_pooledMood["value"].values)
ax.set_title("Pooled Mood scores across users")
ax.set_xlabel("Mood Score")
ax.set_ylabel("Frequency")
fig.savefig("pooled_mood_scores.png")

df_moodPerUser = mental_health[mental_health["variable"] == "mood"].groupby("id")[
    "value"
]
fig, ax = plt.subplots(figsize=(20, 6))
ax.boxplot([group.values for _, group in df_moodPerUser])
ax.set_title("Boxplot Mood Per User")
ax.set_xlabel("User")
ax.set_ylabel("Mood Score")
fig.savefig("mood_per_user_boxplot.png")


mental_health["timestamp"] = pd.to_datetime(
    mental_health["time"]
)  # check your actual column name
mental_health["date"] = mental_health["timestamp"].dt.date

# Different aggregation per variable type
mean_vars = ["mood", "circumplex.arousal", "circumplex.valence", "activity"]
sum_vars = [
    c
    for c in mental_health["variable"].unique()
    if c.startswith("appCat") or c in ["screen", "call", "sms"]
    ]

mental_health["timestamp"] = pd.to_datetime(mental_health["time"])  # adjust column name
mental_health["date"] = mental_health["timestamp"].dt.date
# moods per user per day
mood_only = mental_health[mental_health["variable"] == "mood"]
print(mood_only.groupby(["id", "date"]).size().describe())
# total span per user
print("\n date span per user")
print(mental_health.groupby("id")["date"].agg(["min", "max", "nunique"]))

# Different aggregation per variable type
mean_vars = ['mood', 'circumplex.arousal', 'circumplex.valence', 'activity']
sum_vars  = [c for c in mental_health['variable'].unique() 
             if c.startswith('appCat') or c in ['screen', 'call', 'sms']]

daily_mean = (mental_health[mental_health['variable'].isin(mean_vars)]
              .groupby(['id', 'date', 'variable'])['value'].mean().unstack())
daily_sum  = (mental_health[mental_health['variable'].isin(sum_vars)]
              .groupby(['id', 'date', 'variable'])['value'].sum().unstack())
daily = daily_mean.join(daily_sum).reset_index()

print(daily_mean)
print(daily_sum)

