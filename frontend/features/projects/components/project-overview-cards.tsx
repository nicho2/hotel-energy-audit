import type { ProjectOverviewCard } from "@/types/project";

type ProjectOverviewCardsProps = {
  cards: ProjectOverviewCard[];
};

export function ProjectOverviewCards({ cards }: ProjectOverviewCardsProps) {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(4, minmax(0, 1fr))", gap: 16 }}>
      {cards.map((card) => (
        <div
          key={card.key}
          style={{
            border: "1px solid #e5e7eb",
            borderRadius: 16,
            background: "#fff",
            padding: 20,
            display: "grid",
            gap: 8,
          }}
        >
          <div style={{ fontSize: 13, color: "#627084", textTransform: "uppercase", letterSpacing: "0.04em" }}>
            {card.label}
          </div>
          <div style={{ fontSize: 28, fontWeight: 700, color: "#142033" }}>{card.value}</div>
          <div style={{ fontSize: 13, color: "#627084" }}>{card.helper}</div>
        </div>
      ))}
    </div>
  );
}
