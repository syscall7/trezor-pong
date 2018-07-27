/* -------------------------------------------------------------------------- *
 * File: trezor-sdl.c
 * Description: Simple SDL implementation for Pong on the Trezor
 * Author: Anthony DeRosa
 * Date July 2018
 * -------------------------------------------------------------------------- */
#include <stdint.h>
#include <sys/param.h>

#include "usb.h"
#include "timer.h"
#include "oled.h"
#include "trezor-sdl.h"

int
SDL_FillRect(SDL_Surface *dst, SDL_Rect *dstrect, Uint32 color)
{
    (void) dst;
    (void) color;
    oledBox(MIN(OLED_WIDTH-1, dstrect->x),
            MIN(OLED_HEIGHT-1, dstrect->y),
            MIN(OLED_WIDTH-1, dstrect->x + dstrect->w),
            MIN(OLED_HEIGHT-1, dstrect->y + dstrect->h),
            color);
    return 0;
}

Uint32
SDL_GetTicks(void)
{
    return timer_ms();
}

void
SDL_Delay(Uint32 ms)
{
    usbSleep(ms);
}

int
SDL_Flip(SDL_Surface *screen)
{
    (void) screen;
    oledRefresh();
    return 0;
}
