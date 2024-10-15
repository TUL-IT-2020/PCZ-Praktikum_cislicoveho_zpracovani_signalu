# PCZ - Praktikum číslicového zpracování signálu

## Zápočet: 
- 5. samostatných úloh
- semestrální práce

## Zkouška
Konec před vánocema.
- test na elerningu, na hodinu.
Vlastnoruční tahák povolen.

## Literatura
- CHASSAING, Rulph a Donald REAY. Digital signal processing: and applications with the TMS320C6713 and TMS320C6416 DSK. 2nd ed. 
- Hoboken: John Wiley & Sons, 2008, 576 s. ISBN 978-0-470-13866-3. SMÉKAL, Zdeněk a Petr SYSEL. Signálové procesory. 1. vyd. Praha: Sdělovací Technika, 2006, 283 s. ISBN 80-86645-08-8. 
- REAY, Donald. Digital signal processing and applications with the OMAP L138 eXperimenter. Hoboken, N.J.: Wiley, c2012, xvii, 340 p. ISBN 9780470936863. 
- LYONS, G. Understanding digital signal processing. Vyd. 2. New Jersey: Prentice-Hall, 2004, 665 s. ISBN 0-13-108989-7. 
- LYONS, Richard G a D FUGAL. The essential guide to digital signal processing. Xii, 2014, 188 pages. ISBN 0133804429. 
- LANGBRIDGE, By James A. Professional embedded arm development. Indianapolis, Ind: Wiley, 2013. ISBN 9781118788943. Hayes M.H. 
- Schaum's Outline of Theory and Problems of Digital Signal Processing. ISBN 0–07–027389–8

## Poznámky
Matlab all the way!

Jakou máme desku:
STM32 projekt -> board selector -> nucleo-L4R5ZI


- [x] Přinést krabičku na Nucleo desku.
- [x] Rozchodit STM32CubeIDE na Linuxu.
- [ ] Rozchodit TTY

![[STM32CubeIDE]]

## Cvičení

```
/* USER CODE BEGIN Includes */  
#include "TimeStamp.h"  
/* USER CODE END Includes */  
  
/* USER CODE BEGIN PV */  
#define BLOCK_SIZE_MAX 4800  
float sample_L[BLOCK_SIZE_MAX];  
float sample_R[BLOCK_SIZE_MAX];  
float sample_L1[BLOCK_SIZE_MAX];  
float sample_R1[BLOCK_SIZE_MAX];  
float sample_L2[BLOCK_SIZE_MAX];  
float sample_R2[BLOCK_SIZE_MAX];  
/* USER CODE END PV */  
  
/* USER CODE BEGIN 0 */  
void XferCpltCallback(DMA_HandleTypeDef *hdma)  
{  
    //__NOP(); //Line reached only if transfer was successful. Toggle a breakpoint here  
    TimeStamp_SET_F(); TimeStamp_SET_F();  
}  
/* USER CODE END 0 */  
  
/* USER CODE BEGIN 2 */  
TimeStamp_INIT(&htim5); //HAL_TIM_Base_Start_IT(&htim5);// for time measure GetTime()  
  
// vlastni pokus    
//DMA mem copy experiment  
for(i=0; i<BLOCK_SIZE_MAX; i++)  
    sample_L1[i]= i*i/159;  
TimeStamp_SET_A();  
for(i=0; i<BLOCK_SIZE_MAX; i++)  
    sample_L2[i]= sample_L1[i];  
TimeStamp_SET_B();// 182570 ticks  
HAL_DMA_RegisterCallback(&hdma_memtomem_dma2_channel1, HAL_DMA_XFER_CPLT_CB_ID, &XferCpltCallback);  
TimeStamp_SET_C();// 29932 ticks  
HAL_DMA_Start_IT(&hdma_memtomem_dma2_channel1, (uint32_t) sample_L1, (uint32_t) sample_R2, BLOCK_SIZE_MAX);  
TimeStamp_SET_D();// 440  
/* USER CODE END 2 */
```

## DU

### Měření času
Změřit jak dlouho jsme zmáčkli modré tlačítko a odeslat do matlabu.
- Zobrazit v aplikaci.
Poznámky na externím disku.
- konfigurace DMA pro přenos po sériové lince.
	- 4xByte

## 4. týden: PMOD I2S2, konfigurace rozhraní SAI

Zvýrazněno

1) seznámení s modulem Pmod I2S2

- parametry
- schema zapojení a funkce
- komunikační rozhraní (režim "slave")

2) připojení modulu Pmod k desce Nucleo

- volba konektorů a možnosti patice
- napájení

3) nastavení rozhraní SAI

- konfigurace SAIA, SAIB
- nastavení DMA
- konfigurace časování
- struktura dat: 24bitů na 32bitech signed int (drobný problém)
    - dvojkový doplněk
    - vysvětlit:
```C
if(0x00800000 & buf_SAI_RX[i2])

tmp_sample = (0xFF000000 | buf_SAI_RX[i2]);

else tmp_sample = (0x00FFFFFF & buf_SAI_RX[i2]);
```

4) konfigurace audio smyčky PC - ARM - PC

- Axagon USB HQ audio mini adapter - vlastnosti ([axagon/ada-17](https://www.axagon.eu/produkty/ada-17))
- vzorkovací frekvence max 48kHz
- volba zesílení pro input/output
- program v Matlabu

1. Nejdřív udělat zpětnou vazbu na zvukovce. 
2. Odladit přehrávání a záznam zvuku.
> [!note] Linux
> Pod Linuxem je potřeba nastavit správně vstupy a výstupy. Pomohlo nemít nastavený mikrofon, ale reproduktory na USB kartu. 