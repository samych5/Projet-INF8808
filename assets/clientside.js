window.dash_clientside = Object.assign({}, window.dash_clientside, {
  clientside: {
    update_scatter: function (activeStep, figures, colX, colSymbol) {
      if (!figures || activeStep === undefined || activeStep === null) {
        return window.dash_clientside.no_update;
      }

      const stepKey = String(activeStep);

      if (!(stepKey in figures)) {
        return window.dash_clientside.no_update;
      }

      const stepFigures = figures[stepKey];

      if ("__default__" in stepFigures) {
        return stepFigures["__default__"];
      }

      if (!colX || !colSymbol) {
        return window.dash_clientside.no_update;
      }

      const comboKey = `${colX}|${colSymbol}`;

      if (!(comboKey in stepFigures)) {
        return window.dash_clientside.no_update;
      }

      return stepFigures[comboKey];
    },
  },
});
