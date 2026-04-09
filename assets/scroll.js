window.addEventListener("DOMContentLoaded", function () {
  function initScrollSteps() {
    const steps = document.querySelectorAll(".story-step");

    if (!steps.length) {
      setTimeout(initScrollSteps, 300);
      return;
    }

    function getSectionElement(stepElement) {
      return stepElement.closest("[data-section]");
    }

    function showImageForStep(sectionElement, step) {
      if (!sectionElement) return;

      const frames = sectionElement.querySelectorAll(".section-graph-frame");
      frames.forEach((el) => el.classList.remove("active"));

      const target = sectionElement.querySelector(
        `.section-graph-frame[data-step="${step}"]`,
      );

      if (target) {
        target.classList.add("active");
      }
    }

    function setActiveStepInSection(sectionElement, activeStepElement) {
      if (!sectionElement) return;

      sectionElement
        .querySelectorAll(".story-step")
        .forEach((el) => el.classList.remove("active"));

      activeStepElement.classList.add("active");
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;

          const stepElement = entry.target;
          const step = stepElement.dataset.step;
          const sectionElement = getSectionElement(stepElement);

          setActiveStepInSection(sectionElement, stepElement);
          showImageForStep(sectionElement, step);

          const input = document.querySelector("#active-step-input");
          if (input) {
            const nativeSetter = Object.getOwnPropertyDescriptor(
              window.HTMLInputElement.prototype,
              "value",
            ).set;
            nativeSetter.call(input, step);
            input.dispatchEvent(new Event("input", { bubbles: true }));
            input.dispatchEvent(new Event("change", { bubbles: true }));
          }
        });
      },
      { threshold: 0.5 },
    );

    steps.forEach((stepEl) => observer.observe(stepEl));

    document.querySelectorAll("[data-section]").forEach((sectionElement) => {
      const firstStep = sectionElement.querySelector(".story-step");
      if (firstStep) {
        showImageForStep(sectionElement, firstStep.dataset.step);
      }
    });
  }

  initScrollSteps();
});
