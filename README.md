<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- [![Logo][logo]][logo-url] -->

# Dungeonasium

This is a reinforcement learning project aimed at testing TTRPG rules and monsters -- such as Open Game License (OGL) D&D5e and beasts such as Rats. The end goal is to properly create deadly monsters for dungeons and learn what behavoirs may lead to thier survival.

## Dataset

Examples of rules and monsters can be found [D&D SRD OGL v5.1](https://media.wizards.com/2016/downloads/DND/SRD-OGL_V5.1.pdf).

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Approach

The approach used for this project is to create various dungeons/[Gymnasium Environments](https://gymnasium.farama.org/api/env/) and trying various methods to train agents/monsters including but not limited to [Q-Learning](https://en.wikipedia.org/wiki/Q-learning), [DQN](https://en.wikipedia.org/wiki/Q-learning#Deep_Q-learning), or other algorithms.

[Adversarial ML](https://en.wikipedia.org/wiki/Adversarial_machine_learning) could also become an interesting method; pitting monster against monster.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Dependencies

![python-shield]

This project is implemented using Python 3.X. 

![tf-shield]
![keras-shield]
![np-shield]
![pd-shield]
![skl-shield]
![sci-shield]

All libraries used are included in the `requirements.txt`. You can execute the following to update your dependencies

```
$ pip install -r requirements.txt
```


Any sequential models are originally created with the Nvidia GeForce GTX 980 GPU and Intel Core i7-5960X CPU. Therefore the complexity of the models is further constrained by allowable training time and gpu memory.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

Usages are still being constructed.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Conclusion

This project demonstrates various investigations in how one can train thier monsters.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Asset Credits

Credit to visual assets not created by contributors of the project will go here.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Acbarakat/CrystalVision.svg?style=for-the-badge
[contributors-url]: https://github.com/Acbarakat/CrystalVision/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Acbarakat/CrystalVision.svg?style=for-the-badge
[forks-url]: https://github.com/Acbarakat/CrystalVision/network/members
[stars-shield]: https://img.shields.io/github/stars/Acbarakat/CrystalVision.svg?style=for-the-badge
[stars-url]: https://github.com/Acbarakat/CrystalVision/stargazers
[issues-shield]: https://img.shields.io/github/issues/Acbarakat/CrystalVision.svg?style=for-the-badge
[issues-url]: https://github.com/Acbarakat/CrystalVision/issues
[license-shield]: https://img.shields.io/github/license/Acbarakat/CrystalVision.svg?style=for-the-badge
[license-url]: https://github.com/Acbarakat/CrystalVision/blob/main/LICENSE.md
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/allonte-barakat/
[python-shield]: https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue
[tf-shield]: https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white
[keras-shield]: https://img.shields.io/badge/Keras-FF0000?style=for-the-badge&logo=keras&logoColor=white
[np-shield]: https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white
[pd-shield]: https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white
[skl-shield]: https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white
[sci-shield]: https://img.shields.io/badge/SciPy-654FF0?style=for-the-badge&logo=SciPy&logoColor=white
[logo]: https://repository-images.githubusercontent.com/616501925/3051c914-b18a-42ab-96e1-96d6fb7e2b81
[logo-url]: https://github.com/Acbarakat/Dungeonasium
