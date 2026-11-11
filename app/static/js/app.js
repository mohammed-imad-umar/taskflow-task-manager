const themeToggle = document.getElementById("themeToggle");
const savedTheme = localStorage.getItem("taskflow-theme");
if (savedTheme === "dark") {
  document.body.classList.add("dark");
  if (themeToggle) themeToggle.textContent = "☀";
}
if (themeToggle) {
  themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark");
    const dark = document.body.classList.contains("dark");
    localStorage.setItem("taskflow-theme", dark ? "dark" : "light");
    themeToggle.textContent = dark ? "☀" : "☾";
  });
}
