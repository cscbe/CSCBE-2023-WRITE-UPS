# Corrupted GIF 2

## Category
Stego

## Estimated difficulty
Easy

## Description
The participants have to remove the bad GIF EOF marker.

## Scenario
This GIF file contained valuable information, but somehow it got corrupted...

## Write-up
The challenge presents an animated GIF image:

![challenge](./Challenge/Public/challenge.gif)

- At first sight, nothing seems wrong with this animation. When we [inspect the GIF file](https://movableink.github.io/gif-inspector/), we can see that the last frame has an offset of 35646 (0x8B3E) and a length of 3099 (0xC1B). If we have a look at 0x9759 (0x8B3E + 0xC1B) in a hexadecimal editor, we see the GIF terminator 0x3B as expected but also a new ExtensionBlock definition after this terminator (see [the GIF image format](https://www.daubnet.com/en/file-format-gif) as reference). The ExtensionBlock is used to indicate new frames in the animation. If we remove the GIF terminator 0x3B, the real last frame is revealed.

![intermediate](./Resources/intermediate.gif)

- Additionally, the animation can be stopped to make the last frame more readable. In order to do this, we need to set the Loop Count of the NETSCAPE extension that allows for GIF animations to a value higher than 0 (see [the GIF animation format](http://www.vurdalakov.net/misc/gif/netscape-looping-application-extension) as reference). If we set it to 1, the animation will play once and shows the flag.

![solution](./Resources/solution.gif)

## PoC script
`sed -r 's/\x3B\x21\xF9\x04/\x21\xF9\x04/g; s/\x4E\x45\x54\x53\x43\x41\x50\x45\x32\x2E\x30\x03\x01\x00\x00/\x4E\x45\x54\x53\x43\x41\x50\x45\x32\x2E\x30\x03\x01\x01\x00/g' ./challenge.gif > ./solution.gif`

## Flag
CSC{GCfbnGB2ubjAh5rs}

## Creator
Jelle Aerts

## Creator bio
--
