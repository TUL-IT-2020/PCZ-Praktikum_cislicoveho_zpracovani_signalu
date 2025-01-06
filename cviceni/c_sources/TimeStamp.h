/*
 * verze 15.10.2024
 * By Korner
 */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __TIMESTAMP_H
#define __TIMESTAMP_H

#ifdef __cplusplus
extern "C" {
#endif

#include "main.h"


#define TIME_STAMP_BUF_LEN 256 
//#define TIME_STAMP_BUF_LEN 512
//#define TIME_STAMP_BUF_LEN 1024
#define TIME_STAMP_BUF_MASK TIME_STAMP_BUF_LEN - 1
TIM_HandleTypeDef *TimeStamp_htim;
volatile uint32_t *TimeStamp_CNT;

// struct for time and stamp
typedef struct {
	uint32_t time;
	uint8_t stamp;
} TimeStamp_t;

// pole timestampu
TimeStamp_t TimeStamp[TIME_STAMP_BUF_LEN];
// indexy pro zapis a cteni
uint_fast8_t TimeStamp_index;


// par. timer
void TimeStamp_RESET() {
	TimeStamp_index = 0;
}

HAL_StatusTypeDef TimeStamp_INIT(TIM_HandleTypeDef *htim)
{
	TimeStamp_RESET();
	TimeStamp_htim= htim;
	TimeStamp_CNT = &TimeStamp_htim->Instance->CNT;
	HAL_StatusTypeDef s = HAL_TIM_Base_Start_IT(htim);// for time measure
	return(s);
}

/*
 * Decrement timestamp index
 * Prevent overflow of index by using TIME_STAMP_BUF_MASK
 */
void index_decrement(uint_8 *index) {
	*index = (*index - 1) & TIME_STAMP_BUF_MASK;
}

/*
 * Increment timestamp index
 * Prevent overflow of index by using TIME_STAMP_BUF_MASK
 */
viod index_incement(uint_8 *index) {
	*index = (*index + 1) & TIME_STAMP_BUF_MASK;
}

/*
 * Increment timestamp index
 * Prevent overflow of index by using TIME_STAMP_BUF_MASK
 */
void TimeStamp_index_increment() {
	index_incement(&TimeStamp_index);
}

/*
 * Nastaveni casoveho razitka
 * c - razitko
 * 
 * Vraci index, na ktery bylo razitko ulozeno.
 */
uint_8 TimeStamp_SET(uint_8 c) {
	TimeStamp_t *ts = &TimeStamp[TimeStamp_index];
	ts->time = *TimeStamp_CNT;
	ts->stamp = c;
	// aktualizace indexu, 
	// plus stejna logika jako u modula, aby index nepretekl
	TimeStamp_index_increment();
	return TimeStamp_index;
}

/*
 * Nastaveni casoveho razitka
 * c - razitko
 * 
 * Vraci index, na ktery bylo razitko ulozeno.
 */
uint8_t TimeStamp_SET(char c) {
	return TimeStamp_SET((uint8_t)c);
}

/*
 * Nacteni casoveho razitka
 * c - razitko
 * 
 * Vraci cas, kdy bylo razitko ulozeno.
 * Prevzato od kolegy Mahra
 */
uint32_t TimeStamp_GET(uint8_t c) {
	uint_fast8_t i = TimeStamp_index;
	do {
		index_decrement(&i);
	} while (TimeStamp[i].stamp != c && i != TimeStamp_index);
	return TimeStamp[i].time;
}

/*
 * Nacteni casoveho razitka
 * c - razitko
 * 
 * Vraci cas, kdy bylo razitko ulozeno.
 */
uint32_t TimeStamp_GET(char c) {
	return TimeStamp_GET((uint8_t)c);
}

/*
 * Absolutni rozdil casu
 * Porovnava dva casy a vraci jejich rozdil.
 */
uint32_t abs_diference(uint32_t a, uint32_t b) {
	return a > b ? a - b : b - a;
}

/*
 * Rozdil casu mezi dvema razitky
 * c1 - prvni razitko
 * c2 - druhe razitko
 */
uint32_t TimeStamp_DIFF(uint8_t c1, uint8_t c2) {
	uint32_t time_1 = TimeStamp_GET(c1);
	uint32_t time_2 = TimeStamp_GET(c2);
	// nevime ktery cas je starsi, takze musime zjistit absolutni rozdil
	return abs_diference(time_2, time_1);
}

/*
 * Rozdil casu mezi dvema razitky
 * c1 - prvni razitko
 * c2 - druhe razitko
 */
uint32_t TimeStamp_DIFF(char c1, char c2) {
	return TimeStamp_DIFF((uint8_t)c1, (uint8_t)c2);
}

/*
 * Rozdil casu mezi dvema indexy
 * index_1 - prvni index
 * index_2 - druhy index
 */
uint32_t TimeStamp_DIFF_INDEX(uint8_t index_1, uint8_t index_2) {
	uint32_t time_1 = TimeStamp[index_1].time;
	uint32_t time_2 = TimeStamp[index_2].time;
	return abs_diference(time_2, time_1);
}


#ifdef __cplusplus
}
#endif

#endif /* __TIMESTAMP_H */
