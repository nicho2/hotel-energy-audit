import { env } from "@/lib/config/env";

function resolveFileName(contentDisposition: string | null, fallback: string) {
  if (!contentDisposition) {
    return fallback;
  }

  const utf8Match = contentDisposition.match(/filename\*=UTF-8''([^;]+)/i);
  if (utf8Match?.[1]) {
    return decodeURIComponent(utf8Match[1]);
  }

  const simpleMatch = contentDisposition.match(/filename="?([^"]+)"?/i);
  return simpleMatch?.[1] ?? fallback;
}

export async function downloadGeneratedReport(reportId: string, token: string, fallbackFileName: string) {
  const response = await fetch(`${env.apiBaseUrl}/api/v1/reports/${reportId}/download`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Telechargement impossible.");
  }

  const blob = await response.blob();
  const fileName = resolveFileName(response.headers.get("content-disposition"), fallbackFileName);
  const url = window.URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = fileName;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  window.URL.revokeObjectURL(url);
}
