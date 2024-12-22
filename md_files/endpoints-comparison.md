# Endpoints 完整比對清單

## Issues相關 API
| Python方法 | Markdown是否存在 | 端點路徑 |
|------------|-----------------|----------|
| get_issue_by_id | ✅ | `/api/findings/issues/{id}` |
| get_issues | ✅ | `/api/findings/issues` |
| get_issue_triage_history | ✅ | `/api/findings/issues/{id}/triage-history` |
| get_detection_history | ✅ | `/api/findings/issues/{id}/detection-history` |
| count_issues | ✅ | `/api/findings/issues/_actions/count` |
| count_issues_over_time | ✅ | `/api/findings/issues/_actions/count-over-time` |
| export_issues | ✅ | `/api/findings/issues/_actions/export` |

## Occurrences相關 API
| Python方法 | Markdown是否存在 | 端點路徑 |
|------------|-----------------|----------|
| get_occurrences | ✅ | `/api/findings/occurrences` |
| get_occurrence_by_id | ✅ | `/api/findings/occurrences/{id}` |
| get_occurrence_snippet | ✅ | `/api/findings/occurrences/{id}/snippet` |
| get_occurrence_assist | ✅ | `/api/findings/occurrences/{id}/assist` |
| get_occurrence_artifact | ✅ | `/api/findings/occurrences/{id}/artifacts/{artifact_id}` |

## Component Version相關 API
| Python方法 | Markdown是否存在 | 端點路徑 |
|------------|-----------------|----------|
| get_component_versions | ✅ | `/api/findings/component-versions` |
| get_component_version_by_id | ✅ | `/api/findings/component-versions/{id}` |
| count_component_versions | ✅ | `/api/findings/component-versions/_actions/count` |
| get_component_version_triage_history | ✅ | `/api/findings/component-versions/{id}/triage-history` |

## Component Origin相關 API
| Python方法 | Markdown是否存在 | 端點路徑 |
|------------|-----------------|----------|
| get_component_origin | ✅ | `/api/findings/component-origins/{id}` |
| get_component_origins | ✅ | `/api/findings/component-origins` |
| get_component_origin_matches | ✅ | `/api/findings/component-origins/{id}/matches` |

## License相關 API
| Python方法 | Markdown是否存在 | 端點路徑 |
|------------|-----------------|----------|
| get_license_by_id | ✅ | `/api/findings/licenses/{id}` |
| get_licenses | ✅ | `/api/findings/licenses` |
| count_licenses | ✅ | `/api/findings/licenses/_actions/count` |

## Taxa相關 API
| Python方法 | Markdown是否存在 | 端點路徑 |
|------------|-----------------|----------|
| get_taxon | ✅ | `/api/findings/taxa/{id}` |
| get_taxon_subtaxa | ✅ | `/api/findings/taxa/{id}/subtaxa` |
| get_taxon_issue_types | ✅ | `/api/findings/taxa/{id}/issue-types` |
| get_taxonomies | ✅ | `/api/findings/taxonomies` |

## 比對結果

所有Python代碼中的端點都已經在Markdown文檔中有對應的curl命令，沒有遺漏的端點。

主要的區別在於：
1. Python代碼使用類方法的形式組織API調用
2. Markdown文檔使用curl命令形式展示API調用
3. 兩者的參數處理方式不同，但邏輯相同

每個端點都包含：
- 完整的路徑
- 必要的請求頭
- 查詢參數
- 響應格式