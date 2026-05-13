import os, re, json

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

# ─── İngilizce → Türkçe metin eşlemeleri (DOM'da otomatik değiştirilecek) ───
tr_map = [
    # Genel UI
    ("Generate Report",        "Rapor Oluştur"),
    ("Mission Control",        "Kontrol Merkezi"),
    ("Overview",               "Genel Bakış"),
    ("View All",               "Tümünü Gör"),
    ("Filter",                 "Filtrele"),
    ("Export",                 "Dışa Aktar"),
    ("Search",                 "Ara"),
    ("Save Changes",           "Değişiklikleri Kaydet"),
    ("Add New",                "Yeni Ekle"),
    # Dashboard
    ("Urgency Distribution",   "Aciliyet Dağılımı"),
    ("AI-classified active tickets across all channels.", "AI tarafından tüm kanallardan sınıflandırılmış aktif biletler."),
    ("Critical",               "Kritik"),
    ("High",                   "Yüksek"),
    ("Normal",                 "Normal"),
    ("Low",                    "Düşük"),
    ("Total",                  "Toplam"),
    ("AI System Status",       "AI Sistem Durumu"),
    ("Classification models are running optimally. Risk analysis latency is below threshold.", "Sınıflandırma modelleri optimum çalışıyor. Risk analiz gecikmesi eşiğin altında."),
    ("Uptime",                 "Çalışma Süresi"),
    ("Process Time",           "İşlem Süresi"),
    ("High Risk Return Detected",  "Yüksek Riskli İade Tespit Edildi"),
    ("Complaint Auto-Resolved",    "Şikayet Otomatik Çözüldü"),
    ("New Sentiment Alert",        "Yeni Duygu Analizi Uyarısı"),
    ("Expense Batch Processed",    "Masraf Toplu Olarak İşlendi"),
    ("Daily AI Summary Generated", "Günlük AI Özeti Oluşturuldu"),
    ("System automated report ready for review", "Sistem otomatik raporu incelemeye hazır"),
    ("Store: Kadıköy Branch | Trend: Negative", "Mağaza: Kadıköy Şubesi | Trend: Negatif"),
    ("ID: RET-8992 | AI Score: 0.92",           "ID: RET-8992 | AI Skoru: 0.92"),
    ("ID: CMP-4021 | Refund processed",         "ID: CMP-4021 | İade işlendi"),
    ("Batch ID: EXP-B-09 | 42 items",           "Toplu ID: EXP-B-09 | 42 kalem"),
    ("2 mins ago",   "2 dakika önce"),
    ("15 mins ago",  "15 dakika önce"),
    ("1 hour ago",   "1 saat önce"),
    ("3 hours ago",  "3 saat önce"),
    ("5 hours ago",  "5 saat önce"),
    ("Review Needed",   "İnceleme Gerekli"),
    ("Closed",          "Kapatıldı"),
    ("Monitor",         "İzle"),
    ("Logged",          "Kaydedildi"),
    ("System",          "Sistem"),
    ("Action Req",      "Aksiyon Gerekli"),
    # İadeler
    ("Order ID",         "Sipariş ID"),
    ("Reason",           "Sebep"),
    ("AI Kararı",        "AI Kararı"),
    ("AI Risk Skoru",    "AI Risk Skoru"),
    ("Actions",          "İşlemler"),
    ("Reject",           "Reddet"),
    ("Approve",          "Onayla"),
    ("Manual Review",    "Manuel İnceleme"),
    ("Item damaged upon arrival, box crushed.",   "Teslimat sırasında ürün hasar gördü, kutu ezilmiş."),
    ("Wrong size received, ordered M got L.",     "Yanlış beden geldi, M sipariş ettim L geldi."),
    ("Not as described in the pictures.",         "Fotoğraflardaki gibi değil."),
    ("Changed my mind, no longer needed.",        "Fikrim değişti, artık ihtiyacım yok."),
    ("Showing 1 to 4 of 24 entries",              "24 kayıttan 1-4 arası gösteriliyor"),
    # Şikayetler
    ("Gösterilen: 1 - 4 / 128 Kayıt",   "128 kayıttan 1-4 arası gösteriliyor"),
    ("Filtrele",   "Filtrele"),
    # Masraflar
    ("Drag & Drop Invoice Here",                  "Faturayı Buraya Sürükle & Bırak"),
    ("or click to browse files (PDF, JPG, PNG)",  "veya dosya seçmek için tıkla (PDF, JPG, PNG)"),
    ("Supplier Name",    "Tedarikçi Adı"),
    ("Amount (TL)",      "Tutar (TL)"),
    ("Date",             "Tarih"),
    ("Save and Send to AI",              "Kaydet ve AI'a Gönder"),
    ("Yeni Fatura / Masraf Girişi",      "Yeni Fatura / Masraf Ekle"),
    ("Upload or capture for AI extraction.", "Fatura yükle veya çek — AI verileri otomatik okur."),
    ("AI Processed",     "AI İşledi"),
    ("Pending Approval", "Onay Bekliyor"),
    # Store
    ("Store Name",       "Mağaza Adı"),
    ("Industry",         "Sektör"),
    ("Physical Address", "Fiziksel Adres"),
    ("WhatsApp Business Number", "WhatsApp İşletme Numarası"),
    ("Store Information",        "Mağaza Bilgileri"),
    ("Return Policy",            "İade Politikası"),
    ("Staff Management",         "Çalışan Yönetimi"),
    ("Notification Settings",    "Bildirim Ayarları"),
    ("Store Profile",            "Mağaza Profili"),
]

