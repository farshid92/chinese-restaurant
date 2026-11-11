# Lucky Lid

An interactive ordering page for an imaginary dim sum and sushi restaurant. Customers pick dishes from a spinning turntable, chopsticks carry them into takeaway boxes on the table, and the bill fills in as they go.

This is a concept site. The checkout does not send an order anywhere.

## Run it

Open `index.html` in a browser. There is no build step and no server.

## Files

- `index.html`: the page, its styles and its script
- `menu.js`: the menu (dishes, prices, descriptions) and the restaurant details shown in the info panel. Edit this file to change what the site sells.
- `assets/`: dish illustrations, packaging, background, and the GSAP animation library
- `brand/`: logo files
- `tools/`: the Python scripts used to cut out the artwork and build the background. They were written for one machine, so their file paths need adjusting before reuse.

## Credits

Dish and packaging illustrations were generated with an AI image tool and cut out with the scripts in `tools/`. Fonts are Limelight, Bungee and DM Mono from Google Fonts. Animation uses GSAP.
