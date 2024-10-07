# STM32CubeIDE

## Instalace IDE
### Jak rozchodit STM32CubeIDE na Linuxu

> [!warning] Chyba při nahraní do desky:
> Could not determine GDB version using command: arm-none-eabi-gdb --version
> arm-none-eabi-gdb: error while loading shared libraries: libncurses.so.5: cannot open shared object file: No such file or directory

Cross-compilery pro ARM jsou v repozitářích, ale GDB je potřeba stáhnout z [https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads).

### Jak odinstalovat CubeIDE
```
sudo apt purge segger-jlink-udev-rules st-stlink-server st-stlink-udev-rules st-stm32cubeide-1.5.0
```

## Práce s IDE
### Jak udělat kopii projektu
- pravým, kopírovat,
- pravým, vložit,
- změnit jméno souboru *.ioc !
- projekt -> clean

### Připojení na tty
```bash
ls /dev/ | grep "tty" | wc -l
ls /dev/ | grep "tty"

ttyACM0
```
Výpis konfigurace:
```bash
stty -a -F /dev/ttyACM0
```

Konfigurace pro matlab:
```bash
ls -la /dev/ | grep "ttyACM*"
crw-rw----+  1 root  dialout   166,     1 říj  1 10:26 ttyACM1

sudo chmod 666 /dev/ttyACM1

ls -la /dev/ | grep "ttyACM*"
crw-rw-rw-+  1 root  dialout   166,     1 říj  1 10:26 ttyACM1
```


#### Zdroje:
- https://wiki.st.com/stm32mpu/wiki/How_to_use_TTY_with_User_Terminal
- BP projek David Salek