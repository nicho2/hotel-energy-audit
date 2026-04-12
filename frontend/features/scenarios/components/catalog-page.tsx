"use client";

import { useMemo, useState } from "react";
import { FeedbackBlock } from "@/components/ui/feedback";
import { useCountryProfiles } from "@/features/reference-data/hooks/use-country-profiles";
import { useI18n } from "@/providers/i18n-provider";
import type { SolutionCatalogItem } from "@/types/scenarios";
import { useSolutionCatalog } from "../hooks/use-solution-catalog";

const inputStyle = {
  width: "100%",
  borderRadius: 8,
  border: "1px solid #d1d5db",
  padding: "10px 12px",
  fontSize: 14,
  background: "#fff",
} as const;

const familyFallbacks = ["bacs", "hvac", "lighting", "dhw", "envelope", "optimization"];
const buildingTypes = ["hotel", "aparthotel", "residence", "other_accommodation"];

function formatMoney(value: number | null | undefined) {
  if (value === null || value === undefined) {
    return "-";
  }

  return new Intl.NumberFormat("fr-FR", {
    style: "currency",
    currency: "EUR",
    maximumFractionDigits: 0,
  }).format(value);
}

function getBacsImpactLabel(item: SolutionCatalogItem, neutralLabel: string) {
  const keys = Object.keys(item.bacs_impact_json ?? {});
  if (keys.length === 0) {
    return neutralLabel;
  }

  return keys.slice(0, 3).join(", ");
}

function matchesSearch(item: SolutionCatalogItem, search: string) {
  const normalized = search.trim().toLocaleLowerCase();
  if (!normalized) {
    return true;
  }

  return [item.code, item.name, item.description, item.solution_family, item.offer_reference ?? ""]
    .join(" ")
    .toLocaleLowerCase()
    .includes(normalized);
}

