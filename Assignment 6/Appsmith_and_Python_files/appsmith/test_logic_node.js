// Runs the EXACT AssignmentLogic.js JSObject code in Node with stand-ins for the
// Appsmith globals (appsmith.store, storeValue, showAlert, resetWidget, widgets).
// This verifies the logic only; it is NOT a test of the Appsmith UI.
const fs = require("fs"), vm = require("vm"), path = require("path");
const src = fs.readFileSync(path.join(__dirname, "AssignmentLogic.js"), "utf8")
  .replace("export default", "module.exports =");
const cases = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));

function freshApp() {
  const ctx = { module: {}, alerts: [] };
  ctx.appsmith = { store: {} };
  ctx.storeValue = async (k, v) => { ctx.appsmith.store[k] = v; };
  ctx.showAlert = (m, t) => ctx.alerts.push([t, m]);
  ctx.resetWidget = (n) => { ctx[n].text = ""; };
  ctx.inp_course = { text: "" }; ctx.inp_title = { text: "" };
  vm.createContext(ctx); vm.runInContext(src, ctx);
  return ctx;
}

(async () => {
  let pass = 0; const out = [];
  console.log("AssignmentLogic.js (Appsmith JSObject) — logic run in Node " + process.version + "\n");
  for (const c of cases) {
    const ctx = freshApp(); const L = ctx.module.exports;
    for (const [a, b] of c.pre) { ctx.inp_course.text = a; ctx.inp_title.text = b; await L.add.call(L); }
    const before = JSON.stringify(ctx.appsmith.store.assignments || []);
    ctx.inp_course.text = c.course; ctx.inp_title.text = c.title;
    await L.add.call(L);
    const list = ctx.appsmith.store.assignments || [];
    const msg = ctx.appsmith.store.message.replace(/^ERROR: /, "");
    const stored = !ctx.appsmith.store.isError;
    let ok = stored === c.stored && msg === c.msg && list.length === c.count;
    if (c.stored) ok = ok && JSON.stringify(list[list.length - 1]) === JSON.stringify({ course: c.store_as[0], title: c.store_as[1] });
    else ok = ok && JSON.stringify(list) === before;
    if (ok) pass++;
    out.push({ id: c.id, stored, msg, count: list.length, passed: ok });
    console.log(`${c.id}  ${ok ? "PASS" : "FAIL"}  stored=${String(stored).padEnd(5)} count=${list.length}  msg='${msg}'`);
  }
  // v1.1 extras (control characters, NFC, emoji length)
  const L = freshApp().module.exports;
  const ext = [
    ["ANSI escape in title", () => L.addTo([], "Math", "Lab\x1b[2J FAKE")],
    ["bidi override in title", () => L.addTo([], "Math", "Quiz ‮1 txt.exe")],
    ["NFC vs NFD duplicate", () => L.addTo(L.addTo([], "French", "Café"), "French", "Café")],
    ["30 emoji course (code points)", () => L.addTo([], "\u{1F4D8}".repeat(30), "Essay")],
  ];
  console.log("");
  for (const [n, f] of ext) {
    try { const r = f(); console.log(`${n.padEnd(32)} -> stored (${r.length} item)`); }
    catch (e) { console.log(`${n.padEnd(32)} -> rejected: ${e.message}`); }
  }
  console.log(`\n${pass}/${cases.length} passed`);
  fs.writeFileSync(process.argv[3], JSON.stringify(out, null, 1));
})();
