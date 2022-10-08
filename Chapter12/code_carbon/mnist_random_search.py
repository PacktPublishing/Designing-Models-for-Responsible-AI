import kerastuner
import tensorflow as tf

from codecarbon import EmissionsTracker
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold,RandomizedSearchCV


from codecarbon import track_emissions


@track_emissions(
    # api_endpoint="http://your api if you want",
    # experiment_id="3a202149-8be2-408c-a3d8-baeae2de2987",
    # api_key=" not used yet",
    save_to_api=True,
)

class RandomSearchTuner(kerastuner.tuners.RandomSearch):
    def run_trial(self, trial, *args, **kwargs):
        # You can add additional HyperParameters for preprocessing and custom training loops
        # via overriding `run_trial`
        kwargs["batch_size"] = trial.hyperparameters.Int("batch_size", 32, 256, step=32)

        super(RandomSearchTuner, self).run_trial(trial, *args, **kwargs)


def build_model():
    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(10),
        ]
    )
    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    model.compile(optimizer="adam", loss=loss_fn, metrics=["accuracy"])
    return model


def main():
    mnist = tf.keras.datasets.mnist

    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0

    model = KerasClassifier(build_fn=build_model, epochs=1)
    param_grid = dict(batch_size=list(range(32, 256 + 32, 32)))
    r_search = RandomizedSearchCV(estimator=model, param_distributions=param_grid,
    n_iter = 3,
    cv = 3,
    n_jobs = -1,
    verbose = 1 )

    tracker = EmissionsTracker(project_name="mnist_random_search")
    tracker.start()
    rsearch_result = r_search.fit(x_train, y_train)
    emissions = tracker.stop()

    print(f"Best Accuracy : {rsearch_result.best_score_} using {rsearch_result.best_params_}")
    print(f"Emissions : {emissions} kg CO₂")


if __name__ == "__main__":
    main()
