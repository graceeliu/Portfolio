/* deck.js — click-through slide viewer for case study pages.

   Usage: export slides as images named slide-01.jpg, slide-02.jpg, …
   into a folder in assets/, then add the .deck block (copy it from
   work/msk-llm-evaluation.html) with:
     data-count = number of slides
     data-path  = folder + "slide-"   (the number and .jpg are added here)
   and include <script src="../deck.js"></script> before </body>.
*/
document.querySelectorAll(".deck").forEach(deck => {
  const n = +deck.dataset.count;
  const path = deck.dataset.path;
  const img = deck.querySelector(".deck-img");
  const count = deck.querySelector(".deck-count");
  const thumbs = deck.querySelector(".deck-thumbs");
  const src = i => `${path}${String(i).padStart(2, "0")}.jpg`;
  let cur = 1;

  for (let i = 1; i <= n; i++) {
    const b = document.createElement("button");
    b.type = "button";
    b.setAttribute("role", "listitem");
    b.setAttribute("aria-label", `Go to slide ${i}`);
    b.innerHTML = `<img src="${src(i)}" alt="" loading="lazy">`;
    b.addEventListener("click", () => go(i));
    thumbs.appendChild(b);
  }

  function go(i) {
    cur = Math.min(n, Math.max(1, i));
    img.src = src(cur);
    img.alt = `Slide ${cur} of ${n}`;
    count.textContent = `${cur} / ${n}`;
    deck.querySelector(".deck-prev").disabled = cur === 1;
    deck.querySelector(".deck-next").disabled = cur === n;
    thumbs.querySelectorAll("button").forEach((b, k) => {
      const on = k + 1 === cur;
      b.classList.toggle("is-on", on);
      if (on) b.setAttribute("aria-current", "true"); else b.removeAttribute("aria-current");
    });
    const t = thumbs.children[cur - 1];
    thumbs.scrollTo({ left: t.offsetLeft - thumbs.clientWidth / 2 + t.clientWidth / 2, behavior: "smooth" });
    if (cur < n) new Image().src = src(cur + 1);   // preload next
  }

  deck.querySelector(".deck-prev").addEventListener("click", () => go(cur - 1));
  deck.querySelector(".deck-next").addEventListener("click", () => go(cur + 1));

  // Arrow keys work once the viewer has been clicked or tabbed into
  deck.tabIndex = 0;
  deck.addEventListener("keydown", e => {
    if (e.key === "ArrowRight") { go(cur + 1); e.preventDefault(); }
    if (e.key === "ArrowLeft")  { go(cur - 1); e.preventDefault(); }
  });

  // Swipe on touch screens
  let x0 = null;
  img.addEventListener("touchstart", e => { x0 = e.touches[0].clientX; }, { passive: true });
  img.addEventListener("touchend", e => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 40) go(cur + (dx < 0 ? 1 : -1));
    x0 = null;
  });

  const full = deck.querySelector(".deck-full");
  const stage = deck.querySelector(".deck-stage");
  if (!stage.requestFullscreen) { full.hidden = true; }
  full.addEventListener("click", () => {
    if (document.fullscreenElement) document.exitFullscreen();
    else { stage.requestFullscreen(); deck.focus(); }
  });
  document.addEventListener("fullscreenchange", () => {
    full.textContent = document.fullscreenElement ? "Exit full screen" : "Full screen";
  });
  // keys still work in full screen
  document.addEventListener("keydown", e => {
    if (document.fullscreenElement !== stage || deck.contains(document.activeElement)) return;
    if (e.key === "ArrowRight") go(cur + 1);
    if (e.key === "ArrowLeft")  go(cur - 1);
  });

  go(1);
});
