# AutoPoke

> Recently my friends have reported several bugs in `Jpn` versions. I'll fix them as soon as possible when I'm free, maybe in March, 2025.

> **The emulator bar causes problems because its color value is similar to the text color in Pokémon games. Therefore, it's better to avoid having the emulator bar visible when using AutoPoke, especially during the FISHING function and auto repel. (One approach is to use the PIP mode, i.e., Picture-in-Picture.)**

Auto hunting shiny pokemon using Playback(Epilogue GB operator), writing with Python. Only for Gen3.
宝可梦三代自动化刷闪工具，使用Playback(Epilogue GB operator)。模拟器等也可参考使用。

# How to use?

- **Make sure *TEXT SPEED* in the setting of your game is *Fast*.**
- **In `Emerald` version, make sure *BATTLE SCENE* in the setting of your game is *OFF***
- **Do not minimize the window of Operator when AutoPoke is running.**
- **Do not change the window size of Operator *tooooo* large or *tooooo* small. The default size is recommended.**
- Make player role where you need to encounter PM, and set parameters in `config.ini` file (Optional). Then run `AutoPoke.py` or `AutoPoke.exe`.
- Support sweet scent.
  - You should make sure the pointer of the menu is at **Pokemon**.
  - The last of your pokemon should have learnt sweet scent.
  - Sweet scent should be the first out-battle skill of your last pokemon.

> If your Operator version is lower than `v1.0.0`, download AutoPoke of `v1.1` version.

## Update the config of AutoPoke

> In the latest version, this section is not necessary.

After your first launch, a `config.ini` file will be created in the same directory of AutoPoke. Since I found that the color of Playback differs from PCs, you should update the `Color` config in `config.ini` file, where it looks like this:

![color config example](guide/color_config.png)

Follow the images below to config the color. Attention, here we use RGB value for colors. You can take screenshot and upload to those websites(search them in google) which can give you the RGB you picked.

![bgcolor](guide/bgcolor.png)
![dialogcolor](guide/dialogcolor.png)
![txtcolor](guide/txtcolor.png)

Here, *dialogcolor* you can only change the first RGB value and leave the second one there. In fact, *bgdeepblue* is similar to *bgdeepgreen* while it's of `FrLg`.

# Already confirmed be of use in

- English version:

|  Confirmed   | RS | E | FrLg |
| :----: | :----: |:----: |:----: |
| Wild Encounter | **Yes** | **Yes** | **Yes** |
| Safari Zone | **Yes** | **Yes** | **Yes** |
| Simple Stationary | **Yes** | **Yes** | **Yes** |
| Fishing | **Yes** | **Yes** | **Yes** |
| Starters | **Yes** | **Yes** | **Yes** |
| Gifted PM | Not Complete | Not Complete | **Yes** |

- Japanese version:

|  Confirmed   | RS | E | FrLg |
| :----: | :----: |:----: |:----: |
| Wild Encounter | **Yes** | **Yes** | **Yes** |
| Safari Zone | **Yes** | **Yes** | **Yes** |
| Simple Stationary | **Yes** | **Yes** | **Yes** |
| Fishing | **Yes** | **Yes** | **Yes** |
| Starters | **Yes** | **Yes** | **Yes** |
| Gifted PM | Not Complete | Not Complete | **Yes** |

- Other versions:<br>Not Test
