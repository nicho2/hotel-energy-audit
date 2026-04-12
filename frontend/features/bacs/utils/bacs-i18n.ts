import type { BacsFunctionResponse, BacsMissingFunctionResponse } from "@/types/bacs";

type Translate = (key: string) => string;

function translateOrFallback(t: Translate, key: string, fallback: string | null) {
  const translated = t(key);
  return translated.startsWith("[[") ? fallback : translated;
}

export function getBacsFunctionName(
  item: Pick<BacsFunctionResponse | BacsMissingFunctionResponse, "code" | "name">,
  t: Translate,
) {
  return translateOrFallback(t, `wizard.bacs.functions.${item.code}.name`, item.name) ?? item.name;
}

export function getBacsFunctionDescription(
  item: Pick<BacsFunctionResponse | BacsMissingFunctionResponse, "code" | "description">,
  t: Translate,
) {
  return translateOrFallback(t, `wizard.bacs.functions.${item.code}.description`, item.description);
}
