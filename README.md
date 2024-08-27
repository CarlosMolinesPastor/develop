# develop_app
**develop_app** for archlinux. You can use the app for install various tools for developing
From editors to a utilities only with an app utility
It's makes with [flet](https://flet.dev/) flutter with python.

## Install dependencies && Create a environment

```
sudo pacman -S xfce4-terminal mpv gtk3 gstreamer
sudo ln -s /usr/lib/libmpv.so /usr/lib/libmpv.so.1
mkdir develop
cd develop
python3 -m venv .venv
source .venv/bin/activate
pip install flet
```
or instead of installing pip install flet
```
pip install -r requirements.txt
```

## Clone the repository:

```
git clone https://github.com/CarlosMolinesPastor/develop.git
```

## To run the app:

```
flet run develop
```

## To create and packaging the app

```
flet build linux
```

<h2>Status</h2>
<a href="https://github.com/CarlosMolinesPastor/Factia/releases/"><img src="https://img.shields.io/github/tag/CarlosMolinesPastor/Factia?include_prereleases=&sort=semver&color=blue" alt="GitHub tag"></a>
<a href="#license"><img src="https://img.shields.io/badge/License-GPL3-blue" alt="License"></a>

![Badge en Desarollo](https://img.shields.io/badge/STATUS-EN%20DESAROLLO-green)


<h2>License</h2>
Released under <a href="/LICENSE">GPL3</a> by <a href="https://github.com/CarlosMolinesPastor">@CarlosMolinesPastor</a>.
