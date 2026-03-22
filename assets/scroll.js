window.addEventListener("DOMContentLoaded", function () {
  function initScrollSteps() {
    const steps = document.querySelectorAll(".story-step");

    if (!steps.length) {
      setTimeout(initScrollSteps, 300);
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            steps.forEach((el) => el.classList.remove("active"));
            entry.target.classList.add("active");

            const step = entry.target.dataset.step;

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
          }
        });
      },
      {
        threshold: 0.55,
      },
    );

    steps.forEach((stepEl) => observer.observe(stepEl));
  }

  initScrollSteps();
});
