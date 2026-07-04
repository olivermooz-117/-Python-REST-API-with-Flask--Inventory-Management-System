const BASE_URL = "http://localhost:5000/inventory";

async function handleResponse(response, allow404 = false) {
  if (response.status === 404 && allow404) return null;
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.error || `Request failed with status ${response.status}`);
  }
  if (response.status === 204) return true;
  return response.json();
}

export async function getAllItems() {
  const response = await fetch(BASE_URL);
  return handleResponse(response);
}

export async function getItem(id) {
  const response = await fetch(`${BASE_URL}/${id}`);
  return handleResponse(response, true);
}

export async function createItem(data) {
  const response = await fetch(BASE_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return handleResponse(response);
}

export async function updateItem(id, data) {
  const response = await fetch(`${BASE_URL}/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return handleResponse(response, true);
}

export async function deleteItem(id) {
  const response = await fetch(`${BASE_URL}/${id}`, { method: "DELETE" });
  return handleResponse(response, true);
}

export async function lookupProduct({ barcode, name }) {
  const params = new URLSearchParams();
  if (barcode) params.set("barcode", barcode);
  if (name) params.set("name", name);

  const response = await fetch(`${BASE_URL}/lookup?${params.toString()}`);
  return handleResponse(response, true);
}

export async function addItemFromBarcode(barcode, extraFields = {}) {
  const response = await fetch(`${BASE_URL}/lookup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ barcode, ...extraFields }),
  });
  return handleResponse(response, true);
}