nav_js = """
<script>
const MOCK_USERS = {
  "patron@agentsync.com":  {pass:"patron123",  role:"patron"},
  "calisan@agentsync.com": {pass:"calisan123", role:"staff"}
};

// ──────────────────────────────────────────────────────────────────
// Türkçe çeviriler
// ──────────────────────────────────────────────────────────────────
const TR_MAP = """ + json.dumps([[a, b] for a, b in tr_map], ensure_ascii=False) + """;

function applyTranslations() {
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
  const nodes = [];
  let n;
  while ((n = walker.nextNode())) nodes.push(n);
  nodes.forEach(node => {
    TR_MAP.forEach(([en, tr]) => {
      if (node.nodeValue && node.nodeValue.includes(en)) {
        node.nodeValue = node.nodeValue.split(en).join(tr);
      }
    });
  });
  // placeholder attr çevirisi
  document.querySelectorAll("[placeholder]").forEach(el => {
    TR_MAP.forEach(([en, tr]) => {
      if (el.placeholder.includes(en)) el.placeholder = el.placeholder.split(en).join(tr);
    });
  });
}

// ──────────────────────────────────────────────────────────────────
// SPA Yönlendirici
// ──────────────────────────────────────────────────────────────────
function showPage(id) {
  document.querySelectorAll("[id^=page-]").forEach(el => el.style.display = "none");
  const el = document.getElementById("page-" + id);
  if (el) {
    el.style.display = "flex";
    window.dispatchEvent(new Event("resize"));
  }
  if (location.hash !== "#" + id) location.hash = id;
}

function setupNav(role) {
  const navItems = [
    { texts: ["dashboard", "panel"],                        id: "dashboard" },
    { texts: ["complaint", "şikayet"],                      id: "complaints" },
    { texts: ["return", "iade"],                            id: "returns" },
    { texts: ["expense", "masraf", "gider", "payments"],    id: "expenses" },
    { texts: ["store", "profil", "mağaza"],                 id: "store" }
  ];

  document.querySelectorAll("aside a, nav a").forEach(a => {
    const linkText = a.innerText.toLowerCase();
    const match = navItems.find(item => item.texts.some(t => linkText.includes(t)));
    if (!match) return;

    const targetId = match.id;
    a.setAttribute("data-nav", targetId);
    a.style.cursor = "pointer";
    a.href = "javascript:void(0)";

    if (role === "staff" && targetId === "store") {
      a.style.display = "none";
      if (a.parentElement && a.parentElement.tagName === "LI") a.parentElement.style.display = "none";
    }

    a.addEventListener("click", e => {
      e.preventDefault();
      showPage(targetId);
      document.querySelectorAll("[data-nav]").forEach(el => {
        el.classList.remove("text-on-primary-container", "bg-primary-container", "font-bold");
        el.classList.add("text-on-surface-variant");
      });
      document.querySelectorAll(`[data-nav='${targetId}']`).forEach(el => {
        el.classList.add("text-on-primary-container", "bg-primary-container", "font-bold");
        el.classList.remove("text-on-surface-variant");
      });
    });
  });
}

// ──────────────────────────────────────────────────────────────────
// Toast Bildirimi
// ──────────────────────────────────────────────────────────────────
function showToast(msg, type = "success") {
  const colors = { success: "#4cd6fb", error: "#ffb4ab", warn: "#ffb77d" };
  const icons  = { success: "check_circle", error: "error", warn: "warning" };
  const t = document.createElement("div");
  t.innerHTML = `<span class="material-symbols-outlined" style="font-size:20px">${icons[type]}</span><span>${msg}</span>`;
  Object.assign(t.style, {
    position:"fixed", bottom:"24px", right:"24px", zIndex:"9999",
    display:"flex", alignItems:"center", gap:"10px",
    background:"#1b2023", border:`1px solid ${colors[type]}33`,
    color: colors[type], padding:"14px 20px", borderRadius:"12px",
    fontFamily:"Inter,sans-serif", fontSize:"14px",
    boxShadow:"0 8px 32px rgba(0,0,0,0.4)",
    transform:"translateY(80px)", transition:"transform 0.35s ease, opacity 0.35s ease", opacity:"0"
  });
  document.body.appendChild(t);
  requestAnimationFrame(() => { t.style.transform = "translateY(0)"; t.style.opacity = "1"; });
  setTimeout(() => { t.style.opacity = "0"; t.style.transform = "translateY(80px)"; setTimeout(() => t.remove(), 400); }, 3000);
}

// ──────────────────────────────────────────────────────────────────
// Modal (onay diyaloğu)
// ──────────────────────────────────────────────────────────────────
function showModal(title, body, onConfirm) {
  const overlay = document.createElement("div");
  overlay.style.cssText = "position:fixed;inset:0;z-index:10000;background:rgba(0,0,0,0.7);backdrop-filter:blur(6px);display:flex;align-items:center;justify-content:center;";
  overlay.innerHTML = `
    <div style="background:#1b2023;border:1px solid rgba(76,214,251,0.2);border-radius:16px;padding:28px 32px;max-width:420px;width:90%;box-shadow:0 24px 64px rgba(0,0,0,0.6)">
      <h3 style="font-family:Outfit,sans-serif;font-size:20px;color:#dee3e6;margin:0 0 12px">${title}</h3>
      <p style="font-family:Inter,sans-serif;font-size:14px;color:#bcc9ce;margin:0 0 24px;line-height:1.6">${body}</p>
      <div style="display:flex;gap:12px;justify-content:flex-end">
        <button id="modal-cancel" style="padding:10px 20px;border-radius:8px;border:1px solid #3d494d;background:transparent;color:#bcc9ce;cursor:pointer;font-family:Inter,sans-serif;font-size:13px">İptal</button>
        <button id="modal-confirm" style="padding:10px 20px;border-radius:8px;border:none;background:#4cd6fb;color:#003642;cursor:pointer;font-family:Inter,sans-serif;font-size:13px;font-weight:600">Onayla</button>
      </div>
    </div>`;
  document.body.appendChild(overlay);
  overlay.querySelector("#modal-cancel").onclick  = () => overlay.remove();
  overlay.querySelector("#modal-confirm").onclick = () => { overlay.remove(); onConfirm(); };
  overlay.onclick = (e) => { if (e.target === overlay) overlay.remove(); };
}

// ──────────────────────────────────────────────────────────────────
// Buton İşlevselliği — tüm sayfalar
// ──────────────────────────────────────────────────────────────────
function setupButtons() {
  // ── GENEL: "Rapor Oluştur" butonları ──
  document.querySelectorAll("button").forEach(btn => {
    const t = btn.innerText.trim();

    // Rapor oluştur
    if (t.includes("Rapor Oluştur") || t.includes("Generate Report")) {
      btn.onclick = () => {
        showToast("Rapor hazırlanıyor… AI işliyor.", "success");
        setTimeout(() => showToast("Rapor hazır! PDF indiriliyor.", "success"), 2500);
      };
    }

    // Tümünü gör
    if (t.includes("Tümünü Gör") || t.includes("View All")) {
      btn.onclick = () => showPage("complaints");
    }

    // Filtrele
    if (t === "Filtrele" || t === "Filter") {
      btn.onclick = () => showToast("Filtre paneli yakında açılıyor.", "warn");
    }

    // Dışa aktar / Export
    if (t.includes("Dışa Aktar") || t.includes("Export")) {
      btn.onclick = () => {
        showToast("CSV dışa aktarılıyor…", "success");
        setTimeout(() => showToast("Dosya indirildi ✓", "success"), 1800);
      };
    }

    // Reddet (iade sayfası)
    if (t === "Reddet") {
      btn.onclick = () => {
        const row = btn.closest("tr");
        showModal("İadeyi Reddet", "Bu iade talebini reddetmek istediğinizden emin misiniz? İşlem geri alınamaz.", () => {
          if (row) row.style.opacity = "0.3";
          showToast("İade talebi reddedildi.", "error");
        });
      };
    }

    // Onayla (iade sayfası)
    if (t === "Onayla") {
      btn.onclick = () => {
        const row = btn.closest("tr");
        showModal("İadeyi Onayla", "Bu iade talebini onaylamak istiyor musunuz? Müşteriye otomatik bildirim gönderilecek.", () => {
          if (row) { row.style.opacity = "0.4"; row.style.textDecoration = "line-through"; }
          showToast("İade onaylandı! Müşteriye WhatsApp bildirimi gönderildi ✓", "success");
        });
      };
    }

    // Şikayet "Görüntüle"
    if (t === "Görüntüle") {
      btn.onclick = () => {
        const customerCell = btn.closest("tr")?.querySelector("td:first-child");
        const name = customerCell ? customerCell.innerText.trim() : "Müşteri";
        showModal(name + " — Şikayet Detayı",
          "AI Analizi: Şikayet yüksek öncelikli olarak sınıflandırıldı. Müşteri daha önce 2 kez benzer şikayet iletmiş. Otomatik yanıt hazır — onaylarsanız WhatsApp üzerinden gönderilebilir.",
          () => showToast("Yanıt müşteriye iletildi ✓", "success"));
      };
    }

    // Değişiklikleri Kaydet (Mağaza profili)
    if (t.includes("Değişiklikleri Kaydet") || t.includes("Save Changes")) {
      btn.onclick = () => showToast("Değişiklikler başarıyla kaydedildi ✓", "success");
    }

    // Yeni Ekle (Çalışan)
    if (t.includes("Yeni Ekle") || t.includes("Add New")) {
      btn.onclick = () => showToast("Yeni çalışan ekleme formu yakında açılacak.", "warn");
    }

    // Düzenle (kalem ikonu)
    if (btn.querySelector("span.material-symbols-outlined")?.innerText?.trim() === "edit") {
      btn.onclick = () => showToast("Düzenleme modu açıldı.", "warn");
    }

    // Sil (çöp ikonu)
    if (btn.querySelector("span.material-symbols-outlined")?.innerText?.trim() === "delete") {
      btn.onclick = () => showModal("Çalışanı Sil", "Bu çalışanı silmek istediğinizden emin misiniz?", () => {
        const card = btn.closest("[class*='flex items-center justify-between p-3']");
        if (card) card.remove();
        showToast("Çalışan silindi.", "error");
      });
    }

    // Kamera ile çek (masraflar)
    if (t.includes("Kamera ile Çek")) {
      btn.onclick = () => showToast("Kamera özelliği bu cihazda desteklenmiyor, lütfen dosya yükleyin.", "warn");
    }

    // Kaydet ve AI'a Gönder (masraflar)
    if (t.includes("Kaydet ve AI") || t.includes("Save and Send to AI")) {
      btn.onclick = () => {
        showToast("Fatura AI'a gönderildi, veriler işleniyor…", "success");
        setTimeout(() => showToast("AI okudu: Tutar ve tedarikçi bilgileri kaydedildi ✓", "success"), 2500);
      };
    }

    // Bildirim zili
    if (btn.querySelector("span.material-symbols-outlined")?.innerText?.trim() === "notifications") {
      btn.onclick = () => showToast("3 yeni bildirim var.", "warn");
    }

    // Ayarlar dişli
    if (btn.querySelector("span.material-symbols-outlined")?.innerText?.trim() === "settings") {
      btn.onclick = () => showToast("Ayarlar paneli yakında açılacak.", "warn");
    }

    // Sayfalama butonları
    if (btn.className.includes("rounded") && /^[0-9]+$/.test(t)) {
      btn.onclick = () => showToast(`Sayfa ${t} yükleniyor…`, "success");
    }
  });

  // ── Masraflar — Upload alanı ──
  document.querySelectorAll("[class*='border-dashed']").forEach(area => {
    area.style.cursor = "pointer";
    area.onclick = () => {
      const inp = document.createElement("input");
      inp.type = "file"; inp.accept = "application/pdf,image/*";
      inp.onchange = () => {
        if (inp.files[0]) showToast(`"${inp.files[0].name}" yüklendi. AI işliyor…`, "success");
      };
      inp.click();
    };
  });

  // ── Mağaza Profili — toggle ──
  document.querySelectorAll(".toggle-checkbox").forEach(cb => {
    cb.onchange = () => showToast(cb.checked ? "Bildirim aktif edildi ✓" : "Bildirim devre dışı bırakıldı.", cb.checked ? "success" : "warn");
  });

  // ── Arama kutuları ──
  document.querySelectorAll("input[type='text'], input[type='search']").forEach(inp => {
    if (!inp.getAttribute("data-search-bound")) {
      inp.setAttribute("data-search-bound", "1");
      inp.addEventListener("keydown", e => {
        if (e.key === "Enter" && inp.value.trim()) {
          showToast(`"${inp.value.trim()}" için sonuçlar filtreleniyor…`, "success");
        }
      });
    }
  });
}

// ──────────────────────────────────────────────────────────────────
// Hash Router
// ──────────────────────────────────────────────────────────────────
window.addEventListener("hashchange", () => {
  const id = location.hash.replace("#", "");
  if (id && document.getElementById("page-" + id)) {
    const saved = sessionStorage.getItem("agentsync_user");
    if (saved) showPage(id);
  }
});

// ──────────────────────────────────────────────────────────────────
// Başlangıç
// ──────────────────────────────────────────────────────────────────
window.addEventListener("DOMContentLoaded", () => {
  // Çevirileri uygula
  applyTranslations();

  // ── Login sayfası: sadece #page-login içindeki formu dinle ──
  function doLogin() {
    const emailEl = document.getElementById("email");
    const passEl  = document.getElementById("password");
    const email   = emailEl ? emailEl.value.trim() : "";
    const pass    = passEl  ? passEl.value          : "";
    const user    = MOCK_USERS[email];
    if (user && user.pass === pass) {
      sessionStorage.setItem("agentsync_user", JSON.stringify({email, role: user.role}));
      setupNav(user.role);
      setupButtons();
      showPage("dashboard");
    } else {
      showToast("Hatalı e-posta veya şifre!", "error");
      if (emailEl) { emailEl.style.border = "1px solid #ffb4ab"; setTimeout(() => emailEl.style.border = "", 2000); }
      if (passEl)  { passEl.style.border  = "1px solid #ffb4ab"; setTimeout(() => passEl.style.border  = "", 2000); }
    }
  }

  const loginPage = document.getElementById("page-login");
  if (loginPage) {
    const loginForm = loginPage.querySelector("form");
    if (loginForm) loginForm.addEventListener("submit", e => { e.preventDefault(); doLogin(); });

    // Giriş Yap butonuna direkt click desteği (type="submit" bazen SPA'da tetiklenmeyebilir)
    loginPage.querySelectorAll("button[type='submit'], button").forEach(btn => {
      if (btn.innerText.includes("Giriş") || btn.innerText.includes("Login")) {
        btn.addEventListener("click", e => { e.preventDefault(); doLogin(); });
      }
    });

    // Demo ipucu ekle
    if (loginForm) {
      const hint = document.createElement("div");
      hint.style.cssText = "margin-top:14px;padding:12px 16px;border-radius:10px;background:rgba(76,214,251,0.06);border:1px solid rgba(76,214,251,0.15);font-size:12px;color:#bcc9ce;font-family:JetBrains Mono,monospace;line-height:1.8";
      hint.innerHTML = "🔑 <b style='color:#4cd6fb'>Demo Giriş</b><br>Patron: patron@agentsync.com / patron123<br>Çalışan: calisan@agentsync.com / calisan123";
      loginForm.appendChild(hint);
    }
  }

  // Oturum varsa direkt yükle
  const saved = sessionStorage.getItem("agentsync_user");
  if (saved) {
    const u = JSON.parse(saved);
    setupNav(u.role);
    setupButtons();
    const initialHash = location.hash.replace("#", "");
    showPage(initialHash && document.getElementById("page-" + initialHash) ? initialHash : "dashboard");
  } else {
    showPage("login");
  }

  // Çıkış butonları
  document.querySelectorAll("[data-logout], button").forEach(btn => {
    if (btn.innerText.includes("Çıkış") || btn.innerText.includes("Logout")) {
      btn.onclick = () => {
        sessionStorage.removeItem("agentsync_user");
        showPage("login");
        location.hash = "";
      };
    }
  });
});
</script>
"""

parts = []
for key in ['login', 'dashboard', 'complaints', 'returns', 'expenses', 'store']:
    display = 'flex' if key == 'login' else 'none'
    cls = "w-full h-screen" + (" flex" if key != "login" else "")
    parts.append(f'<div id="page-{key}" class="{cls}" style="display:{display}">\n{bodies[key]}\n</div>')

html_out = """<!DOCTYPE html>
<html class="dark" lang="tr">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>AgentSync AI | Kontrol Merkezi</title>
{{SHARED_HEAD}}
</head>
<body class="bg-background text-on-background font-body-md antialiased">
{{PARTS}}
{{NAV_JS}}
</body>
</html>""".replace("{{SHARED_HEAD}}", shared_head).replace("{{PARTS}}", ''.join(parts)).replace("{{NAV_JS}}", nav_js)

os.makedirs('app/static', exist_ok=True)
with open('app/static/index.html', 'w', encoding='utf-8') as f:
    f.write(html_out)
print('Done! Bytes:', os.path.getsize('app/static/index.html'))
