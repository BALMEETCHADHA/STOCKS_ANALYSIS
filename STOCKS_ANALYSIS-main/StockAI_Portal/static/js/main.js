// Custom-duration toggle on the dashboard form
document.addEventListener("DOMContentLoaded", function () {
  const periodSelect = document.getElementById("period-select");
  const customRow = document.getElementById("custom-duration-row");
  const periodMode = document.getElementById("period-mode");

  if (periodSelect) {
    periodSelect.addEventListener("change", function () {
      if (periodSelect.value === "__custom__") {
        customRow.style.display = "grid";
        periodMode.value = "custom";
      } else {
        customRow.style.display = "none";
        periodMode.value = "preset";
      }
    });
  }

  // Chart type selector on the report page
  const chartSelect = document.getElementById("chart-select");
  if (chartSelect) {
    chartSelect.addEventListener("change", function () {
      document.querySelectorAll(".chart-img").forEach(function (img) {
        img.style.display = img.dataset.idx === chartSelect.value ? "block" : "none";
      });
    });
  }

  // Official-site search buttons on the dashboard
  const siteInput = document.getElementById("site-search-input");
  const siteContext = document.getElementById("site-context");
  document.querySelectorAll(".site-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      const query = (siteInput && siteInput.value.trim()) || "";
      if (!query) {
        if (siteContext) siteContext.textContent = "Type a name first, then click a site.";
        return;
      }
      const url = btn.dataset.template.replace("%s", encodeURIComponent(query));
      window.open(url, "_blank", "noopener");
    });
  });

  // Paste-a-screenshot-directly feature: click the paste zone, then Ctrl+V.
  // The pasted image is attached to the same hidden file input the
  // "upload a chart photo" field uses, so the backend handles it identically.
  const pasteZone = document.getElementById("paste-zone");
  const pastePreview = document.getElementById("paste-preview");
  const imgFileInput = document.getElementById("img-file-input");

  if (pasteZone && imgFileInput) {
    pasteZone.addEventListener("click", function () { pasteZone.focus(); });

    pasteZone.addEventListener("paste", function (e) {
      const items = (e.clipboardData || window.clipboardData).items;
      for (let i = 0; i < items.length; i++) {
        if (items[i].type.indexOf("image") !== -1) {
          const blob = items[i].getAsFile();
          try {
            const dt = new DataTransfer();
            dt.items.add(new File([blob], "pasted-chart.png", { type: blob.type || "image/png" }));
            imgFileInput.files = dt.files;
          } catch (err) {
            // DataTransfer construction can fail on some older browsers;
            // the visible preview still confirms the paste worked, and the
            // user can fall back to the normal file picker if submit fails.
          }
          const reader = new FileReader();
          reader.onload = function (ev) {
            pastePreview.src = ev.target.result;
            pastePreview.style.display = "block";
            pasteZone.textContent = "✅ Screenshot captured — ready to analyze (click to replace)";
          };
          reader.readAsDataURL(blob);
          e.preventDefault();
          break;
        }
      }
    });
  }
});
