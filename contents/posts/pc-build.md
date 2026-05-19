---
title: PC Build for Gaming (2025)
created_at: 2025-02-23T12:34:56.789Z
slug: /gaming-pc-build-2025
---

After four years, I have finally built a new PC.

| Component     | Name                                                         |
| ------------- | ------------------------------------------------------------ |
| Motherboard   | MSI MPG X670E CARBON WIFI                                    |
| CPU           | AMD Ryzen 7 9800X3D                                          |
| CPU Cooler    | ARCTIC Liquid Freezer III 360                                |
| Graphics Card | Colorful iGame RTX 4080 SUPER Advanced OC 16GB               |
| RAM           | Predator Hera DDR5 6400 32GB * 2                             |
| Hard Drives   | Samsung 990 PRO 2TB / Samsung 980 PRO 1TB / WD Black SN750 1TB |
| PSU           | Super Flower Leadex VII XG 1300W                             |
| Case          | Fractal Design North XL White TG                             |
| Rear fan      | Thermalright TL-B14B EXTREM (Black)                          |

I'm keeping my old graphics card and SSDs until I can afford the RTX 5090, which is now sky-high in price. 🙂

![IMG_7092](https://cdn.sa.net/2025/02/03/8jyKIkOVizYmGN1.jpg)

## Why?

I have been playing World of Warcraft again for several months now, and my previous build's CPU (AMD Ryzen 7 5800X) is obivously the bottleneck. An X3D CPU will perform better in MMORPGs, even at 4K resolution (NB: I play all games in 4K, regardless of framerate).

And since I am a pro-4K guy, I would like to get the latest RTX 5090 so that I can have a better experience.

> I'm really not into cable management — it just doesn't feel right to me. 😅

## Consideration

### Motherboard

I bought a brand-new X670E motherboard for this build because I'm not interested in the latest chips (X870, X870E & B850) featuring USB4, which sacrifices some original PCIe lanes. Besides, I don't need >= 5GbE LAN as my home network currently runs at 1GbE and isn't slated for a major upgrade until 2027.

Cost-effectiveness matters here, since a motherboard rarely offers significant performance gains.

MSI MPG X670E CARBON WIFI is a motherboard which has 4 M.2 slots and I love the extensibility of it.

### PSU

I did tons of research before making my decision, and to be honest, the Leadex VII XG 1300w was not my first pick. I initially bought [FSP's Hydro PTM PRO 1350W](https://www.fsplifestyle.com/en/product/HydroPTMPRO1350W_12V2X6.html) which had a problem that I just couldn't stand. You can check out the video in the next section for more details.

### Use Cases

It's mainly a gaming PC, so FPS matters here. I might use it for some development work but I prefer using my MacBook Pro (M1 Pro) over this, if possible.

## Tuning

### CPU

Just enable the PBO settings. Bang!

### RAM

![image-20250203160621198](https://cdn.sa.net/2025/02/03/5oLRm4Kn8ZdGtkz.png)

> [!NOTE]
> 
>Just enable EXPO or XMP if you think this doesn't make sense to you.

There are lots of posts and screenshots of settings to guide you how to tweak your RAM. Overclocking 32GB x2 is a bit more physically challenging than 16GB x2, so make sure to double-check whether the post you're viewing fits your case. If you decide to buy the same RAM as I did, the screenshot above might provide some helpful clues.

#### Why 6200 with CL28?

- You won't see much performance gain by opting for a higher frequency (e.g., 8400) RAM
  - The X670E chip might not even work with DDR5 8000+ RAM either, according to [the compatibility list](https://www.predatorstorage.com/u_file/fileUpload/2024-12/16/Memory%20Module%20Platform%20Compatibility%20List.pdf) on Predator's website.
- Lower latency will definitely benefit MMORPG performance.

## Known Issues

### AIO Cooler

- All the fans suddenly stop spinning, which caused CPU overheat and shutdown. It just happened once, though.

### PSU

- The Hydro PTM Pro 1350W, for which I have already requested a refund, produces a horrible "tada-tada" sound when the CPU and GPU are under moderate load:
  <iframe class="aspect-video w-full" height="300" src="https://www.youtube.com/embed/9B8Pv2efoug?si=CkDImFgoIAlhaGbi" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
  
  Before requesting a refund, I contacted their technical support and they told me that this is normal - it's the sound produced when the PC reaches the critical point between low and medium load.

  At first, I thought this was an acceptable answer since it's completely reproducible by controlling the maximum FPS in the game settings. However, I think this will become extremely annoying if I have to configure every game's settings.

  Before asking for a refund, I requested an exchange but the issue remained exactly the same. Personally, I consider this an unacceptable flaw, and I'm not sure if it's an only isolated case.

### Misc.

- There is some buzzing noise that I can't yet confirm the source right now when the PC is not under load or even hibernate. It could last for several seconds and is quite annoying since I expect my work environment to be as quiet as possible when the PC is idle (i.e., when I'm not playing games).
  - I suspect it's coming from the PSU, but it seems that every PSU I've bought has the same issue, which is quite confusing.
- The GPU has some [coil whine](https://www.youtube.com/results?search_query=coil+whine) when it's under load, but that's acceptable to me since I'll likely be gaming with the speakers on.
