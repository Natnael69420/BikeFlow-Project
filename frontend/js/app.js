const API_BASE_URL = "http://127.0.0.1:5000/api";

/* ------------------------------
   Shared API functions
------------------------------ */

async function apiRequest(endpoint, options = {}) {
    let response;

    try {
        response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers: {
                "Content-Type": "application/json",
                ...options.headers
            }
        });
    } catch (error) {
        throw new Error(
            "Cannot connect to the BikeFlow backend. Check that the backend server is running."
        );
    }

    let data;

    try {
        data = await response.json();
    } catch (error) {
        throw new Error("The server returned an invalid response.");
    }

    if (!response.ok || data.success === false) {
        throw new Error(data.message || "Something went wrong.");
    }

    return data;
}

async function getOrders() {
    const data = await apiRequest("/orders");
    return data.orders || [];
}

async function getOrderById(id) {
    const data = await apiRequest(`/orders/${encodeURIComponent(id)}`);
    return data.order;
}

/* ------------------------------
   Shared display helpers
------------------------------ */

function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, character => {
        const entities = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;"
        };

        return entities[character];
    });
}

function getStatusClass(status) {
    const classes = {
        "Registered": "status-registered",
        "Scheduled": "status-scheduled",
        "In Progress": "status-in-progress",
        "Waiting for Parts": "status-waiting-for-parts",
        "Completed": "status-completed",
        "Cancelled": "status-cancelled"
    };

    return classes[status] || "";
}

function formatDate(dateValue) {
    if (!dateValue) {
        return "—";
    }

    const date = new Date(dateValue);

    if (Number.isNaN(date.getTime())) {
        return "—";
    }

    return date.toLocaleDateString();
}

/* ------------------------------
   Dashboard functions
------------------------------ */

function showDashboardMessage(message, type = "info") {
    const messageElement = document.getElementById("dashboard-message");

    if (!messageElement) {
        return;
    }

    messageElement.textContent = message;
    messageElement.className = `alert alert-${type}`;
}

function updateDashboardStats(orders) {
    const total = orders.length;

    const registered = orders.filter(
        order => order.status === "Registered"
    ).length;

    const inProgress = orders.filter(
        order => order.status === "In Progress"
    ).length;

    const completed = orders.filter(
        order => order.status === "Completed"
    ).length;

    document.getElementById("total-orders").textContent = total;
    document.getElementById("registered-orders").textContent = registered;
    document.getElementById("in-progress-orders").textContent = inProgress;
    document.getElementById("completed-orders").textContent = completed;
}

function displayRecentOrders(orders) {
    const tableBody = document.getElementById("recent-orders-table");

    if (!tableBody) {
        return;
    }

    if (orders.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="6">No repair orders found.</td>
            </tr>
        `;
        return;
    }

    const recentOrders = [...orders]
        .sort((a, b) => {
            return new Date(b.created_at || 0) -
                   new Date(a.created_at || 0);
        })
        .slice(0, 5);

    tableBody.innerHTML = recentOrders.map(order => {
        const bicycle = [
            order.bicycle_brand,
            order.bicycle_type
        ].filter(Boolean).join(" ");

        const statusClass = getStatusClass(order.status);

        return `
            <tr>
                <td>#${escapeHtml(order.id)}</td>
                <td>${escapeHtml(order.customer_name)}</td>
                <td>${escapeHtml(bicycle || "—")}</td>
                <td>
                    <span class="${statusClass}">
                        ${escapeHtml(order.status)}
                    </span>
                </td>
                <td>${escapeHtml(formatDate(order.created_at))}</td>
                <td>
                    <a href="order.html?id=${encodeURIComponent(order.id)}">
                        View
                    </a>
                </td>
            </tr>
        `;
    }).join("");
}

async function loadDashboard() {
    const tableBody = document.getElementById("recent-orders-table");

    if (!tableBody) {
        return;
    }

    try {
        showDashboardMessage("Loading repair orders...");

        const orders = await getOrders();

        updateDashboardStats(orders);
        displayRecentOrders(orders);

        showDashboardMessage(
            `Successfully loaded ${orders.length} repair order(s).`,
            "success"
        );

    } catch (error) {
        showDashboardMessage(error.message, "error");

        tableBody.innerHTML = `
            <tr>
                <td colspan="6">
                    Unable to load repair orders.
                </td>
            </tr>
        `;
    }
}

/* ------------------------------
   Initialize dashboard
------------------------------ */

document.addEventListener("DOMContentLoaded", () => {
    loadDashboard();
});

/* ------------------------------
   Make shared functions available
   to other frontend pages
------------------------------ */

window.BikeFlow = {
    API_BASE_URL,
    apiRequest,
    getOrders,
    getOrderById,
    escapeHtml,
    getStatusClass,
    formatDate
};
