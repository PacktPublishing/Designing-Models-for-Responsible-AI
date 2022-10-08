import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, ensemble
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import GridSearchCV

# Datasets
# save models with either joblib or pickle
import joblib
from verta import Client
from verta.dataset import Path

client = Client("http://localhost:3000")
# set up model versioning
proj = client.set_project("Model Classification")
expt = client.set_experiment("ModelDB Experiment")
# log the first run
run = client.set_experiment_run("First Run")
dataset = client.set_dataset(name = "Diabetes Data")
save_path = '/Users/shachatt1/Desktop/sharmi/books/My_book_responsible_ai/python_code/Chapter 7/modeldb_model_artifacts/'
dataset_version = dataset.create_version(Path(save_path))
run.log_dataset_version("v1", dataset_version)


diabetes = datasets.load_diabetes()
X, y = diabetes.data, diabetes.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.1, random_state=13
)

params = {
    "n_estimators": [400, 500],
    "max_depth": [4,5],
    "min_samples_split": [2, 5],
    "learning_rate": [0.02, 0.01],
    "loss": ["squared_error","absolute_error"],
}


reg_model = ensemble.GradientBoostingRegressor()

cv = RepeatedStratifiedKFold(n_splits=2, n_repeats=3, random_state=1)
grid_search = GridSearchCV(estimator=reg_model, param_grid=params, n_jobs=-1, cv=cv, scoring='r2',error_score=0)
grid_result = grid_search.fit(X, y)
# summarize results
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
run.log_metric("r2", grid_result.best_score_)

means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
i = 0

for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))
    run.log_observation("mean", mean)
    run.log_observation("stdev", stdev)
    param_dict = dict(param)
    param_dict['iter'] = str(i)
    i = i +1
    run.log_observation("lr", param_dict['learning_rate'])
    run.log_observation("loss", param_dict['loss'])
    run.log_observation("maxdepth", param_dict['max_depth'])
    run.log_observation("minsamplesplit", param_dict['min_samples_split'])
    run.log_observation("nestimator", param_dict['n_estimators'])
    run.log_observation("iter", param_dict['iter'])

grid_result.fit(X_train, y_train)

y_pred = grid_result.predict(X_test)
train_score = grid_result.score(X_train, y_train)
test_score = grid_result.score(X_test, y_test)
run.log_metric("Accuracy_train", train_score)
run.log_metric("Accuracy_test", test_score)


mse = mean_squared_error(y_test, grid_result.predict(X_test))
print("The mean squared error (MSE) on test set: {:.4f}".format(mse))

run.log_metric("mse", mse)
run.log_hyperparameters(grid_result.best_params_)

filename_2 = "simple_model_gbr_2.joblib"
joblib.dump(grid_result, filename_2)
run.log_model(save_path, filename_2)

test_score = np.zeros((grid_result.best_params_["n_estimators"],), dtype=np.float64)
best_model = grid_result.best_estimator_
print("test score shape", test_score.shape)
for i, y_pred in enumerate(best_model.staged_predict(X_test)):
    test_score[i] = best_model.loss_(y_test, y_pred)
    run.log_observation("testscore", test_score[i])


fig = plt.figure(figsize=(6, 6))
plt.subplot(1, 1, 1)
plt.title("Deviance")
plt.plot(
    np.arange(grid_result.best_params_["n_estimators"]) + 1,
    best_model.train_score_,
    "b-",
    label="Training Set Deviance",
)
plt.plot(
    np.arange(grid_result.best_params_["n_estimators"]) + 1, test_score, "r-", label="Test Set Deviance"
)
plt.legend(loc="upper right")
plt.xlabel("Boosting Iterations")
plt.ylabel("Deviance")
fig.tight_layout()
plt.savefig(save_path + 'perf_gbr.png')
run.log_artifact("perf_gbr", save_path + 'perf_gbr.png')


feature_importance = best_model.feature_importances_
sorted_idx = np.argsort(feature_importance)
pos = np.arange(sorted_idx.shape[0]) + 0.5
fig = plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.barh(pos, feature_importance[sorted_idx], align="center")
plt.yticks(pos, np.array(diabetes.feature_names)[sorted_idx])
plt.title("Feature Importance (MDI)")

result = permutation_importance(
    grid_result, X_test, y_test, n_repeats=10, random_state=42, n_jobs=2
)
sorted_idx = result.importances_mean.argsort()
plt.subplot(1, 2, 2)
plt.boxplot(
    result.importances[sorted_idx].T,
    vert=False,
    labels=np.array(diabetes.feature_names)[sorted_idx],
)
plt.title("Permutation Importance (test set)")
fig.tight_layout()
#plt.show()
plt.savefig(save_path + 'feature_imp.png')
#run.log_artifact()
run.log_artifact("feature_imp", save_path + 'feature_imp.png')