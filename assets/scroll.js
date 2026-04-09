window.addEventListener("DOMContentLoaded", function () {
  function initScrollSteps() {
    const steps = document.querySelectorAll(".story-step");

    if (!steps.length) {
      setTimeout(initScrollSteps, 300);
      return;
    }

    function showImageForStep(step) {
    document.querySelectorAll("[id^='scatter-img-']").forEach((el) => {
        el.style.display = "none";
    });
    document.querySelectorAll("[id^='jitter-img-']").forEach((el) => {
        el.style.display = "none";
    });

    document.querySelectorAll("[id^='boxplot-img-']").forEach((el) => {
    el.style.display = "none";
    });

    document.querySelectorAll("[id^='barchart-img-']").forEach((el) => {
    el.style.display = "none";
  });

    const scatterTarget = document.getElementById(`scatter-img-${step}`);
    if (scatterTarget) scatterTarget.style.display = "block";

    const jitterTarget = document.getElementById(`jitter-img-${step}`);
    if (jitterTarget) jitterTarget.style.display = "block";

    const boxplotTarget = document.getElementById(`boxplot-img-${step}`);
    if (boxplotTarget) boxplotTarget.style.display = "block";

    const barchartTarget = document.getElementById(`barchart-img-${step}`);
    if (barchartTarget) barchartTarget.style.display = "block";

}

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            steps.forEach((el) => el.classList.remove("active"));
            entry.target.classList.add("active");

            const step = entry.target.dataset.step;
            showImageForStep(step);

            const input = document.querySelector("#active-step-input");
            if (input) {
              const nativeSetter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype,
                "value"
              ).set;
              nativeSetter.call(input, step);
              input.dispatchEvent(new Event("input", { bubbles: true }));
              input.dispatchEvent(new Event("change", { bubbles: true }));
            }
          }
        });
      },
      { threshold: 0.3 }
    );

    steps.forEach((stepEl) => observer.observe(stepEl));

    const firstStep = steps[0];
    if (firstStep) {
      showImageForStep(firstStep.dataset.step);
    }
  }

  initScrollSteps();
});