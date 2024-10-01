import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# -------- import csv
dayHour_df= pd.read_csv("dayHour_data.csv")


# -------- helper func
# hours change
def both_hoursRenting_df(df):
    rentPerHour= df.groupby("hr")["cnt_hr"].mean().reset_index()

    return rentPerHour

# working day weekend/holiday
def casual_workingdayRenter_df(df):
    casualRenter= df.groupby("workingday_day")["casual_day"].mean().reset_index().sort_values("casual_day")

    return casualRenter

def registered_workingdayRenter_df(df):
    registeredRenter= df.groupby("workingday_day")["registered_day"].mean().reset_index().sort_values("registered_day")

    return registeredRenter

# seasons
def casual_seasonRenter_df(df):
    casualSeason= df.groupby("season_day")["casual_day"].mean().reset_index().sort_values("casual_day")

    return casualSeason

def registered_seasonRenter_df(df):
    registeredSeason= df.groupby("season_day")["registered_day"].mean().reset_index().sort_values("registered_day")

    return registeredSeason

# weatherssssssss
def casual_weatherRenter_df(df):
    casualWeather= df.groupby("weathersit_day")["casual_day"].mean().reset_index().sort_values("casual_day")

    return casualWeather

def registered_weatherRenter_df(df):
    registeredWeather= df.groupby("weathersit_day")["registered_day"].mean().reset_index().sort_values("registered_day")

    return registeredWeather

# ------------- filter
datetime_columns = ["dteday"]
dayHour_df.sort_values(by="dteday")
dayHour_df.reset_index(inplace=True)

for column in datetime_columns:
    dayHour_df[column] = pd.to_datetime(dayHour_df[column])


min_date= dayHour_df["dteday"].min()
max_date= dayHour_df["dteday"].max()

