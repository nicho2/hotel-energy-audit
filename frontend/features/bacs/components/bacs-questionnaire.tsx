"use client";

import type { BacsDomain, BacsFunctionResponse } from "@/types/bacs";
import { BacsDomainSection } from "./bacs-domain-section";

const domainOrder: BacsDomain[] = ["monitoring", "heating", "cooling_ventilation", "dhw", "lighting"];

type BacsQuestionnaireProps = {
  functions: BacsFunctionResponse[];
  selectedFunctionIds: string[];
  onToggle: (functionId: string, nextSelected: boolean) => void;
};

export function BacsQuestionnaire({ functions, selectedFunctionIds, onToggle }: BacsQuestionnaireProps) {
  return (
    <div style={{ display: "grid", gap: 16 }}>
      {domainOrder
        .map((domain) => ({
          domain,
          items: functions.filter((item) => item.domain === domain),
        }))
        .filter((group) => group.items.length > 0)
        .map((group) => (
          <BacsDomainSection
            key={group.domain}
            domain={group.domain}
            functions={group.items}
            selectedFunctionIds={selectedFunctionIds}
            onToggle={onToggle}
          />
        ))}
    </div>
  );
}
