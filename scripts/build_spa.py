import os, re

base = r'stitch_agentsync_ai_admin_dashboard\stitch_agentsync_ai_admin_dashboard'
pages = {
    'login':      'giri_yap_agentsync_ai',
    'dashboard':  'dashboard_agentsync_ai',
    'returns':    'i_ade_talepleri_agentsync_ai',
    'complaints': 'ikayetler_agentsync_ai',
    'expenses':   'masraflar_agentsync_ai',
    'store':      'ma_aza_profili_agentsync_ai',
}

bodies = {}
for key, folder in pages.items():
    with open(os.path.join(base, folder, 'code.html'), 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()
    m = re.search(r'<body[^>]*>(.*)</body>', html, re.DOTALL)
    bodies[key] = m.group(1).strip() if m else ''

# Shared head from dashboard (has full Tailwind config + fonts)
with open(os.path.join(base, 'dashboard_agentsync_ai', 'code.html'), 'r', encoding='utf-8', errors='replace') as f:
    dash_html = f.read()
head_m = re.search(r'<head>(.*)</head>', dash_html, re.DOTALL)
shared_head = head_m.group(1).strip() if head_m else ''

nav_js = """
<script>
const MOCK_USERS = {
  "patron@agentsync.com":  {pass:"patron123",  role:"patron"},
  "calisan@agentsync.com": {pass:"calisan123", role:"staff"}
};

function showPage(id) {
  document.querySelectorAll("[id^=page-]").forEach(el => el.style.display = "none");
  const el = document.getElementById("page-" + id);
  if (el) { el.style.display = "flex"; }
}

function setupNav(role) {
  const navItems = [
    { texts: ["dashboard", "panel"], id: "dashboard" },
    { texts: ["complaint", "şikayet"], id: "complaints" },
    { texts: ["return", "iade"], id: "returns" },
    { texts: ["expense", "masraf", "gider", "payments"], id: "expenses" },
    { texts: ["store", "profil", "mağaza"], id: "store" }
  ];

  console.log("Setting up nav for role:", role);
  const links = document.querySelectorAll("aside a");
  
  links.forEach(a => {
    const linkText = a.innerText.toLowerCase();
    const match = navItems.find(item => item.texts.some(t => linkText.includes(t)));
    
    if (match) {
      const targetId = match.id;
      a.setAttribute("data-nav", targetId);
      a.href = "javascript:void(0)";
      
      // Staff kısıtlaması
      if (role === "staff" && targetId === "store") {
        a.style.display = "none";
        if (a.parentElement && a.parentElement.tagName === "LI") a.parentElement.style.display = "none";
      }

      a.addEventListener("click", e => {
        e.preventDefault();
        console.log("Navigating to:", targetId);
        showPage(targetId);
        
        // Aktiflik durumunu güncelle
        document.querySelectorAll("[data-nav]").forEach(el => {
          el.classList.remove("text-on-primary-container","bg-primary-container","font-bold");
          el.classList.add("text-on-surface-variant");
        });
        document.querySelectorAll("[data-nav='" + targetId + "']").forEach(el => {
          el.classList.add("text-on-primary-container","bg-primary-container","font-bold");
          el.classList.remove("text-on-surface-variant");
        });
      });
    }
  });
}

window.addEventListener("DOMContentLoaded", () => {
  // Login form submit
  document.querySelectorAll("form").forEach(form => {
    form.addEventListener("submit", e => {
      e.preventDefault();
      const email = (form.querySelector("#email") || {}).value || "";
      const pass  = (form.querySelector("#password") || {}).value || "";
      const user  = MOCK_USERS[email.trim()];
      if (user && user.pass === pass) {
        sessionStorage.setItem("agentsync_user", JSON.stringify({email, role: user.role}));
        setupNav(user.role);
        showPage("dashboard");
      } else {
        alert("Hatalı e-posta veya şifre! \\n\\nPatron: patron@agentsync.com / patron123\\nÇalışan: calisan@agentsync.com / calisan123");
      }
    });
  });

  // Auto-login if session exists
  const saved = sessionStorage.getItem("agentsync_user");
  if (saved) {
    const u = JSON.parse(saved);
    setupNav(u.role);
    showPage("dashboard");
  } else {
    showPage("login");
  }
});
</script>
"""

parts = []
for key in ['login','dashboard','complaints','returns','expenses','store']:
    display = 'flex' if key == 'login' else 'none'
    # Login haricindekiler yan yana sidebar düzeni için flex olmalı
    cls = "w-full h-screen" + (" flex" if key != "login" else "")
    parts.append(f'<div id="page-{key}" class="{cls}" style="display:{display}">\n{bodies[key]}\n</div>')

html_out = f"""<!DOCTYPE html>
<html class="dark" lang="tr">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>AgentSync AI | Mission Control</title>
{shared_head}
</head>
<body class="bg-background text-on-background font-body-md antialiased">
{''.join(parts)}
{nav_js}
</body>
</html>"""

os.makedirs('app/static', exist_ok=True)
with open('app/static/index.html', 'w', encoding='utf-8') as f:
    f.write(html_out)
print('Done! Bytes:', os.path.getsize('app/static/index.html'))
