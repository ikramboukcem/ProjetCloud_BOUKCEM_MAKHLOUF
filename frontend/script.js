const API_BASE = "http://localhost:3000"; // URL API de Meriem

// Navigation SPA
function showSection(section) {
    document.getElementById("uploadSection").classList.add("d-none");
    document.getElementById("statusSection").classList.add("d-none");
    document.getElementById("metadataSection").classList.add("d-none");

    if (section === "upload") document.getElementById("uploadSection").classList.remove("d-none");
    if (section === "status") document.getElementById("statusSection").classList.remove("d-none");
    if (section === "metadata") document.getElementById("metadataSection").classList.remove("d-none");
}

// 🔵 UPLOAD PAR URL
async function uploadFromUrl() {
    const url = document.getElementById("fileUrl").value;

    if (!url.trim()) {
        showAlert("uploadMessage", "danger", "Veuillez entrer une URL.");
        return;
    }

    showAlert("uploadMessage", "info", "⏳ Chargement...");

    // Appelle l'API de Meriem : /upload-url?url=
    const res = await fetch(`${API_BASE}/upload-url?url=${encodeURIComponent(url)}`);
    const data = await res.json();

    if (data.error) {
        showAlert("uploadMessage", "danger", "❌ Erreur : " + data.error);
        return;
    }

    showAlert("uploadMessage", "success", `✅ Fichier envoyé ! ID : <b>${data.documentId}</b>`);
}

// 🔵 STATUT
async function checkStatus() {
    const id = document.getElementById("statusId").value;
    if (!id.trim()) return showAlert("statusMessage", "danger", "Veuillez entrer un ID.");

    showAlert("statusMessage", "info", "⏳ Vérification...");

    const res = await fetch(`${API_BASE}/status/${id}`);
    const data = await res.json();

    showAlert("statusMessage", "secondary", `📌 Statut : <span class="badge bg-primary">${data.status}</span>`);
}

// 🔵 METADONNEES
async function getMetadata() {
    const id = document.getElementById("metaId").value;
    if (!id.trim()) return;

    const res = await fetch(`${API_BASE}/metadata/${id}`);
    const data = await res.json();

    if (data.error) {
        document.getElementById("metaTable").innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
        return;
    }

    let html = `
        <table class="table table-bordered table-striped">
            <tr><th>Nom</th><td>${data.name}</td></tr>
            <tr><th>Type</th><td>${data.type}</td></tr>
            <tr><th>Taille</th><td>${data.size}</td></tr>
            <tr><th>Date</th><td>${data.date}</td></tr>
            <tr><th>Statut</th><td>${data.status}</td></tr>
        </table>
    `;

    document.getElementById("metaTable").innerHTML = html;
}

// 🟢 AFFICHER UNE ALERTE BOOTSTRAP
function showAlert(elementId, type, message) {
    document.getElementById(elementId).innerHTML =
        `<div class="alert alert-${type}">${message}</div>`;
}
