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
    const status = document.querySelector("[data-demo-status]");
    const device = document.querySelector("[data-device]");
    const loading = document.querySelector("[data-demo-loading]");
    const quizAnswers = Array.from(document.querySelectorAll("[data-answer]"));
    const answerFeedback = document.querySelector("[data-answer-feedback]");
    const revealButton = document.querySelector("[data-reveal]");
    const recallAnswer = document.querySelector("[data-recall-answer]");
    const recallGrades = document.querySelector("[data-recall-grades]");
    const audioButtons = Array.from(document.querySelectorAll("[data-audio]"));
    const audioFiles = new Map(
      Array.from(document.querySelectorAll("[data-audio-file]")).map((audio) => [
        audio.dataset.audioFile,
        audio,
      ])
    );

    const screenMessages = {
      home: "点击手机里的“学习”开始",
      quiz: "选择“分析”，体验四选一识别",
      recall: "先在心里回忆，再查看答案",
      result: "这就是一次完整的短时学习闭环",
      books: "六本词书覆盖通用学习与 TOPIK 备考",
      stats: "累计学习统计跨词书保存",
    };

    const announce = (message) => {
      if (status) {
        status.textContent = message;
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
      if (answerFeedback) {
        answerFeedback.hidden = true;
      }
    };

    const resetRecall = () => {
      if (revealButton) {
        revealButton.hidden = false;
      }
      if (recallAnswer) {
        recallAnswer.hidden = true;
      }
      if (recallGrades) {
        recallGrades.hidden = true;
      }
      document.querySelectorAll("[data-grade]").forEach((button) => {
        button.classList.remove("is-selected");
      });
    };

    const setScreen = (name, options = {}) => {
      const target = screens.find((screen) => screen.dataset.screen === name);
      if (!target) {
        return;
      }

      stopAudio();
      if (name === "quiz" && options.preserve !== true) {
        resetQuiz();
      }
      if (name === "recall" && options.preserve !== true) {
        resetRecall();
      }

      screens.forEach((screen) => {
        const active = screen === target;
        screen.classList.toggle("is-active", active);
        screen.setAttribute("aria-hidden", String(!active));
      });

      const previewName = name === "recall" || name === "result" ? "quiz" : name;
      previewButtons.forEach((button) => {
        const active = button.dataset.preview === previewName;
        button.classList.toggle("is-active", active);
        button.setAttribute("aria-pressed", String(active));
      });

      announce(options.message || screenMessages[name] || "继续探索芽芽韩语");
    };

    document.querySelectorAll("[data-action]").forEach((button) => {
      button.addEventListener("click", () => setScreen(button.dataset.action));
    });

    previewButtons.forEach((button) => {
      button.setAttribute("aria-pressed", String(button.classList.contains("is-active")));
      button.addEventListener("click", () => setScreen(button.dataset.preview));
    });

    document.querySelectorAll("[data-start-demo]").forEach((button) => {
      button.addEventListener("click", () => {
        setScreen("quiz");
        device?.scrollIntoView({ behavior: "smooth", block: "center" });
      });
    });

    quizAnswers.forEach((button) => {
      button.addEventListener("click", () => {
        const correct = button.dataset.answer === "correct";
        const correctButton = quizAnswers.find((item) => item.dataset.answer === "correct");

        quizAnswers.forEach((item) => {
          item.disabled = true;
        });
        correctButton?.classList.add("is-correct");

        if (!correct) {
          button.classList.add("is-wrong");
          announce("这里容易混淆，正确答案是“分析”");
        } else {
          announce("答对了，接下来体验主动回忆");
        }

        if (answerFeedback) {
          answerFeedback.hidden = false;
        }
      });
    });

    revealButton?.addEventListener("click", () => {
      revealButton.hidden = true;
      if (recallAnswer) {
        recallAnswer.hidden = false;
      }
      if (recallGrades) {
        recallGrades.hidden = false;
      }
      announce("根据真实记忆感受选择一个结果");
    });

    const gradeMessages = {
      forgot: "已加入会话内重学，稍后再见一次",
      fuzzy: "已缩短复习间隔，巩固模糊记忆",
      remembered: "记忆稳定，系统会延长复习间隔",
    };

    document.querySelectorAll("[data-grade]").forEach((button) => {
      button.addEventListener("click", () => {
        document.querySelectorAll("[data-grade]").forEach((item) => {
          item.classList.toggle("is-selected", item === button);
        });
        window.setTimeout(() => {
          setScreen("result", { message: gradeMessages[button.dataset.grade] });
        }, 220);
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
          announce("正在播放真实韩语女声发音");
        } catch (error) {
          button.classList.remove("is-playing");
          announce("浏览器暂未允许播放，请再点一次发音按钮");
        }
      });
    });

    const copyText = async (value) => {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(value);
        return;
      }

      const field = document.createElement("textarea");
      field.value = value;
      field.setAttribute("readonly", "");
      field.style.position = "fixed";
      field.style.opacity = "0";
      document.body.appendChild(field);
      field.select();
      const copied = document.execCommand("copy");
      field.remove();
      if (!copied) {
        throw new Error("copy failed");
      }
    };

    document.querySelectorAll("[data-copy-name]").forEach((button) => {
      button.addEventListener("click", async () => {
        try {
          await copyText("芽芽韩语");
          document.querySelectorAll("[data-copy-status]").forEach((item) => {
            item.textContent = "已复制“芽芽韩语”，打开微信搜索即可";
          });
          announce("小程序名称已复制");
        } catch (error) {
          document.querySelectorAll("[data-copy-status]").forEach((item) => {
            item.textContent = "小程序名称：芽芽韩语";
          });
          announce("小程序名称：芽芽韩语");
        }
      });
    });

    const menuButton = document.querySelector("[data-menu-button]");
    const mobileNav = document.querySelector("[data-mobile-nav]");
    const closeMenu = () => {
      if (!menuButton || !mobileNav) {
        return;
      }
      menuButton.setAttribute("aria-expanded", "false");
      menuButton.setAttribute("aria-label", "打开导航");
      menuButton.setAttribute("title", "打开导航");
      mobileNav.hidden = true;
    };

    menuButton?.addEventListener("click", () => {
      if (!mobileNav) {
        return;
      }
      const open = menuButton.getAttribute("aria-expanded") === "true";
      menuButton.setAttribute("aria-expanded", String(!open));
      menuButton.setAttribute("aria-label", open ? "打开导航" : "关闭导航");
      menuButton.setAttribute("title", open ? "打开导航" : "关闭导航");
      mobileNav.hidden = open;
    });

    mobileNav?.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", closeMenu);
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        closeMenu();
      }
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
      const revealObserver = new IntersectionObserver(
        (entries, observer) => {
          entries.forEach((entry) => {
            if (!entry.isIntersecting) {
              return;
            }
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          });
        },
        { rootMargin: "0px 0px -8%", threshold: 0.08 }
      );
      revealItems.forEach((item) => revealObserver.observe(item));
    } else {
      revealItems.forEach((item) => item.classList.add("is-visible"));
    }

    document.querySelectorAll(".screenshot-rail img").forEach((image) => {
      image.addEventListener("error", () => {
        image.closest("figure")?.classList.add("is-missing");
      });
    });

    const initializeIcons = () => {
      if (window.lucide?.createIcons) {
        window.lucide.createIcons({ attrs: { "aria-hidden": "true" } });
      }
    };

    initializeIcons();
    window.addEventListener("load", initializeIcons, { once: true });

    const finishLoading = () => {
      loading?.classList.add("is-hidden");
      window.setTimeout(() => loading?.remove(), 260);
    };
    if (document.readyState === "complete") {
      finishLoading();
    } else {
      window.addEventListener("load", finishLoading, { once: true });
      window.setTimeout(finishLoading, 900);
    }

    const year = document.querySelector("[data-year]");
    if (year) {
      year.textContent = String(new Date().getFullYear());
    }

    setScreen("home", { preserve: true });
  });
})();
