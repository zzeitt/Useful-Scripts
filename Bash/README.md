# README
## How to use
### `turn_on_off_monitors.sh`
1. Get monitors' names
```bash
xrandr | grep " connected"| cut -f1 -d ' '
```
2. Run bash scripts
Replace `MNT1` & `MNT2` with outputs from step 1.
```bash
bash turn_on_off_monitors.sh
```

--- 

### Reference
1. https://ubuntuqa.com/article/9536.html
