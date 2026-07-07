document.addEventListener('DOMContentLoaded', () => {
  // Demo interactivity for the Arc web-app
  const themeToggle = document.getElementById('themeToggle');
  const showToast = document.getElementById('showToast');
  const repoInfo = document.getElementById('repoInfo');
  const contactForm = document.getElementById('contactForm');

  // Theme toggle
  function isDark() { return document.documentElement.classList.contains('dark'); }
  function setDark(d) { document.documentElement.classList.toggle('dark', d); }
  if (themeToggle) {
    themeToggle.addEventListener('click', () => setDark(!isDark()));
  }

  // Simple toast-like action: fetch basic repo info from GitHub public API
  if (showToast && repoInfo) {
    showToast.addEventListener('click', async () => {
      const meta = document.querySelector('meta[name=repo]');
      if (!meta) { repoInfo.textContent = 'Repository meta tag not found.'; return; }
      const repo = meta.content;
      repoInfo.textContent = 'Loading repository info for ' + repo + ' ...';
      try {
        const res = await fetch(`https://api.github.com/repos/${repo}`);
        if (!res.ok) throw new Error(res.status + ' ' + res.statusText);
        const data = await res.json();
        const out = {
          name: data.full_name,
          description: data.description,
          stars: data.stargazers_count,
          forks: data.forks_count,
          open_issues: data.open_issues_count,
          url: data.html_url
        };
        repoInfo.textContent = JSON.stringify(out, null, 2);
      } catch (err) {
        repoInfo.textContent = 'Failed to fetch repo info: ' + err.message;
      }
    });
  }

  // Contact form client-side demo
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const form = new FormData(contactForm);
      const name = form.get('name');
      const email = form.get('email');
      const message = form.get('message');
      if (!name || !email || !message) {
        alert('Please fill all fields.');
        return;
      }
      // Demo behavior: show a message and clear form
      alert('Thanks, ' + name + '! This is a demo form and will not send data anywhere.');
      contactForm.reset();
    });
  }
});
