import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers import Dense
from keras import regularizers


fights = pd.read_csv(r"C:\Users\Stephen\Downloads\ufc_bouts.csv", index_col=0)  # reading in csv file of all fights
fighters = pd.read_csv(r"C:\Users\Stephen\Downloads\ufc_fighters.csv")  # reading in csv file of all fighters

fighters.iloc[485, 1] = "Michael McDonald WW" # changing names of fighters with same name so can differentiate between them
fighters.iloc[800, 1] = "Dong Hyun Kim LW"
fighters.iloc[903, 1] = "Tony Johnson MW"

fighters.drop("fighter_id", axis=1,
              inplace=True)  # dropping fighter_id column from table and using the name column to identify fighters
fighters.set_index("name", inplace=True)

new_fighters = fighters.loc[~((fighters["SLpM"] == 0) &  #
                              (fighters["Str_Acc"] == "0%") &
                              (fighters["SApM"] == 0) &
                              (fighters["Str_Def"] == "0%") &
                              (fighters["TD_Avg"] == 0) &
                              (fighters["TD_Acc"] == "0%") &
                              (fighters["TD_Def"] == "0%") &
                              (fighters["Sub_Avg"] == 0))].copy() #drop fighters with no stats available



percentages = ["Str_Acc", "Str_Def", "TD_Acc", "TD_Def"] #all data with % after it
predictors = ["SLpM", "Str_Acc", "SApM", "Str_Def", "TD_Avg", "TD_Acc", "TD_Def", "Sub_Avg"]#all features used to predict

new_fighters = new_fighters[predictors]#remove all columns from fighters dataframe other than 8 predictors

new_fighters.loc[:, percentages] = new_fighters.loc[:, percentages].applymap(
    lambda x: x.replace("%", ""))#remove the % symbol from the end of the percentage values

new_fighters.loc[:, predictors] = new_fighters.loc[:, predictors].astype(np.float32) #change the percentages to floats so they can be subtracted from one another

new_fights = fights.loc[fights["result"] == "win"].copy()#remove all fights that end in a draw/no contest
new_fights = new_fights.loc[:, ["fighter1", "fighter2", "winner", "weight_class"]]#removes columns not needed
new_fights.reset_index(drop=True, inplace=True)

randomise_fights = np.random.choice(len(new_fights), size=int(len(new_fights) / 2), replace=False)#randomise fighters order as fighter 1 is always winner at the moment
new_fights.iloc[randomise_fights, [0, 1]] = new_fights.iloc[randomise_fights, [1, 0]].values

new_fights["result"] = (new_fights["winner"] == new_fights["fighter1"]).astype("int")
new_fights.drop(['winner'], axis=1, inplace=True)
new_fights.drop(['weight_class'], axis=1, inplace=True)

fighter_names = new_fighters.index.values.tolist()

new_fights = new_fights.loc[(new_fights["fighter1"].isin(fighter_names)) &
                            (new_fights["fighter2"].isin(fighter_names))].copy()

# use fighter 1 - fighter 2 (the differences) for learning
for col in predictors:
    new_fights[col] = new_fights.apply(
        lambda row: new_fighters.loc[row["fighter1"], col] - new_fighters.loc[row["fighter2"], col], axis=1)

# drop fighter1 and fighter2 columns
new_fights.drop(["fighter1", "fighter2"], axis=1, inplace=True)

X = new_fights.iloc[:, 1:]
y = new_fights.iloc[:, 0]

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75, test_size=0.25, random_state=101)

model = Sequential([Dense(32, input_dim=X_train.shape[1], activation='relu', kernel_regularizer=regularizers.l2(0.01)),
                    Dense(32, activation='relu', kernel_regularizer=regularizers.l2(0.01), ),
                    Dense(32, activation='relu', kernel_regularizer=regularizers.l2(0.01)),
                    Dense(32, activation='relu', kernel_regularizer=regularizers.l2(0.01)),
                    Dense(1, activation='sigmoid'), ])
model.compile(loss='binary_crossentropy', optimizer='Adam', metrics=['accuracy'])

model.summary() #visual representation of layers of model
