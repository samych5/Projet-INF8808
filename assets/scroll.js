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
          }
        });
      },
      {
        threshold: 0.55,
      },
    );

    steps.forEach((step) => observer.observe(step));
  }

  initScrollSteps();
});
