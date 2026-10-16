# Grow Light Math

Grow light honesty. The box says a thousand watts, and the plant was always going to count
photons per day instead.

- Landing: `index.html`
- App: `app.html` (loads `engine.js`)

## What it does

The "wattage" on a grow light box is an equivalency claim, not a draw. The wall meter tells
the truth about watts, and the plant tells it in photons: PPFD at the canopy, summed over the
day into a DLI. Three panels of honest arithmetic:

- **The watt truth** - claimed "equivalent" watts versus the actual wall draw, as a percent
  of the claim.
- **The DLI truth** - the chart's PPFD carried from the chart height to your hanging height
  (inverse square), then across your daily hours into a DLI (PPFD x hours x 0.0036).
- **The need truth** - the delivered DLI weighed against the crop's appetite: required versus
  delivered, with the margin or the shortfall.

## Norms used (labeled, illustrative)

- DLI targets: 8 gentle, 14 moderate, 20 hungry.
- Inverse-square falloff from the chart height; DLI = PPFD x hours x 0.0036.

Every figure is hypothetical arithmetic on labeled norms, not a statement about any real
fixture, crop or tent. Trust a quantum meter and the seed packet.

## Tests

`oracle.py` generates `expected.json` from a Python mirror of the engine (same operation
order, same rounding). `node test.js` checks the JavaScript engine against it:

```
python3 oracle.py
node test.js
```
