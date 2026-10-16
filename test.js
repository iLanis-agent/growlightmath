const engine = require("./engine.js");
const expected = require("./expected.json");
let checks = 0, fails = 0;
for (const c of expected) {
  checks++;
  let got;
  try {
    got = { out: engine[c.fn](...c.args) };
  } catch (e) {
    got = { err: e.message };
  }
  const want = c.err !== undefined ? { err: c.err } : { out: c.out };
  if (JSON.stringify(got) !== JSON.stringify(want)) {
    fails++;
    console.log("FAIL", c.fn, JSON.stringify(c.args), "got", JSON.stringify(got), "want", JSON.stringify(want));
  }
}
console.log(`${expected.length} cases / ${checks} checks, ${fails} failed`);
process.exit(fails ? 1 : 0);
