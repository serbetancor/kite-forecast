import {
  defineConfigWithVueTs,
  vueTsConfigs,
} from "@vue/eslint-config-typescript"
import simpleImportSort from "eslint-plugin-simple-import-sort"

export default defineConfigWithVueTs(vueTsConfigs.recommended, {
  files: ["**/*.{js,jsx,ts,tsx,vue}"],
  plugins: {
    "simple-import-sort": simpleImportSort,
  },
  rules: {
    "simple-import-sort/imports": "error",
    "simple-import-sort/exports": "error",
  },
})
