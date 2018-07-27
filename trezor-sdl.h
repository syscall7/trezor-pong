#ifndef SDL_H
#define SDL_H

#include <stdint.h>

typedef enum {
    SDL_FALSE = 0,
    SDL_TRUE  = 1
} SDL_bool;

typedef int8_t      Sint8;
typedef uint8_t     Uint8;
typedef int16_t     Sint16;
typedef uint16_t    Uint16;
typedef int32_t     Sint32;
typedef uint32_t    Uint32;
typedef int64_t     Sint64;
typedef uint64_t    Uint64;

typedef struct SDL_Surface {
    int w, h;               /**< Read-only */
} SDL_Surface;

typedef struct SDL_Rect {
    Sint16 x, y;
    Uint16 w, h;
} SDL_Rect;

int
SDL_Flip(SDL_Surface *screen);

int
SDL_FillRect(SDL_Surface *dst, SDL_Rect *dstrect, Uint32 color);

Uint32
SDL_GetTicks(void);

void
SDL_Delay(Uint32 ms);

#endif /* SDL_H */
