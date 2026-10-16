// Grow Light Math engine - hypothetical arithmetic on labeled norms only.
// Watt claims, PPFD charts and DLI targets are published or typical norms,
// not measurements of your fixture or your plants.

function plural(n, one, many) { return n === 1 ? one : many; }
function tenths(x) { return Math.floor(x * 10 + 0.5) / 10; }
function fixed1(x) { return tenths(x).toFixed(1); }

const NEED = [8, 14, 20]; // labeled norm: DLI target, gentle / moderate / hungry
const CROP = ["gentle", "moderate", "hungry"];

function wattTruth(claim, draw) {
  if (!(claim > 0)) throw new Error("the claimed watts must be above zero");
  if (!(draw > 0)) throw new Error("the wall draw must be above zero");
  const pct = tenths(draw / claim * 100);
  let band;
  if (pct < 12) band = "about a tenth";
  else if (pct < 22) band = "about a fifth";
  else if (pct < 38) band = "about a third";
  else if (pct < 70) band = "about half";
  else band = "most of the claim";
  return `The box claims ${claim} ${plural(claim, "watt", "watts")} and the wall meter reads ${draw} - ${pct.toFixed(1)}% of the claim, ${band} honestly.`;
}

function dliTruth(ppfd, refH, hangH, hours) {
  if (!(ppfd > 0)) throw new Error("the chart PPFD must be above zero");
  if (!(refH > 0)) throw new Error("the chart height must be above zero");
  if (!(hangH > 0)) throw new Error("the hanging height must be above zero");
  if (!(hours > 0)) throw new Error("the daily hours must be above zero");
  if (!(hours <= 24)) throw new Error("the daily hours must be 24 or fewer");
  const at = ppfd * Math.pow(refH / hangH, 2);
  const dli = at * hours * 0.0036;
  return `The chart's ${ppfd} µmol at ${refH} ${plural(refH, "inch", "inches")} hangs at ${hangH} ${plural(hangH, "inch", "inches")} as ${fixed1(at)} µmol; ${hours} ${plural(hours, "hour", "hours")} a day grows a DLI of ${fixed1(dli)} honestly.`;
}

function needTruth(dli, level) {
  if (!(dli > 0)) throw new Error("the delivered DLI must be above zero");
  const need = NEED[level];
  const dm = tenths(dli - need);
  let verdict;
  if (dm > 0) verdict = `a margin of ${fixed1(dm)} honestly`;
  else if (dm < 0) verdict = `${fixed1(-dm)} short honestly`;
  else verdict = "exactly matched honestly";
  return `A ${CROP[level]} crop asks for a DLI of ${fixed1(need)}; the lamp delivers ${fixed1(dli)} - ${verdict}.`;
}

if (typeof module !== "undefined") {
  module.exports = { wattTruth, dliTruth, needTruth };
}
