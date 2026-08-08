(() => {
  "use strict";

  const ready = (callback) => {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", callback, { once: true });
      return;
    }
    callback();
  };

  ready(() => {
    const screens = Array.from(document.querySelectorAll("[data-screen]"));
    const previewButtons = Array.from(document.querySelectorAll("[data-preview]"));
    const actualScreens = Array.from(document.querySelectorAll("[data-real-screen]"));
    const actualPreviewButtons = Array.from(document.querySelectorAll("[data-actual-preview]"));
    const modeButtons = Array.from(document.querySelectorAll("[data-demo-mode]"));
    const interactiveDemo = document.querySelector("[data-interactive-demo]");
    const actualDemo = document.querySelector("[data-actual-demo]");
    const interactiveTabs = document.querySelector("[data-interactive-tabs]");
    const actualTabs = document.querySelector("[data-actual-tabs]");
    const status = document.querySelector("[data-demo-status]");
    const note = document.querySelector("[data-demo-note]");
    const device = document.querySelector("[data-device]");
    const loading = document.querySelector("[data-demo-loading]");
    const quizAnswers = Array.from(document.querySelectorAll("[data-answer]"));
    const answerFeedback = document.querySelector("[data-answer-feedback]");
    const unsureLink = document.querySelector(".unsure-link");
    const recallAnswer = document.querySelector("[data-recall-answer]");
    const recallGrades = document.querySelector("[data-recall-grades]");
    const audioButtons = Array.from(document.querySelectorAll("[data-audio]"));
    const audioFiles = new Map(
      Array.from(document.querySelectorAll("[data-audio-file]")).map((audio) => [
        audio.dataset.audioFile,
        audio,
      ])
    );

    let activeMode = "interactive";
    let activeActualScreen = "home";

    const screenMessages = {
      home: "点击“学习”进入四选一，或从底部导航查看统计与我的",
      quiz: "选择一个释义，体验正确与错误反馈",
      recall: "根据真实记忆感受选择记得、模糊或忘记",
      books: "六本词书均可切换，每组词量也可以调整",
      result: "本组学习完成后，可以再学一组或返回首页",
      stats: "点击学习日历可展开更多日期",
      mine: "收藏、已掌握、学习中与未学习词表都可以继续打开",
      wordlist: "这是跨词书汇总词表的交互示意",
      info: "信息页支持从个人详情进入并原路返回",
    };

    const actualMessages = {
      home: "真实小程序首页 · 演示进度数据",
      quiz: "真实小程序四选一答题页",
      result: "真实小程序单词小结页 · 演示进度数据",
      stats: "真实小程序学习统计页 · 演示进度数据",
    };

    const announce = (message) => {
      if (status) status.textContent = message;
    };

    const initializeIcons = () => {
      if (window.lucide?.createIcons) {
        window.lucide.createIcons({ attrs: { "aria-hidden": "true" } });
      }
    };

    const stopAudio = () => {
      audioFiles.forEach((audio) => {
        audio.pause();
        audio.currentTime = 0;
      });
      audioButtons.forEach((button) => button.classList.remove("is-playing"));
    };

    const resetQuiz = () => {
      quizAnswers.forEach((button) => {
        button.disabled = false;
        button.classList.remove("is-correct", "is-wrong");
      });
      if (answerFeedback) answerFeedback.hidden = true;
      if (unsureLink) unsureLink.hidden = false;
    };

    const resetRecall = () => {
      if (recallAnswer) recallAnswer.hidden = true;
      if (recallGrades) recallGrades.hidden = false;
      document.querySelectorAll("[data-grade]").forEach((button) => {
        button.classList.remove("is-selected");
      });
    };

    const setScreen = (name, options = {}) => {
      const target = screens.find((screen) => screen.dataset.screen === name);
      if (!target) return;

      stopAudio();
      if (name === "quiz" && options.preserve !== true) resetQuiz();
      if (name === "recall" && options.preserve !== true) resetRecall();

      screens.forEach((screen) => {
        const active = screen === target;
        screen.classList.toggle("is-active", active);
        screen.setAttribute("aria-hidden", String(!active));
      });

      const previewName = ["wordlist", "info"].includes(name) ? "mine" : name;
      previewButtons.forEach((button) => {
        const active = button.dataset.preview === previewName;
        button.classList.toggle("is-active", active);
        button.setAttribute("aria-pressed", String(active));
      });

      announce(options.message || screenMessages[name] || "继续体验芽芽韩语");
    };

    const setActualScreen = (name) => {
      const target = actualScreens.find((screen) => screen.dataset.realScreen === name);
      if (!target) return;
      activeActualScreen = name;
      actualScreens.forEach((screen) => {
        const active = screen === target;
        screen.classList.toggle("is-active", active);
        screen.setAttribute("aria-hidden", String(!active));
      });
      actualPreviewButtons.forEach((button) => {
        const active = button.dataset.actualPreview === name;
        button.classList.toggle("is-active", active);
        button.setAttribute("aria-pressed", String(active));
      });
      announce(actualMessages[name]);
    };

    const setMode = (mode) => {
      activeMode = mode === "actual" ? "actual" : "interactive";
      const isActual = activeMode === "actual";
      if (interactiveDemo) interactiveDemo.hidden = isActual;
      if (actualDemo) actualDemo.hidden = !isActual;
      if (interactiveTabs) interactiveTabs.hidden = isActual;
      if (actualTabs) actualTabs.hidden = !isActual;
      modeButtons.forEach((button) => {
        const active = button.dataset.demoMode === activeMode;
        button.classList.toggle("is-active", active);
        button.setAttribute("aria-selected", String(active));
      });
      if (note) {
        note.textContent = isActual ? "小程序实际页面 · 演示进度数据" : "网页交互 Demo · 完整核心流程";
      }
      if (isActual) setActualScreen(activeActualScreen);
      else announce(screenMessages[document.querySelector("[data-screen].is-active")?.dataset.screen] || screenMessages.home);
    };

    document.querySelectorAll("[data-action]").forEach((button) => {
      button.addEventListener("click", () => setScreen(button.dataset.action));
    });

    previewButtons.forEach((button) => {
      button.setAttribute("aria-pressed", String(button.classList.contains("is-active")));
      button.addEventListener("click", () => {
        setMode("interactive");
        setScreen(button.dataset.preview);
      });
    });

    actualPreviewButtons.forEach((button) => {
      button.setAttribute("aria-pressed", String(button.classList.contains("is-active")));
      button.addEventListener("click", () => setActualScreen(button.dataset.actualPreview));
    });

    modeButtons.forEach((button) => {
      button.addEventListener("click", () => setMode(button.dataset.demoMode));
    });

    document.querySelectorAll("[data-start-demo]").forEach((button) => {
      button.addEventListener("click", () => {
        setMode("interactive");
        setScreen("quiz");
        device?.scrollIntoView({ behavior: "smooth", block: "center" });
      });
    });

    quizAnswers.forEach((button) => {
      button.addEventListener("click", () => {
        const correct = button.dataset.answer === "correct";
        const correctButton = quizAnswers.find((item) => item.dataset.answer === "correct");
        quizAnswers.forEach((item) => { item.disabled = true; });
        correctButton?.classList.add("is-correct");
        if (!correct) button.classList.add("is-wrong");
        if (answerFeedback) answerFeedback.hidden = false;
        if (unsureLink) unsureLink.hidden = true;
        announce(correct ? "回答正确，下一步进入主动回忆" : "已标出正确答案，可以继续进入主动回忆");
      });
    });

    const gradeMessages = {
      forgot: "忘记的词会回到本次学习队列",
      fuzzy: "模糊的词会缩短下次复习间隔",
      remembered: "记忆稳定，系统会延长下次复习间隔",
    };

    document.querySelectorAll("[data-grade]").forEach((button) => {
      button.addEventListener("click", () => {
        document.querySelectorAll("[data-grade]").forEach((item) => {
          item.classList.toggle("is-selected", item === button);
        });
        if (recallGrades) recallGrades.hidden = true;
        if (recallAnswer) recallAnswer.hidden = false;
        announce(gradeMessages[button.dataset.grade]);
      });
    });

    document.querySelector("[data-recall-reset]")?.addEventListener("click", () => {
      resetRecall();
      announce("已撤销本次判断，请重新选择记忆状态");
    });

    const favoriteButtons = Array.from(document.querySelectorAll("[data-favorite]"));
    favoriteButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const active = button.getAttribute("aria-pressed") !== "true";
        favoriteButtons.forEach((item) => {
          item.setAttribute("aria-pressed", String(active));
          item.classList.toggle("is-active", active);
        });
        announce(active ? "已加入我的收藏" : "已取消收藏");
      });
    });

    document.querySelectorAll("[data-known]").forEach((button) => {
      button.addEventListener("click", () => {
        const active = button.getAttribute("aria-pressed") !== "true";
        button.setAttribute("aria-pressed", String(active));
        button.classList.toggle("is-active", active);
        announce(active ? "已标记为掌握，本词将移出当前学习队列" : "已恢复到学习队列");
      });
    });

    const bookButtons = Array.from(document.querySelectorAll("[data-book]"));
    const updateBook = (button) => {
      const learned = Number(button.dataset.learned || 0);
      const total = Number(button.dataset.total || 1);
      const progress = Math.min(100, Math.max(0, (learned / total) * 100));

      document.querySelectorAll("[data-current-book]").forEach((element) => {
        element.textContent = button.dataset.name;
      });
      document.querySelectorAll("[data-current-learned]").forEach((element) => {
        element.textContent = learned.toLocaleString("zh-CN");
      });
      document.querySelectorAll("[data-current-total]").forEach((element) => {
        element.textContent = total.toLocaleString("zh-CN");
      });
      document.querySelectorAll("[data-current-progress]").forEach((element) => {
        element.style.width = `${progress.toFixed(1)}%`;
      });
      document.querySelectorAll("[data-current-book-icon]").forEach((element) => {
        element.className = `mini-book ${button.dataset.icon}`;
        const label = element.querySelector("span");
        if (label) label.textContent = button.dataset.label;
      });

      bookButtons.forEach((item) => {
        item.classList.toggle("is-current", item === button);
        let tag = item.querySelector(".current-tag");
        if (item === button && !tag) {
          tag = document.createElement("span");
          tag.className = "current-tag";
          tag.textContent = "正在学习";
          item.append(tag);
        }
      });
      announce(`已切换为${button.dataset.name}`);
    };

    bookButtons.forEach((button) => {
      button.addEventListener("click", () => {
        updateBook(button);
        window.setTimeout(() => setScreen("home", { preserve: true }), 260);
      });
    });

    document.querySelectorAll("[data-session-count]").forEach((button) => {
      button.addEventListener("click", () => {
        document.querySelectorAll("[data-session-count]").forEach((item) => {
          item.classList.toggle("is-active", item === button);
        });
        announce(`每组学习数量已设为 ${button.dataset.sessionCount} 词`);
      });
    });

    document.querySelector("[data-calendar-toggle]")?.addEventListener("click", (event) => {
      const button = event.currentTarget;
      const more = button.querySelector("[data-calendar-more]");
      const expanded = button.getAttribute("aria-expanded") === "true";
      button.setAttribute("aria-expanded", String(!expanded));
      if (more) more.hidden = expanded;
      announce(expanded ? "已收起学习日历" : "已展开完整学习周记录");
    });

    document.querySelectorAll("[data-list-title]").forEach((button) => {
      button.addEventListener("click", () => {
        const title = button.dataset.listTitle;
        const heading = document.querySelector("[data-word-list-title]");
        if (heading) heading.textContent = title;
        setScreen("wordlist", { message: `${title}包含用户自使用以来的跨词书累计记录` });
      });
    });

    document.querySelectorAll("[data-info-title]").forEach((button) => {
      button.addEventListener("click", () => {
        const title = button.dataset.infoTitle;
        document.querySelectorAll("[data-info-heading]").forEach((heading) => {
          heading.textContent = title;
        });
        const copy = document.querySelector("[data-info-copy]");
        if (copy) {
          copy.textContent = title === "数据管理"
            ? "学习记录优先保存在本地，登录后通过云端同步；清除操作需要再次确认。"
            : "芽芽韩语通过四选一、主动回忆和间隔复习，帮助学习者把眼熟变成真正想得起来。";
        }
        setScreen("info");
      });
    });

    audioButtons.forEach((button) => {
      const key = button.dataset.audio;
      const audio = audioFiles.get(key);
      if (!audio) {
        button.disabled = true;
        return;
      }
      audio.addEventListener("ended", () => button.classList.remove("is-playing"));
      audio.addEventListener("pause", () => button.classList.remove("is-playing"));
      button.addEventListener("click", async () => {
        const wasPlaying = !audio.paused;
        stopAudio();
        if (wasPlaying) {
          announce("发音已暂停");
          return;
        }
        button.classList.add("is-playing");
        try {
          await audio.play();
          announce("正在播放与小程序一致的韩语女声发音");
        } catch (error) {
          button.classList.remove("is-playing");
          announce("浏览器暂未允许播放，请再点击一次发音按钮");
        }
      });
    });

    const menuButton = document.querySelector("[data-menu-button]");
    const mobileNav = document.querySelector("[data-mobile-nav]");
    const closeMenu = () => {
      if (!menuButton || !mobileNav) return;
      menuButton.setAttribute("aria-expanded", "false");
      menuButton.setAttribute("aria-label", "打开导航");
      menuButton.setAttribute("title", "打开导航");
      mobileNav.hidden = true;
    };

    menuButton?.addEventListener("click", () => {
      if (!mobileNav) return;
      const open = menuButton.getAttribute("aria-expanded") === "true";
      menuButton.setAttribute("aria-expanded", String(!open));
      menuButton.setAttribute("aria-label", open ? "打开导航" : "关闭导航");
      menuButton.setAttribute("title", open ? "打开导航" : "关闭导航");
      mobileNav.hidden = open;
    });
    mobileNav?.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeMenu));
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeMenu();
    });

    const header = document.querySelector("[data-site-header]");
    const hero = document.querySelector(".hero");
    if (header && hero && "IntersectionObserver" in window) {
      const headerObserver = new IntersectionObserver(
        ([entry]) => header.classList.toggle("is-scrolled", !entry.isIntersecting),
        { rootMargin: "-68px 0px 0px", threshold: 0.05 }
      );
      headerObserver.observe(hero);
    }

    const revealItems = Array.from(document.querySelectorAll(".reveal"));
    if ("IntersectionObserver" in window) {
      const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      }, { rootMargin: "0px 0px -8%", threshold: 0.08 });
      revealItems.forEach((item) => revealObserver.observe(item));
    } else {
      revealItems.forEach((item) => item.classList.add("is-visible"));
    }

    document.querySelectorAll(".screenshot-rail img, [data-real-screen] img").forEach((image) => {
      image.addEventListener("error", () => image.closest("figure, section")?.classList.add("is-missing"));
    });

    initializeIcons();
    window.addEventListener("load", initializeIcons, { once: true });

    const finishLoading = () => {
      loading?.classList.add("is-hidden");
      window.setTimeout(() => loading?.remove(), 260);
    };
    if (document.readyState === "complete") finishLoading();
    else {
      window.addEventListener("load", finishLoading, { once: true });
      window.setTimeout(finishLoading, 900);
    }

    const query = new URLSearchParams(window.location.search);
    const requestedMode = query.get("mode") === "actual" ? "actual" : "interactive";
    const requestedScreen = query.get("screen");
    const requestedActualScreen = query.get("actual");

    setMode(requestedMode);
    if (requestedMode === "actual" && actualScreens.some((screen) => screen.dataset.realScreen === requestedActualScreen)) {
      setActualScreen(requestedActualScreen);
    } else if (screens.some((screen) => screen.dataset.screen === requestedScreen)) {
      setScreen(requestedScreen, { preserve: true });
    } else {
      setScreen("home", { preserve: true });
    }

    if (query.get("focus") === "1") {
      window.requestAnimationFrame(() => device?.scrollIntoView({ block: "center" }));
    }
  });
})();
