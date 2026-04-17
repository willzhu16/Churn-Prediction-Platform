function normalizeBaseUrl(url) {
  return url ? url.replace(/\/+$/, "") : "";
}

export function getApiBaseUrl() {
  const configuredUrl = normalizeBaseUrl(import.meta.env.VITE_API_URL);

  if (configuredUrl) {
    return configuredUrl;
  }

  if (typeof window !== "undefined") {
    const { hostname, protocol } = window.location;

    if (hostname === "localhost" || hostname === "127.0.0.1") {
      return `${protocol}//${hostname}:5050`;
    }
  }

  return "";
}

export async function fetchJson(path, options) {
  const baseUrl = getApiBaseUrl();
  const url = `${baseUrl}${path}`;
  const response = await fetch(url, options);
  const contentType = response.headers.get("content-type") || "";

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status} for ${url}`);
  }

  if (!contentType.includes("application/json")) {
    const bodyPreview = (await response.text()).slice(0, 120);
    throw new Error(
      `Expected JSON from ${url}, but received ${contentType || "unknown content type"}: ${bodyPreview}`
    );
  }

  return response.json();
}
