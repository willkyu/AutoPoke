# AutoPoke
Auto hunting shiny pokemon using Epilogue GB operator, writing with Python. Only for Gen3.  
宝可梦三代自动化刷闪工具，使用Epilogue GB operator。模拟器等也可参考使用。

# How to use?
- **Make sure Text speed in the setting of your game is *Fast*.**
- **Do not change the window size of Operator.**
- **Do not minimize the window of Operator when AutoPoke is running.**
- Make player role where you need to encounter PM, and set parameters in `config.ini` file. Then run `AutoPoke.py` or `AutoPoke.exe`.
- If your Operator version is lower than `v1.0.0`, download AutoPoke of `v1.1` version.

# Already confirmed be of use in
- English version: `RS`
  - safari zone
  - wild encounter
  - stationary
- English version: `FrLg`
  - wild encounter

# Update Log
- 2023-08-05
  - Fixed bug for special anime when wildpoke raising.
  - Fixed when wildpoke, receiving pokenav will interrupt autopoke.
  - Fixed bug when in cave. InCave parameter is no longer needed.

- 2023-08-04
  - Update for Operator version later than `v1.0.0`.
  - Support extra anime detection for `FrLg`, which only support `RS` in lower version.

- 2023-07-20
  - Stationary function is available now.
  - Optimized codes structure and make all configs in one file.
  - Make the `.exe` file for those can not use python.
  
- 2023-07-08: 
  - Much faster when in safari zone.
  - Auto record encounter counts in `parser.ini`.
  - Support edit keymapping in `parser.ini`.
