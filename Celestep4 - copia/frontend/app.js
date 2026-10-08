const API_URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", () => {
    cargarCapitulos();
    cargarSecretos();

    document.getElementById("secreto-form").addEventListener("submit", (e) => {
        e.preventDefault();
        guardarSecreto();
    });
});

async function cargarCapitulos() {
    try {
        const res = await fetch(`${API_URL}/capitulos`);
        const capitulos = await res.json();
        const select = document.getElementById("capitulo_id");
        select.innerHTML = "";
        capitulos.forEach(cap => {
            select.innerHTML += `<option value="${cap.id}">Ch. ${cap.numero} - ${cap.nombre}</option>`;
        });
    } catch (err) {
        console.error("Error cargando capítulos:", err);
    }
}

async function cargarSecretos() {
    try {
        const res = await fetch(`${API_URL}/secretos`);
        const secretos = await res.json();
        const tbody = document.getElementById("secretos-tabla");
        tbody.innerHTML = "";

        if(secretos.length === 0) {
            tbody.innerHTML = `<tr><td colspan="6" class="text-center text-muted p-4">No hay secretos registrados aún.</td></tr>`;
            return;
        }

        secretos.forEach(sec => {
            let badgeClass = "badge-fresa";
            if (sec.tipo_coleccionable === "Casete") badgeClass = "badge-casete";
            if (sec.tipo_coleccionable === "Corazon") badgeClass = "badge-corazon";

            tbody.innerHTML += `
                <tr>
                    <td class="fw-bold text-nowrap">${sec.capitulo_nombre}</td>
                    <td>${sec.nombre}</td>
                    <td><span class="badge ${badgeClass}">${sec.tipo_coleccionable}</span></td>
                    <td class="text-center fw-bold text-warning">${sec.lado}</td>
                    <td><small>${sec.ubicacion_detalles}</small></td>
                    <td class="text-nowrap">
                        <button class="btn btn-sm btn-warning me-1" onclick="prepararEdicion(${sec.id})">✏️</button>
                        <button class="btn btn-sm btn-danger" onclick="eliminarSecreto(${sec.id})">🗑️</button>
                    </td>
                </tr>
            `;
        });
    } catch (err) {
        console.error("Error cargando secretos:", err);
    }
}

async function guardarSecreto() {
    const id = document.getElementById("secreto-id").value;
    const datos = {
        capitulo_id: parseInt(document.getElementById("capitulo_id").value),
        nombre: document.getElementById("nombre").value,
        tipo_coleccionable: document.getElementById("tipo_coleccionable").value,
        lado: document.getElementById("lado").value,
        ubicacion_detalles: document.getElementById("ubicacion_detalles").value
    };

    const metodo = id ? "PUT" : "POST";
    const url = id ? `${API_URL}/secretos/${id}` : `${API_URL}/secretos`;

    try {
        const res = await fetch(url, {
            method: metodo,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(datos)
        });

        if (res.ok) {
            resetForm();
            cargarSecretos();
        } else {
            const errData = await res.json();
            alert("Error: " + errData.detail);
        }
    } catch (err) {
        console.error("Error al guardar:", err);
    }
}

async function prepararEdicion(id) {
    try {
        const res = await fetch(`${API_URL}/secretos/${id}`);
        const sec = await res.json();

        document.getElementById("secreto-id").value = sec.id;
        document.getElementById("capitulo_id").value = sec.capitulo_id;
        document.getElementById("nombre").value = sec.nombre;
        document.getElementById("tipo_coleccionable").value = sec.tipo_coleccionable;
        document.getElementById("lado").value = sec.lado;
        document.getElementById("ubicacion_detalles").value = sec.ubicacion_detalles;

        document.getElementById("form-title").innerText = "Editar Secreto Seleccionado";
        document.getElementById("btn-submit").className = "btn btn-warning w-100 fw-bold";
        document.getElementById("btn-cancel").classList.remove("d-none");
    } catch (err) {
        console.error("Error al obtener secreto:", err);
    }
}

async function eliminarSecreto(id) {
    if (!confirm("¿Seguro que quieres borrar este secreto del archivo de Celeste?")) return;

    try {
        const res = await fetch(`${API_URL}/secretos/${id}`, { method: "DELETE" });
        if (res.ok) {
            cargarSecretos();
        }
    } catch (err) {
        console.error("Error al eliminar:", err);
    }
}

function resetForm() {
    document.getElementById("secreto-id").value = "";
    document.getElementById("secreto-form").reset();
    document.getElementById("form-title").innerText = "Registrar Secreto / Coleccionable";
    document.getElementById("btn-submit").className = "btn btn-danger w-100 fw-bold";
    document.getElementById("btn-cancel").className = "btn btn-secondary w-100 fw-bold mt-2 d-none";
}