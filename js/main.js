/* Zenith AI 研学社 · 官网交互 */
(function () {
  "use strict";

  /* ── 系统设置：用户开了「减少动态效果」就不启动装饰动画 ── */
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ── 导航：滚动状态 + 移动端菜单 ── */
  var nav = document.getElementById("nav");
  var navToggle = document.getElementById("navToggle");
  var navLinks = document.getElementById("navLinks");

  function onScroll() {
    if (window.scrollY > 10) nav.classList.add("is-scrolled");
    else nav.classList.remove("is-scrolled");
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  navToggle.addEventListener("click", function () {
    var open = navLinks.classList.toggle("open");
    navToggle.setAttribute("aria-expanded", open ? "true" : "false");
  });
  navLinks.addEventListener("click", function (e) {
    if (e.target.tagName === "A") {
      navLinks.classList.remove("open");
      navToggle.setAttribute("aria-expanded", "false");
    }
  });

  /* ── 滚动显现 ── */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  }

  /* ── 星空 ── */
  var starsBox = document.getElementById("stars");
  if (starsBox && !reduceMotion) {
    var html = "";
    for (var i = 0; i < 42; i++) {
      var big = i % 9 === 0;
      var size = big ? 3 : 2;
      html += '<span class="star' + (big ? " big" : "") + '" style="left:' +
        (Math.random() * 98) + "%;top:" + (Math.random() * 70) +
        "%;width:" + size + "px;height:" + size + "px;--d:" +
        (2 + Math.random() * 4).toFixed(1) + 's"></span>';
    }
    starsBox.innerHTML = html;
  }

  /* ── Hero 打字机金句轮播 ── */
  var quoteLine = document.getElementById("quoteLine");
  var quotes = [
    "AI 不是指南针，它是油门。",
    "用 AI 加速错误的人，比不用 AI 的人死得更快。",
    "深内容，浅表达。看完是\"原来如此\"，不是\"完了完了\"。",
    "山顶见。"
  ];
  if (quoteLine && !reduceMotion) {
    var qi = 0, ci = 0, deleting = false;
    (function type() {
      var q = quotes[qi];
      quoteLine.textContent = q.slice(0, ci);
      var delay = deleting ? 45 : 110;
      if (!deleting && ci === q.length) { delay = 2200; deleting = true; }
      else if (deleting && ci === 0) { deleting = false; qi = (qi + 1) % quotes.length; delay = 500; }
      ci += deleting ? -1 : 1;
      setTimeout(type, delay);
    })();
  } else if (quoteLine) {
    quoteLine.textContent = quotes[0];
  }

  /* ── 工具 1：开店决策小测 ── */
  var quiz = document.getElementById("quiz");
  if (quiz) {
    var qs = quiz.querySelectorAll(".quiz-q");
    var resultBox = document.getElementById("quizResult");
    var resultTitle = document.getElementById("quizTitle");
    var resultDesc = document.getElementById("quizDesc");
    var votes = { franchise: 0, self: 0 };
    var step = 0;

    var RESULTS = {
      franchise: {
        title: "🏪 你适合开「加盟店」",
        desc: "省心优先，让别人把流程铺好。对应 WorkBuddy：开箱即用、按量付费、平台帮你兜底。适合预算紧、想先跑起来的团队——先活下来，再谈自主。"
      },
      self: {
        title: "🧗 你适合开「自营店」",
        desc: "一切自己说了算。对应 DeepSeek Harness：自主可控、长期成本更低，但要自己养流程。适合愿意投入换长期自主的团队——慢，但是自己的。"
      }
    };

    function showResult() {
      var pick = votes.franchise >= 2 ? "franchise" : "self";
      resultTitle.textContent = RESULTS[pick].title;
      resultDesc.textContent = RESULTS[pick].desc;
      qs.forEach(function (q) { q.hidden = true; });
      resultBox.hidden = false;
    }

    quiz.addEventListener("click", function (e) {
      var opt = e.target.closest(".opt");
      if (!opt) return;
      votes[opt.dataset.ans] += 1;
      step += 1;
      if (step < qs.length) {
        qs[step - 1].hidden = true;
        qs[step].hidden = false;
      } else {
        showResult();
      }
    });

    var again = document.getElementById("quizAgain");
    if (again) {
      again.addEventListener("click", function () {
        votes = { franchise: 0, self: 0 };
        step = 0;
        resultBox.hidden = true;
        qs.forEach(function (q, i) { q.hidden = i !== 0; });
      });
    }
  }

  /* ── 工具 2：你是哪种 AI 用户？ ── */
  var quiz2 = document.getElementById("quiz2");
  if (quiz2) {
    var q2s = quiz2.querySelectorAll(".quiz-q");
    var r2Box = document.getElementById("quiz2Result");
    var r2Title = document.getElementById("quiz2Title");
    var r2Desc = document.getElementById("quiz2Desc");
    var v2 = { free: 0, stuff: 0, stuck: 0 };
    var s2 = 0;
    var R2 = {
      free: { title: "🌪️ 你是「跟风自由党」", desc: "你追求自由，但先看别人用什么。工具换了一茬又一茬，能力却没沉淀下来——自由是假的，跟风是真的。先想清楚：你要的到底是自由，还是存在感。" },
      stuff: { title: "💸 你是「家当白送党」", desc: "你只盯着免费和便宜，把已投入的当宝贝舍不得扔。可工具换代时，旧积累会一夜贬值——别让'家当'绑架你换更好的路。省下的钱，常会花在更贵的地方。" },
      stuck: { title: "🧱 你是「赖着不走党」", desc: "你离不开手里的工具，哪怕它涨价、变差、跟不上。确定性是资产没错，但抱着不放就成了包袱——该换的时候要敢换。确定性值钱，僵化不值钱。" }
    };
    function showR2() {
      var pick;
      if (v2.free >= 2) pick = "free";
      else if (v2.stuff >= 2) pick = "stuff";
      else if (v2.stuck >= 2) pick = "stuck";
      else pick = v2.free >= v2.stuff && v2.free >= v2.stuck ? "free" : (v2.stuff >= v2.stuck ? "stuff" : "stuck");
      r2Title.textContent = R2[pick].title;
      r2Desc.textContent = R2[pick].desc;
      q2s.forEach(function (q) { q.hidden = true; });
      r2Box.hidden = false;
    }
    quiz2.addEventListener("click", function (e) {
      var opt = e.target.closest(".opt");
      if (!opt) return;
      v2[opt.dataset.ans] += 1;
      s2 += 1;
      if (s2 < q2s.length) { q2s[s2 - 1].hidden = true; q2s[s2].hidden = false; }
      else showR2();
    });
    var again2 = document.getElementById("quiz2Again");
    if (again2) again2.addEventListener("click", function () {
      v2 = { free: 0, stuff: 0, stuck: 0 }; s2 = 0;
      r2Box.hidden = true;
      q2s.forEach(function (q, i) { q.hidden = i !== 0; });
    });
  }

  /* ── 好玩：鼠标光斑（紫色微光跟随；首次移动才亮，免得加载时页中央先冒一团光；
        触屏设备没有鼠标，直接不建这层）── */
  if (!reduceMotion && window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
    var glow = document.createElement("div");
    glow.className = "cursor-glow";
    document.body.appendChild(glow);
    var gx = 0, gy = 0, tx = 0, ty = 0, raf = null;
    document.addEventListener("mousemove", function (e) {
      if (!glow.classList.contains("is-on")) {
        gx = tx = e.clientX; gy = ty = e.clientY;
        glow.style.transform = "translate(" + (gx - 160) + "px," + (gy - 160) + "px)";
        glow.classList.add("is-on");
        return;
      }
      tx = e.clientX; ty = e.clientY;
      if (!raf) raf = requestAnimationFrame(function step() {
        gx += (tx - gx) * 0.12; gy += (ty - gy) * 0.12;
        glow.style.transform = "translate(" + (gx - 160) + "px," + (gy - 160) + "px)";
        if (Math.abs(tx - gx) > 0.5 || Math.abs(ty - gy) > 0.5) raf = requestAnimationFrame(step);
        else raf = null;
      });
    }, { passive: true });
  }

  /* ── 好玩：Hero 入场动画（错峰浮现）── */
  var heroEls = document.querySelectorAll(".hero .fade-up");
  if (heroEls.length) {
    heroEls.forEach(function (el, i) {
      el.style.animationDelay = (0.15 + i * 0.12) + "s";
    });
  }

  /* ── 动态：Hero 山视差（滚动时山缓移）── */
  var mount = document.querySelector(".hero-mountain");
  if (mount && !reduceMotion) {
    window.addEventListener("scroll", function () {
      var y = window.scrollY;
      if (y < innerHeight) mount.style.transform = "translateY(" + (y * 0.22) + "px)";
    }, { passive: true });
  }
})();