with st.sidebar:
    # no image, copyright issue
    start_date, end_date = st.date_input(
        label='Time Range',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

time_df= dayHour_df[(dayHour_df["dteday"] >= str(start_date)) & (dayHour_df["dteday"] <= str(end_date))]


# ------------ make for figures within df time range
rentPerHour= both_hoursRenting_df(time_df)
casualRenter = casual_workingdayRenter_df(time_df)
registeredRenter = registered_workingdayRenter_df(time_df)
casualSeason= casual_seasonRenter_df(time_df)
registeredSeason= registered_seasonRenter_df(time_df)
casualWeather= casual_weatherRenter_df(time_df)
registeredWeather= registered_weatherRenter_df(time_df)


# ------------ plot
# hours
st.subheader("Bike Renting per Hour")

fig, ax = plt.subplots(figsize=(16, 8))
line, = ax.plot(
    rentPerHour["hr"],
    rentPerHour["cnt_hr"],
    marker='o', 
    linewidth=2,
    color="#51addb"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_ylabel("Average Daily bike renting", fontsize= 25)

st.pyplot(fig)


# workday sahgkdwja
st.subheader("Bike Renting between Casual Users and Registered Users during Workday and Weekend/Holiday")
st.text("") #blank space

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.barplot(x="workingday_day", y="casual_day", data=casualRenter, palette=["#edbc6d", "#D3D3D3"], ax=ax[0], hue= "workingday_day", legend= False)
ax[0].set_xlabel(None)
ax[0].set_ylabel("Average casual users", fontsize= 35)
ax[0].set_title("Bike Renting in Working Day and Weekend/Holiday\n for Casual Users", loc="center", fontsize=40)
ax[0].tick_params(axis='y', labelsize=25)
ax[0].set_xticks([0, 1])
ax[0].set_xticklabels(["Weekday/Holiday", "Working Day"], fontsize=30);
ax[0].yaxis.grid(True, linestyle='--', linewidth=1)

sns.barplot(x="workingday_day", y="registered_day", data=registeredRenter, palette=["#D3D3D3", "#edbc6d"], ax=ax[1], hue= "workingday_day", legend= False)
ax[1].set_xlabel(None)
ax[1].set_ylabel("Average registered users", fontsize= 35)
ax[1].set_title("Bike Renting in Working Day and Weekend/Holiday\n for Registered Users", loc="center", fontsize=40)
ax[1].tick_params(axis='y', labelsize=25)
ax[1].set_xticks([0, 1])
ax[1].set_xticklabels(["Weekday/Holiday", "Working Day"], fontsize=30);
ax[1].yaxis.grid(True, linestyle='--', linewidth=1)

st.pyplot(fig)


# seasons
st.subheader("Bike Renting between Casual Users and Registered Users during Each Season")
st.text("") #blank space

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.barplot(x="season_day", y="casual_day", data=casualSeason, palette=["#D3D3D3", "#D3D3D3", "#edbc6d", "#D3D3D3"], ax=ax[0], hue= "season_day", legend= False)
ax[0].set_xlabel("Season", fontsize= 25)
ax[0].set_ylabel("Average casual users", fontsize= 35)
ax[0].set_title("Bike Renting in Every Season\n for Casual Users", loc="center", fontsize=40)
ax[0].tick_params(axis='y', labelsize=25)
ax[0].set_xticks([0, 1, 2, 3])
ax[0].set_xticklabels(["Spring", "Summer", "Fall", "Winter"], fontsize=30);
ax[0].yaxis.grid(True, linestyle='--', linewidth=1)

sns.barplot(x="season_day", y="registered_day", data=registeredSeason, palette=["#D3D3D3", "#D3D3D3", "#edbc6d", "#D3D3D3"], ax=ax[1], hue= "season_day", legend= False)
ax[1].set_xlabel("Season", fontsize= 25)
ax[1].set_ylabel("Average registered users", fontsize= 35)
ax[1].set_title("Bike Renting in Every Season\n for Registered Users", loc="center", fontsize=40)
ax[1].tick_params(axis='y', labelsize=25)
ax[1].set_xticks([0, 1, 2, 3])
ax[1].set_xticklabels(["Spring", "Summer", "Fall", "Winter"], fontsize=30);
ax[1].yaxis.grid(True, linestyle='--', linewidth=1)

st.pyplot(fig)


# weather
st.subheader("Bike Renting between Casual Users and Registered Users during Certain Weather Conditions")
st.text("") #blank space

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.barplot(x="weathersit_day", y="casual_day", data=casualWeather, palette=["#edbc6d", "#D3D3D3", "#D3D3D3"], ax=ax[0], hue= "weathersit_day", legend= False)
ax[0].set_xlabel("Waether", fontsize= 25)
ax[0].set_ylabel("Average casual users", fontsize= 35)
ax[0].set_title("Bike Renting in Based on Weather Condition\n for Casual Users", loc="center", fontsize=40)
ax[0].tick_params(axis='y', labelsize=25)
ax[0].set_xticks([0, 1, 2])
ax[0].set_xticklabels(["Clear", "Cloudy", "Light Rain"], fontsize=30);
ax[0].yaxis.grid(True, linestyle='--', linewidth=1)

sns.barplot(x="weathersit_day", y="registered_day", data=registeredWeather, palette=["#edbc6d", "#D3D3D3", "#D3D3D3"], ax=ax[1], hue= "weathersit_day", legend= False)
ax[1].set_xlabel("Waether", fontsize= 25)
ax[1].set_ylabel("Average registered users", fontsize= 35)
ax[1].set_title("Bike Renting in Based on Weather Condition\n for Registered Users", loc="center", fontsize=40)
ax[1].tick_params(axis='y', labelsize=25)
ax[1].set_xticks([0, 1, 2])
ax[1].set_xticklabels(["Clear", "Cloudy", "Light Rain"], fontsize=30);
ax[1].yaxis.grid(True, linestyle='--', linewidth=1)

st.pyplot(fig)
