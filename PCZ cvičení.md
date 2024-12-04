# Cvičení a úkoly

### DMA

```C
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
	    // neagtive
        sign_extended_value = (0xFF000000 | value);
    } else  {
	    // positive
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
- `arm_fir_f32()` - spuštění "fast"

Rozchodit fir filter na Nucleu.

```C
// config
#define BLOCK_SIZE 10
#define NUM_TAPS 5
float32_t firStateF32[BLOCK_SIZE + NUM_TAPS + 1];
float32_t firCoeffs32[NUM_TAPS] = {0.2, 0.2, 0.2, 0.2, 0.2};
arm_fir_instance_f32 S;

// init
arm_fir_init_f32(&S, NUM_TAPS, firCoeffs32, firStateF32, BLOCK_SIZE);

// proces filter
arm_fir_f32(&S, &source, &dest, BLOCK_SIZE);
```

Koeficienty filtru si můžeme jednoduše vygenerovat v Matlabu pomocí filter designeru.

Přidat také možnost odeslání dvou odpovědí na jeden požadavek.
`s2m_Status`

```C
// pockani na ukonceni odesilani po UARTu
while(s2m_Status) {}
```

## 8. týden

> [!tip]
> `octave` má stejně barvičky jako `matlab`

```octave
% odesilame koeficienty filtru do nuklea
[b, nb] = My_FIR(8000, 12000, 80);
writeDataSTM32(app.s, 35008, nb, b);
```

## 9. týden
CMSIS-DSP software library:
- [IIR](https://arm-software.github.io/CMSIS_5/DSP/html/group__BiquadCascadeDF1.html)
- [arm_biquad_cascade_df1_f32](https://arm-software.github.io/CMSIS_5/DSP/html/group__BiquadCascadeDF1.html#gaab9bd89c50c5c9116a1389855924aa9d)

Použití SOS vygenerovaných ve filter designérů.
- Pásmová propust

- [ ] Rozchodit IIR filter na nucleu
	- [x] Stáhnout .mat file s filterem
	- [x] Odesílání konfigurace z Matlabu
	- [x] Spuštění na Nucleu
		- [x] Přepínač FIR/IIR
	- [ ] Odchycení odezvy
	- [ ] Porovnání výsledku s referenčním výpočtem v Matlabu
- [ ] Možnost spustit jak FIR tak IIR
- [ ] Měření času jak dlouho to trvá
```octave
% frekvenční charakteristika filtru
freqz()
% Nacteni filtru a prevedeni do formatu pro nucleo
math_file = "IIR_PP_CV09.mat"
filter_IIR = load(math_file)
% SOS - second order sections
% G - gains
% prevod do formatu vhodneho pro nucleo
iir_nucleo = IIR_2_STM32(filter_IIR.SOS, filter_IIR.G)
% odeslani do nuclea
writeDataSTM32(app.s, 35009, length(iir_nucleo), iir_nucleo)
```


Stavové proměnné potřebné pro IIR filter:
```C
#define NUM_STAGES_MAX 100
int number_of_stages = -1;

// Declare the coefficients and state buffer for the IIR filter
float biquadCoeffs[NUM_STAGES_MAX * 5];
float biquadState[NUM_STAGES_MAX * 4];

// Declare the instance of the IIR filter
arm_biquad_casd_df1_inst_f32 S_L_IIR, S_R_IIR;

enum FIR_IIR {
    FIR, 
    IIR
};
enum FIR_IIR filter_type = FIR;
```

Přijetí zprávy od matlabu a nastavení koeficientů:
```C
case 35009:
	HAL_SAI_DMAStop(&hsai_BlockA1);
	HAL_SAI_DMAStop(&hsai_BlockB1);

	// Přijmout koeficienty IIR filtru
	number_of_stages = nData_in_values / 5;
	for (int i = 0; i < nData_in_values; i++) {
		biquadCoeffs[i] = ((float *)xData)[i];
	}

	arm_biquad_cascade_df1_init_f32(&S_L_IIR, number_of_stages, biquadCoeffs, biquadState);
	filter_type = IIR;

	HAL_SAI_Transmit_DMA(&hsai_BlockA1,(uint8_t *) buf_SAI_TX, 4*BlockSize);
	HAL_SAI_Receive_DMA(&hsai_BlockB1,(uint8_t *) buf_SAI_RX, 4*BlockSize);
	break;
