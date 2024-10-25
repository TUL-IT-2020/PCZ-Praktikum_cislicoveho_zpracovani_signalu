# Cvičení a úkoly

## Měření času
Změřit jak dlouho jsme zmáčkli modré tlačítko a odeslat do matlabu.
- Zobrazit v aplikaci.
Poznámky na externím disku.
- konfigurace DMA pro přenos po sériové lince.
	- 4xByte

## 4. týden
PMOD I2S2, konfigurace rozhraní SAI

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

### Znaménkové rozšíření z 24bit na 32bit
```C
int32_t sign_extend_24_to_32bit(int32_t value) {
    int32_t sign_extended_value = 0;
    if(0x00800000 & value) {
        sign_extended_value = (0xFF000000 | value);
    } else  {
        sign_extended_value = (0x00FFFFFF & value);
    }
    return sign_extended_value;
}
```
### Odladění zapojení
1. Nejdřív udělat zpětnou vazbu na zvukovce. 
2. Odladit přehrávání a záznam zvuku.
> [!note] Linux
> Pod Linuxem je potřeba nastavit správně vstupy a výstupy. Pomohlo nemít nastavený mikrofon, ale reproduktory na USB kartu. 


## 5. týden
Přidáváme knihovnu pro ARM.

> [!tip] Instalace knihovny
IOC -> midleware -> STMX-CUBE-ALGOBUILD
Stáhnout knihovnu. 
Vybrat DSP library a začkrtnout.

> [!tip] Přidání knihovny do projektu
IOC -> Midleware -> AlgoBuild
Zaškrtnout. 

```C
#include <arm_math.h>
```

### Použití knihovny `"math.h"` 
sinus -> 26 us
48kHz -> 20 us

> [!warning]
> Při použití obecné knihovny nestihneme generovat signál na vzorkovací frekvenci 48kHz!


```C
void copy_audio_input_to_output(){
	for(int i = 0 ; i<BlockSize; i++)
	{
		sample_L1[i]= sample_L[i];
		sample_R1[i]= sample_R[i];
	}
	Status_Process_DSP_Complete=1;
}

uint32_t phase; // posunuti v case
int Fs = 48000;//Hz
int f = 1000;//Hz
float ADC_max = 4194304;
float A = ADC_max/20;

void generate_sin(int* phase, float A, int f, int Fs, int n, float* array) {
	float omega = 2*PI*f/Fs;
	for(int i = 0; i<n; i++) {
		array[i] = A*arm_sin_f32(omega*(i+*phase));
	}
	*phase += n;
}
```

## 6. týden

CMSIS-DSP software library

- `arm_fir_init()` - inicializace filtru
- `arm_fir_fast()` - spuštění

Rozchodit fir filter na Nucleu.

Přidat také možnost odeslání dvou odpovědí na jeden požadavek.
`s2m_Status`

```C
// pockani na ukonceni odesilani po UARTu
while(s2m_Status) {}
```