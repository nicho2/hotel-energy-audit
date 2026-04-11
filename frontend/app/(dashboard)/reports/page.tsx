"use client";

import { useI18n } from "@/providers/i18n-provider";

export default function Page() {
  const { t } = useI18n();

  return <div>{t("reports.globalPlaceholder")}</div>;
}
