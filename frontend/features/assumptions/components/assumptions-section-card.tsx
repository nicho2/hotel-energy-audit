"use client";

import type { AssumptionItem, AssumptionSection } from "@/types/assumptions";
import { useI18n } from "@/providers/i18n-provider";

type AssumptionsSectionCardProps = {
  section: AssumptionSection;
};

const sourceStyles = {
  configured: { color: "#166534", background: "#f0fdf4", border: "#bbf7d0" },
  defaulted: { color: "#92400e", background: "#fffbeb", border: "#fde68a" },
  calculated: { color: "#14365d", background: "#eff6ff", border: "#bfdbfe" },
};

function translateItemLabel(item: AssumptionItem, sectionKey: string, t: (key: string) => string) {
  const translated = t(`assumptions.items.${sectionKey}.${item.key}`);
  return translated.startsWith("[[") ? item.label : translated;
}

export function AssumptionsSectionCard({ section }: AssumptionsSectionCardProps) {
  const { t } = useI18n();
  const sectionTitle = t(`assumptions.sections.${section.key}`);

  return (
    <section style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "#fff", overflow: "hidden" }}>
      <div style={{ padding: "16px 20px", borderBottom: "1px solid #e5e7eb", display: "grid", gap: 4 }}>
        <h2 style={{ margin: 0, fontSize: 18, fontWeight: 700 }}>
          {sectionTitle.startsWith("[[") ? section.title : sectionTitle}
        </h2>
      </div>
      <div style={{ overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
          <tbody>
            {section.items.map((item) => {
              const badge = sourceStyles[item.source];
              return (
                <tr key={item.key}>
                  <th style={{ padding: "12px 16px", borderBottom: "1px solid #e5e7eb", textAlign: "left", width: "30%", color: "#334155" }}>
                    {translateItemLabel(item, section.key, t)}
                  </th>
                  <td style={{ padding: "12px 16px", borderBottom: "1px solid #e5e7eb", color: item.warning ? "#92400e" : "#142033" }}>
                    {item.value}
                    {item.note ? <div style={{ color: "#627084", fontSize: 12, marginTop: 4 }}>{item.note}</div> : null}
                  </td>
                  <td style={{ padding: "12px 16px", borderBottom: "1px solid #e5e7eb", textAlign: "right", whiteSpace: "nowrap" }}>
                    <span
                      style={{
                        display: "inline-flex",
                        padding: "4px 8px",
                        borderRadius: 8,
                        border: `1px solid ${badge.border}`,
                        color: badge.color,
                        background: badge.background,
                        fontSize: 12,
                        fontWeight: 700,
                      }}
                    >
                      {t(`assumptions.sources.${item.source}`)}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
}