```

Aktualizace funkce proces Samples, která má podporu přepínání mezi FIR a IIR filtrem:
```C
void ProcessSamples()
{
	Status_Process_DSP_Complete=0;
	
    if (filter_type == FIR) {
        arm_fir_f32(&S_L_FIR, sample_L, sample_L1, BlockSize);
    } else {
        arm_biquad_cascade_df1_f32(&S_L_IIR, sample_L, sample_L1, BlockSize);
    }

	for (int i = 0; i < BlockSize; i++) {
        sample_R1[i] = sample_L[i];
    }
	
    Status_Process_DSP_Complete = 1;
}
```


> [!warning]
> Při kopírování Matlab -> Nucleo je potřeba otočit koeficinety filtru!
> $-A$
## 10. týden Tónová volba
```C
arm_rfft_fast_f32 // fft
arm_mult_f32 // vektrove nasobeni pro okenkovaci funkci
```

Hammingovo okno, nebo jiná okénkovací funkce. 

- [ ] přehrání tónové volby na počítači v Matlabu
- [ ] Matlab přijme zprávu s dekódováním tónové volby a zobrazí ji

## 11. týden: realizace FFT, projekt SCRAMBLER, samostatná práce

V rámci výuky jiného předmětu bude zaměněna stávající redukce za redukci "EXP KIT", kde je prohozeno `TR (B)` a `RE (A)` a A je master a B sync. slave na stejný SAI - nutno překonfigurovat.

### SCRAMBLER

Chceme otočit složení spektra, tak aby:
- nízké frekvence byli  -> vysoké,
- vysoké -> nízké 

![[schema_scambler.png]]

Docílíme toho tak že namodulujeme signál na nosnou frekvenci, které nebude daleko od našeho pozorovaného spektra. Spektrum v okolí nosné frekvence má převrácený charakter. Pokud bude nosná frekvence odpovídat nejvyšší složce našeho spektra 

Postup:
- Filtrace DP
- Modulace na nosnou
- Filtrace DP

### Generování sinu

``` Octave
% apmlituda
A = 2
n = 100 % sec
% frekvence
f = 3100
Fs = 48000

% omega
w0 = 2*pi*f*/Fs

% nastaeveni koeficientu
a1 = -2 * cos(w0)
a2 = 1
b0 = A .* sin(w0)

% pocatecni hodnoty
y0 = b0
y(1) = -a1 * y0
y(2) = -a1 * y(1) - a2*y0

for n=3:n*Fs
	y(n) = -a1 * y(n-1) - a2*y(n-2)
end

plot(y)
```

Implementace v C:
```C
void start_sin_generator(float A, float omega, float* a1, float* a2, float* y_prew, float* y_prew2) {
	float y0 = A*arm_sin_f32(omega);
	*a1 = -2 * cos(omega);
	*a2 = 1;
	*y_prew = -a1*y0;
	*y_prew2 = -a1* (*y_prew) - a2 * y0;
}

float generate_next_sin_value(float A, float omega, float a1, float a2, float* y_prew, float* y_prew2){
	float y_new = -a1* (*y_prew) -a2* (*y_prew2);
	*y_prew2 = *y_prew;
	*y_prew = y_new;
	return y_new;
}
```
Použití v C:
```C
A = 2;
f1 = 3000;
Fs = 48000;
omega = 2*PI*f1/Fs;
start_sin_generator(A, omega, &a1, &a2, &y_prew, &y_prew2);
```

S použitím struktury:
```C
#include <stdlib.h>

typedef struct {
	float amplitude;
	float omega;
	float a1;
	float a2;
	float y_prew[2];
} sin_genarator_t;

sin_genarator_t* start_sin_generator(float A, float omega) {
	sin_genarator_t* sin_gen = (sin_genarator_t*)malloc(sizeof(sin_genarator_t));
	float y0 = A*sin(omega);
	sin_gen->amplitude = A;
	sin_gen->omega = omega;
	sin_gen->a1 = -2 * cos(omega);
	sin_gen->a2 = 1;
	sin_gen->y_prew[0] = -sin_gen->a1*y0;
	sin_gen->y_prew[1] = -sin_gen->a1* (sin_gen->y_prew[0]) - sin_gen->a2 * y0;
	return sin_gen;
}

float generate_next_sin_value(sin_genarator_t* sin_gen){
	float y_new = - sin_gen->a1 * (sin_gen->y_prew[0]) - sin_gen->a2 * (sin_gen->y_prew[1]);
	sin_gen->y_prew[1] = sin_gen->y_prew[0];
	sin_gen->y_prew[0] = y_new;
	return y_new;
}
```

### TODO:
- Nucleo:
	- [x] Přijímání zprávy,
	- [x] Nastavení filtru,
	- [x] Generování sinu,
- Matlab:
	- [x] Odesílání zprávy,
		- [x] Dolnopropustní filtr,
		- [x] Frekvence nosné,
	- [x] generování signálu,
	- [x] Vizualizace

## Nápad
Zavést logování zpráv na Nucleu.
Odesílání zpráv:
- Info
- warning
- Error

Přidání okna terminál do Matlab App.
Vypisování zpráv, které chodí z nuclea.

Implementace fronty zpráv pro neblokované odesílání z nuclea. 

Instalace matlabu na win10.
Normalizace systému zpráv.

