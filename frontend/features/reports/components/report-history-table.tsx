"use client";

import { formatCurrency } from "@/features/results/utils/formatters";
import type { GeneratedReportResponse } from "@/types/reports";

function formatDate(value: string) {
  return new Intl.DateTimeFormat("fr-FR", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function formatFileSize(bytes: number) {
  if (bytes < 1024) {
    return `${bytes} B`;
  }

  if (bytes < 1024 * 1024) {
    return `${(bytes / 1024).toFixed(1)} KB`;
  }

  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function getStatusBadgeStyle(status: string) {
  if (status === "generated") {
    return { color: "#166534", background: "#dcfce7", border: "#bbf7d0" };
  }
  if (status === "failed") {
    return { color: "#b91c1c", background: "#fee2e2", border: "#fecaca" };
  }
  return { color: "#92400e", background: "#fef3c7", border: "#fde68a" };
}

type ReportHistoryTableProps = {
  reports: GeneratedReportResponse[];
  scenarioNames: Map<string, string>;
  onDownload: (report: GeneratedReportResponse) => void;
  isDownloadingReportId: string | null;
};

export function ReportHistoryTable({
  reports,
  scenarioNames,
  onDownload,
  isDownloadingReportId,
}: ReportHistoryTableProps) {
  return (
    <section style={{ border: "1px solid #e5e7eb", borderRadius: 16, overflow: "hidden" }}>
      <div style={{ padding: 20, borderBottom: "1px solid #e5e7eb", display: "grid", gap: 4 }}>
        <div style={{ fontSize: 20, fontWeight: 700 }}>Report history</div>
        <div style={{ color: "#627084", fontSize: 14 }}>Historique des PDF deja generes pour ce projet.</div>
      </div>

      {reports.length === 0 ? (
        <div style={{ padding: 24, color: "#627084" }}>Aucun rapport genere pour le moment.</div>
      ) : (
        <div style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ background: "#f8fafc", textAlign: "left" }}>
                {["Title", "Scenario", "Type", "Status", "Created", "Size", "Actions"].map((label) => (
                  <th key={label} style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb", fontSize: 13, fontWeight: 700 }}>
                    {label}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {reports.map((report) => {
                const badge = getStatusBadgeStyle(report.status);
                return (
                  <tr key={report.id}>
                    <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>
                      <div style={{ display: "grid", gap: 4 }}>
                        <div style={{ fontWeight: 700 }}>{report.title}</div>
                        <div style={{ fontSize: 13, color: "#627084" }}>{report.file_name}</div>
                      </div>
                    </td>
                    <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>
                      {scenarioNames.get(report.scenario_id) ?? report.scenario_id}
                    </td>
                    <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>{report.report_type}</td>
                    <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>
                      <span
                        style={{
                          display: "inline-flex",
                          padding: "4px 8px",
                          borderRadius: 999,
                          border: `1px solid ${badge.border}`,
                          color: badge.color,
                          background: badge.background,
                          fontSize: 12,
                          fontWeight: 700,
                          textTransform: "uppercase",
                        }}
                      >
                        {report.status}
                      </span>
                    </td>
                    <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>{formatDate(report.created_at)}</td>
                    <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>{formatFileSize(report.file_size_bytes)}</td>
                    <td style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>
                      <button
                        type="button"
                        onClick={() => onDownload(report)}
                        disabled={report.status !== "generated" || isDownloadingReportId === report.id}
                        style={{
                          borderRadius: 8,
                          border: "1px solid #14365d",
                          background: report.status === "generated" ? "#14365d" : "#e5e7eb",
                          color: report.status === "generated" ? "#fff" : "#627084",
                          padding: "8px 12px",
                          fontWeight: 700,
                          cursor: report.status === "generated" ? "pointer" : "not-allowed",
                        }}
                      >
                        {isDownloadingReportId === report.id ? "Telechargement..." : "Telecharger"}
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
