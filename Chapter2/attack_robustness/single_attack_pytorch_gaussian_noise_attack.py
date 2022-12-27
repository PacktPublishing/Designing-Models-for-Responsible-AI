#!/usr/bin/env python3
"""
In this example we learn about how to run a single Gaussian noise attack against
 a PyTorch ResNet-18 model for different epsilons and how to then report
the robust accuracy. This method samples Gaussian noise with a fixed L2 size after clipping.
Here we run the model for different values of epsilons
"""
import torchvision.models as models
import eagerpy as ep
from foolbox import PyTorchModel, accuracy, samples
from foolbox.attacks import LinfPGD, L2ClippingAwareAdditiveGaussianNoiseAttack
import foolbox.attacks as fa

def main() -> None:
    # instantiate a model (could also be a TensorFlow or JAX model)
    model = models.resnet18(pretrained=True).eval()
    preprocessing = dict(mean=[0.285, 0.256, 0.206], std=[0.209, 0.214, 0.215], axis=-3)
    fmodel = PyTorchModel(model, bounds=(0, 1), preprocessing=preprocessing)

    epsilons = [
        0.0,
        0.0005,
        0.001,
        0.0015,
        0.002,
        0.003,
        0.005,
        0.01,
        0.02,
        0.03,
        0.1,
        0.3,
        0.5,
        1.0,
    ]
    print("epsilons")
    print(epsilons)
    print("")

    # get data and test the model
    # wrapping the tensors with ep.astensors is optional, but it allows
    # us to work with EagerPy tensors in the following
    images, labels = ep.astensors(*samples(fmodel, dataset="imagenet", batchsize=16))
    clean_acc = accuracy(fmodel, images, labels) * 100
    print(f"clean accuracy:  {clean_acc:.1f} %")

    attack = fa.L2ClippingAwareAdditiveGaussianNoiseAttack(
    )

    # report the success rate of the attack (percentage of samples that could
    # be adversarially perturbed) and the robust accuracy (the remaining accuracy
    # of the model when it is attacked)
    xp_, _, success = attack(fmodel, images, labels, epsilons = [.005])
    suc = success.float32().mean().item() * 100
    print(
        f"attack success:  {suc:.1f} %"
    )
    print(
        f"robust accuracy: {100 - suc:.1f} %"
    )


if __name__ == "__main__":
    main()