export function CatalogPage() {
  const { t, language } = useI18n();
  const countries = useCountryProfiles();
  const [search, setSearch] = useState("");
  const [country, setCountry] = useState("");
  const [family, setFamily] = useState("");
  const [buildingType, setBuildingType] = useState("");
  const [scope, setScope] = useState("");
  const catalog = useSolutionCatalog({
    country: country || undefined,
    family: family || undefined,
    building_type: buildingType || undefined,
    scope: scope || undefined,
  });

  const solutions = catalog.data?.data ?? [];
  const visibleSolutions = useMemo(
    () => solutions.filter((item) => matchesSearch(item, search)),
    [search, solutions],
  );
  const families = useMemo(
    () => Array.from(new Set([...familyFallbacks, ...solutions.map((item) => item.solution_family)])).sort(),
    [solutions],
  );
  const familyStats = useMemo(() => {
    const counts = new Map<string, number>();
    for (const item of visibleSolutions) {
      counts.set(item.solution_family, (counts.get(item.solution_family) ?? 0) + 1);
    }
    return Array.from(counts.entries()).sort((left, right) => left[0].localeCompare(right[0]));
  }, [visibleSolutions]);

  if (catalog.isLoading || countries.isLoading) {
    return <FeedbackBlock>{t("catalog.loading")}</FeedbackBlock>;
  }

  return (
    <div style={{ display: "grid", gap: 20 }}>
      <div style={{ display: "grid", gap: 6 }}>
        <div style={{ fontSize: 13, color: "#627084", textTransform: "uppercase", letterSpacing: 0 }}>{t("catalog.kicker")}</div>
        <h1 style={{ margin: 0, fontSize: 30, fontWeight: 800 }}>{t("catalog.title")}</h1>
        <p style={{ margin: 0, color: "#627084", maxWidth: 760 }}>{t("catalog.subtitle")}</p>
      </div>

      {catalog.error ? (
        <FeedbackBlock tone="error">{t("catalog.error")}</FeedbackBlock>
      ) : null}

      <section style={{ border: "1px solid #e5e7eb", borderRadius: 8, background: "#fff", padding: 18, display: "grid", gap: 14 }}>
        <div style={{ display: "grid", gridTemplateColumns: "minmax(220px, 1.5fr) repeat(4, minmax(150px, 1fr))", gap: 12 }}>
          <input
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder={t("catalog.searchPlaceholder")}
            style={inputStyle}
          />
          <select value={country} onChange={(event) => setCountry(event.target.value)} style={inputStyle}>
            <option value="">{t("catalog.allCountries")}</option>
            {(countries.data?.data ?? []).map((item) => (
              <option key={item.id} value={item.country_code}>
                {(language === "fr" ? item.name_fr : item.name_en) || item.name_fr}
              </option>
            ))}
          </select>
          <select value={family} onChange={(event) => setFamily(event.target.value)} style={inputStyle}>
            <option value="">{t("catalog.allFamilies")}</option>
            {families.map((item) => (
              <option key={item} value={item}>{item}</option>
            ))}
          </select>
          <select value={buildingType} onChange={(event) => setBuildingType(event.target.value)} style={inputStyle}>
            <option value="">{t("catalog.allBuildings")}</option>
            {buildingTypes.map((item) => (
              <option key={item} value={item}>{t(`projects.buildingTypes.${item}`)}</option>
            ))}
          </select>
          <select value={scope} onChange={(event) => setScope(event.target.value)} style={inputStyle}>
            <option value="">{t("catalog.allScopes")}</option>
            <option value="global">{t("catalog.scope.global")}</option>
            <option value="country_specific">{t("catalog.scope.country")}</option>
            <option value="organization_specific">{t("catalog.scope.organization")}</option>
          </select>
        </div>

        <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
          {familyStats.length === 0 ? (
            <span style={{ color: "#627084", fontSize: 14 }}>{t("catalog.noFamilyStats")}</span>
          ) : familyStats.map(([name, count]) => (
            <span key={name} style={{ border: "1px solid #dbe4ee", borderRadius: 8, padding: "8px 10px", background: "#f8fafc", fontSize: 13 }}>
              <strong>{name}</strong> - {count}
            </span>
          ))}
        </div>
      </section>

      {visibleSolutions.length === 0 ? (
        <FeedbackBlock>{t("catalog.empty")}</FeedbackBlock>
      ) : (
        <section style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: 14 }}>
          {visibleSolutions.map((item) => (
            <article key={item.id} style={{ border: "1px solid #e5e7eb", borderRadius: 8, background: "#fff", padding: 16, display: "grid", gap: 12 }}>
              <div style={{ display: "flex", justifyContent: "space-between", gap: 12, alignItems: "start" }}>
                <div style={{ display: "grid", gap: 4 }}>
                  <div style={{ fontSize: 12, color: "#627084", textTransform: "uppercase", letterSpacing: 0 }}>{item.solution_family}</div>
                  <h2 style={{ margin: 0, fontSize: 18 }}>{item.name}</h2>
                </div>
                {item.is_commercial_offer ? (
                  <span style={{ border: "1px solid #bfdbfe", borderRadius: 8, color: "#1d4ed8", padding: "4px 8px", fontSize: 12, fontWeight: 700 }}>
                    {t("catalog.commercialOffer")}
                  </span>
                ) : null}
              </div>

              <p style={{ margin: 0, color: "#334155", lineHeight: 1.5 }}>{item.description}</p>

              <dl style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, margin: 0 }}>
                <Metric label={t("catalog.capex")} value={formatMoney(item.default_capex)} />
                <Metric label={t("catalog.unitCost")} value={formatMoney(item.default_unit_cost)} />
                <Metric label={t("catalog.lifetime")} value={item.lifetime_years ? `${item.lifetime_years} ${t("catalog.years")}` : "-"} />
                <Metric label={t("catalog.defaultQuantity")} value={item.default_quantity ? `${item.default_quantity} ${item.default_unit ?? ""}` : "-"} />
              </dl>

              <div style={{ display: "grid", gap: 6, fontSize: 13, color: "#627084" }}>
                <div><strong style={{ color: "#334155" }}>{t("catalog.bacsImpact")}</strong> {getBacsImpactLabel(item, t("catalog.bacsNeutral"))}</div>
                <div><strong style={{ color: "#334155" }}>{t("catalog.targets")}</strong> {item.target_scopes.join(", ")}</div>
                <div><strong style={{ color: "#334155" }}>{t("catalog.scopeLabel")}</strong> {item.scope}{item.country_code ? ` - ${item.country_code}` : ""}</div>
              </div>
            </article>
          ))}
        </section>
      )}
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div style={{ border: "1px solid #edf2f7", borderRadius: 8, padding: 10, background: "#f8fafc" }}>
      <dt style={{ color: "#627084", fontSize: 12 }}>{label}</dt>
      <dd style={{ margin: "4px 0 0", fontWeight: 800 }}>{value}</dd>
    </div>
  );
}
